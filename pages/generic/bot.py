import streamlit as st
import os
import numpy as np
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer
import faiss

import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

# ============================================================
# SECRETS
# ============================================================

def get_secret(key, section=None):
    try:
        return st.secrets[section][key] if section else st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.getenv(key)

# ============================================================
# CACHED RESOURCES
# ============================================================

@st.cache_resource
def load_groq_model():
    groq_api_key = get_secret("GROQ_API_KEY")
    if not groq_api_key:
        st.error("Groq API key not found.")
        st.stop()
    return ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,
    )

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def data_path(*parts):
    return os.path.join(BASE_DIR, "data", *parts)

# ============================================================
# FAISS INDEX
# ============================================================

def docs_preprocessing_helper(file):
    from langchain_community.document_loaders import CSVLoader
    from langchain_text_splitters import CharacterTextSplitter
    loader = CSVLoader(file)
    docs = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
    return text_splitter.split_documents(docs)


def build_faiss_index(docs):
    embed_model = load_embedding_model()
    texts = [doc.page_content for doc in docs]
    embeddings = embed_model.encode(texts, convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index, texts


def retrieve(query, index, texts, k=3):
    embed_model = load_embedding_model()
    q_vec = embed_model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(q_vec)
    _, indices = index.search(q_vec, k)
    return "\n".join(texts[i] for i in indices[0] if i < len(texts))


PROMPT_TEMPLATE = """You are a finance consultant chatbot. Answer the customer's questions only using the source data provided.
Please answer to their specific questions. If you are unsure, say "I don't know, please call our customer support". Keep your answers concise.

{context}

Question: {question}
Answer:"""


@st.cache_resource
def get_bot_chain():
    """Build FAISS index and return a callable. Cached for the app lifetime — safe across tab switches."""
    docs         = docs_preprocessing_helper(data_path("generic.csv"))
    index, texts = build_faiss_index(docs)
    model        = load_groq_model()

    def run(query):
        context = retrieve(query, index, texts)
        filled  = PROMPT_TEMPLATE.format(context=context, question=query)
        return model.invoke(filled).content

    return run

# ============================================================
# STREAMLIT PAGE
# ============================================================

def bot_page():
    st.markdown("""
    <style>
    * { font-family: Verdana, sans-serif !important; }
    [data-testid="stChatMessageContent"] { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:15px;margin-bottom:-20px;margin-top:-10px">
      <h3 style="margin:0;">Let our bot help you with your queries!</h3>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chain = get_bot_chain()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(
                    f'<div style="color:white;">{message["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(message["content"])

    if user_input := st.chat_input("How can I assist you today?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            with st.spinner("Thinking..."):
                response = chain(user_input)
            placeholder.markdown(
                f'<div style="color:white;">{response}</div>',
                unsafe_allow_html=True,
            )

        st.session_state.messages.append({"role": "assistant", "content": response})