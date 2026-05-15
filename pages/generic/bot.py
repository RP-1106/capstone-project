import streamlit as st
import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

# ============================================================
# SECRETS: Read from st.secrets (cloud) or env vars (local)
# ============================================================

def get_secret(key, section=None):
    try:
        return st.secrets[section][key] if section else st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.getenv(key)

# ============================================================
# CACHED RESOURCES — load once, reuse across all interactions
# ============================================================

@st.cache_resource
def load_groq_model():
    """Load the Groq LLM once and cache it."""
    groq_api_key = get_secret("GROQ_API_KEY")
    if not groq_api_key:
        st.error("Groq API key not found. Please set GROQ_API_KEY in your secrets.")
        st.stop()
    return ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,
    )

# Cross-platform data path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def data_path(*parts):
    return os.path.join(BASE_DIR, "data", *parts)

# ============================================================
# DOCUMENT HELPERS
# ============================================================

def docs_preprocessing_helper(file):
    loader = CSVLoader(file)
    docs = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
    return text_splitter.split_documents(docs)


def setup_chroma_db(docs):
    """Pure chromadb EphemeralClient — bypasses langchain_community Chroma wrapper entirely."""
    import chromadb
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    client = chromadb.EphemeralClient()
    ef = SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    collection = client.create_collection("generic_bot", embedding_function=ef)
    texts = [doc.page_content for doc in docs]
    ids   = [str(i) for i in range(len(texts))]
    collection.add(documents=texts, ids=ids)
    return collection


def create_prompt_template():
    template = """You are a finance consultant chatbot. Answer the customer's questions only using the source data provided.
Please answer to their specific questions. If you are unsure, say "I don't know, please call our customer support". Keep your answers concise.

{context}

Question: {question}
Answer:"""
    return template


def create_retrieval_chain(model, collection, prompt_template):
    """Returns a callable that retrieves context then calls the LLM."""
    def run(query):
        results  = collection.query(query_texts=[query], n_results=3)
        context  = "\n".join(results["documents"][0])
        filled   = prompt_template.format(context=context, question=query)
        return model.invoke(filled).content
    return run


def query_chain(chain, query):
    return chain(query)


@st.cache_resource
def get_bot_chain():
    model          = load_groq_model()
    docs           = docs_preprocessing_helper(data_path("generic.csv"))
    collection     = setup_chroma_db(docs)
    prompt         = create_prompt_template()
    return create_retrieval_chain(model, collection, prompt)

# ============================================================
# STREAMLIT PAGE
# ============================================================

def bot_page():
    """Bot section of the landing page."""
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

    # Load model + chain once per session
    st.session_state.chain = get_bot_chain()

    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(
                    f'<div style="color:white;">{message["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(message["content"])

    # Handle new input
    if user_input := st.chat_input("How can I assist you today?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            with st.spinner("Thinking..."):
                response = query_chain(st.session_state.chain, user_input)
            placeholder.markdown(
                f'<div style="color:white;">{response}</div>',
                unsafe_allow_html=True,
            )

        st.session_state.messages.append({"role": "assistant", "content": response})