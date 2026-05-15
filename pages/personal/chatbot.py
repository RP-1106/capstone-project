import streamlit as st
import os
import mysql.connector as sql
import pandas as pd
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
#from langchain_community.chains import RetrievalQA
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

# ============================================================
# SECRETS: Read from Streamlit secrets (cloud) or .env (local)
# ============================================================

def get_secret(key, section=None):
    """
    Read a secret from st.secrets (Streamlit Cloud) first,
    then fall back to environment variables for local development.
    """
    try:
        if section:
            return st.secrets[section][key]
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.getenv(key)

GROQ_API_KEY = get_secret("GROQ_API_KEY")

mysql_config = {
    "host":     get_secret("host",     "mysql"),
    "port":     int(get_secret("port", "mysql") or 3306),
    "user":     get_secret("user",     "mysql"),
    "password": get_secret("password", "mysql"),
    "database": get_secret("database", "mysql"),
}

# ============================================================
# STEP 1: CACHED MODEL + EMBEDDINGS
# Using @st.cache_resource so these load ONCE and are reused.
# This is the main fix for the 30-second+ response times.
# ============================================================

@st.cache_resource
def load_groq_model():
    """Load the Groq LLM once and cache it for the session lifetime."""
    return ChatGroq(
        temperature=0.1,
        model_name="llama-3.3-70b-versatile",
        groq_api_key=GROQ_API_KEY,
    )

@st.cache_resource
def load_embedding_function():
    """
    Load the HuggingFace embedding model once and cache it.
    Previously this was re-initialised on every interaction,
    causing the long delays.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

model             = load_groq_model()
embedding_function = load_embedding_function()

# ============================================================
# STEP 2: DATABASE CONFIG & INITIALISATION
# ============================================================

# Cross-platform path helper (fixes Windows backslash issues on Linux/cloud)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def data_path(*parts):
    """Return an absolute path inside the project's data/ folder."""
    return os.path.join(BASE_DIR, "data", *parts)


def initialize_database():
    """
    Connect to the cloud MySQL instance, create the database/table if
    they don't exist, and seed with dummy1.csv if the table is empty.
    """
    # Connect without specifying a database first so we can CREATE it
    init_config = {k: v for k, v in mysql_config.items() if k != "database"}
    mycon = sql.connect(**init_config)
    cursor = mycon.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_config['database']}")
    cursor.execute(f"USE {mysql_config['database']}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Capstone (
            Date            DATE,
            Mode            VARCHAR(255),
            Category        VARCHAR(255),
            Remark          VARCHAR(255),
            Amount          FLOAT,
            Income_Expense  VARCHAR(50),
            Transaction_id  VARCHAR(50) PRIMARY KEY
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM Capstone")
    count = cursor.fetchone()[0]

    csv_file = data_path("dummy1.csv")
    if count == 0 and os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        records = []
        for _, row in df.iterrows():
            date_parts = str(row["Date"]).split("-")
            # Handle both DD-MM-YYYY and YYYY-MM-DD in source CSV
            if len(date_parts[0]) == 4:
                mysql_date = row["Date"]          # already YYYY-MM-DD
            else:
                mysql_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
            records.append((
                mysql_date, row["Mode"], row["Category"], row["Remark"],
                float(row["Amount"]), row["Income_Expense"], row["Transaction_id"],
            ))

        insert_sql = """INSERT IGNORE INTO Capstone
                        (Date, Mode, Category, Remark, Amount, Income_Expense, Transaction_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(insert_sql, records)
        mycon.commit()
        print(f"Seeded {len(records)} records from dummy1.csv")

    mycon.close()

# ============================================================
# STEP 3: SQL → ENGLISH (DataDigger)
# ============================================================

sql_to_english_prompt_template = """
You are an expert at converting SQL query results into natural, conversational English responses.

CRITICAL CONVERSION GUIDELINES:
1. Match the exact style of the provided examples
2. Preserve all original data details
3. Use conversational but precise language
4. Follow the specific response patterns demonstrated
5. Always use ₹ instead of $ for displaying amount

Context:
- Original Question: {original_question}
- SQL Query: {sql_query}
- Column Names: {columns}
- Result: {result}

Conversion Rules:
- For single values: Provide context and explain the value
- For single rows: Create a narrative explaining the transaction details
- For multiple rows: Summarize key insights
- For aggregations: Explain the significance of the totals
- Always maintain a helpful, assistant-like tone

Provide ONLY the natural language response. Do not include the original question or query details.
"""

def generate_sql_to_english_response(original_question, sql_query, columns, result):
    prompt = PromptTemplate(
        template=sql_to_english_prompt_template,
        input_variables=["original_question", "sql_query", "columns", "result"],
    )
    input_dict = {
        "original_question": original_question,
        "sql_query": sql_query,
        "columns": ", ".join(columns),
        "result": str(result),
    }
    response = model.invoke(prompt.format(**input_dict))
    return response.content


def natural_language_interpretation(original_question, sql_query, columns, result):
    if not result or (
        isinstance(result, list)
        and isinstance(result[0], str)
        and result[0].startswith("Error:")
    ):
        return "I couldn't find any information matching your query."

    if len(result) == 1:
        try:
            return generate_sql_to_english_response(
                original_question, sql_query, columns, result
            )
        except Exception as e:
            print(f"SQL to English conversion error: {e}")
            row = result[0]
            if len(columns) == 1 and len(row) == 1:
                return f"The result is: {row[0]}"
            description = "Query Result:\n"
            for col, val in zip(columns, row):
                description += f"- **{col}**: {val}\n"
            return description

    if len(columns) == 1 and len(result[0]) == 1:
        try:
            return generate_sql_to_english_response(
                original_question, sql_query, columns, result
            )
        except Exception as e:
            print(f"SQL to English conversion error: {e}")
            return f"Amount corresponding to the query sums to {result[0][0]}"

    return "Found multiple records. Displaying in table format."

# ============================================================
# STEP 4: SQL QUERY EXECUTION
# ============================================================

def read_sql_query(sql_query, db_config):
    try:
        mycon = sql.connect(**db_config)
        cursor = mycon.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = (
            [col[0] for col in cursor.description] if cursor.description else []
        )
        cursor.close()
        mycon.close()
        return rows, columns
    except sql.Error as e:
        return [f"Error: {e}"], []


data_digger_prompt_template = """
You are an expert in converting English questions to MySQL SQL queries!
The MySQL database has a table named Capstone with the following columns:
- Date (DATE)
- Mode (VARCHAR)
- Category (VARCHAR) - IMPORTANT: This contains specific expense and income categories listed below
- Remark (VARCHAR) - IMPORTANT: This contains specific details about the transaction like 'Hospital', 'Restaurant Name', 'Gas Station', etc.
- Amount (FLOAT)
- Income_Expense (VARCHAR) - Can be 'Income' or 'Expense'
- Transaction_id (VARCHAR) - Primary key

CATEGORY TYPES AND THEIR CLASSIFICATIONS:
# Expense categories:
- Groceries (Expense)
- Education (Expense)
- Healthcare (Expense)
- Transportation (Expense)
- Utilities (Expense)
- Communication (Expense)
- Enrichment (Expense)
- Domestic_Help (Expense)
- Care_Essentials (Expense)
- Financial_Dues (Expense)
- Discretionary (Expense)

# Income categories:
- Salary (Income)
- Pension (Income)
- Rewards (Income)
- Stocks (Income)
- Interest (Income)
- Side_Hustle (Income)
- Gifts (Income)

# Dual-purpose categories (can be either Income or Expense):
- Rent (Dual)
- Miscellaneous (Dual)

IMPORTANT DISTINCTION:
- Category is the specific type of income or expense as listed above
- Remark contains the specific detail or place of transaction (e.g., 'Hospital visit', 'Grocery store', 'College fee')

IMPORTANT ABOUT CASE SENSITIVITY:
- Always use LOWER() function when performing text comparisons to make searches case-insensitive
- Example: LOWER(Remark) LIKE LOWER('%kitchen%') instead of Remark LIKE '%Kitchen%'

IMPORTANT ABOUT SEARCH TERMS:
- When the user asks about transactions related to an item that could appear in either Category OR Remark columns, your query must check BOTH columns using the OR operator
- Example: For "Show me all milk transactions" use: WHERE LOWER(Category) LIKE LOWER('%milk%') OR LOWER(Remark) LIKE LOWER('%milk%')

IMPORTANT ABOUT DATE HANDLING:
- The Date column is stored in MySQL's native YYYY-MM-DD format
- For date operations: YEAR(Date), MONTH(Date), DAY(Date), CURRENT_DATE, DATE_SUB, BETWEEN, etc.

Examples:
1. Question: How many entries of records are present?
   SQL: SELECT COUNT(*) FROM Capstone;

2. Question: Give me the category and amount corresponding to Transaction id TXN129?
   SQL: SELECT Category, Amount FROM Capstone WHERE Transaction_id="TXN129";

3. Question: Display all the rows which contain amount between 100 and 1000 within the first 15 rows.
   SQL: SELECT * FROM Capstone WHERE Amount BETWEEN 100 AND 1000 LIMIT 15;

4. Question: What are the total expenses for each category?
   SQL: SELECT Category, SUM(Amount) AS TotalExpenses FROM Capstone WHERE Income_Expense = 'Expense' GROUP BY Category ORDER BY TotalExpenses DESC;

5. Question: What is the total amount spent on healthcare?
   SQL: SELECT SUM(Amount) AS TotalHealthcareExpenses FROM Capstone WHERE LOWER(Category) = LOWER('Healthcare') AND Income_Expense = 'Expense';

6. Question: Show me all income transactions
   SQL: SELECT * FROM Capstone WHERE Income_Expense = 'Income';

IMPORTANT NOTES:
- Return ONLY the SQL query without explanations, quotation marks, or text
- Do not include the word 'SQL' or 'sql' in your response
- ALWAYS use LOWER() for text comparisons
- Check BOTH Category and Remark columns when relevant using OR

Question: {question}
SQL:
"""


def get_mistral_response(question, prompt_template):
    prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
    llm_chain = prompt | model
    response = llm_chain.invoke({"question": question})
    response_metadata = response.response_metadata
    timing_info = {
        "completion_time": response_metadata.get("token_usage", {}).get("completion_time", 0),
        "prompt_time":     response_metadata.get("token_usage", {}).get("prompt_time", 0),
        "queue_time":      response_metadata.get("token_usage", {}).get("queue_time", 0),
        "total_time":      response_metadata.get("token_usage", {}).get("total_time", 0),
    }
    return {"query": response.content, "timing": timing_info}

# ============================================================
# STEP 5: FINMENTOR — Document QA
# ============================================================

def docs_preprocessing_helper(file):
    loader = CSVLoader(file)
    docs = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
    return text_splitter.split_documents(docs)


def setup_chroma_db(docs, embedding_fn):
    """In-memory Chroma DB using EphemeralClient (no SQLite file needed)."""
    import chromadb
    from langchain_community.vectorstores import Chroma

    client = chromadb.EphemeralClient()
    texts     = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]

    return Chroma.from_texts(
        texts=texts,
        embedding=embedding_fn,
        metadatas=metadatas,
        collection_name="fin_mentor",
        client=client,
    )

@st.cache_resource
def get_mentor_chain():
    file_path      = data_path("custom.csv")
    docs           = docs_preprocessing_helper(file_path)
    mentor_persist = os.path.join(BASE_DIR, "chroma_fin_mentor")
    db             = setup_chroma_db(docs, embedding_function, mentor_persist)
    prompt         = create_prompt_template()
    return create_retrieval_chain(model, db, prompt)

def create_prompt_template():
    template = """You are a finance consultant chatbot. Answer the customer's questions only using the source data provided.
Please answer to their specific questions. If you are unsure, say "I don't know, please call our customer support". Keep your answers concise.

{context}

Question: {question}
Answer:"""
    return PromptTemplate(template=template, input_variables=["context", "question"])


def create_retrieval_chain(llm, db, prompt):
    retriever = db.as_retriever(search_kwargs={"k": 1})
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def query_chain(chain, query):
    return chain.invoke(query)

# ============================================================
# STREAMLIT UI
# ============================================================

def data_digger():
    """History-Based Bot that analyzes transaction data using SQL."""
    chat_container  = st.container()
    input_container = st.container()

    # Initialize database (safe to call repeatedly — uses CREATE IF NOT EXISTS)
    try:
        initialize_database()
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.info("Please check your database credentials in the app settings.")
        return

    if "digger_messages" not in st.session_state:
        st.session_state.digger_messages = []
    if "dataframes" not in st.session_state:
        st.session_state.dataframes = {}
    if "query_counter" not in st.session_state:
        st.session_state.query_counter = 0

    with input_container:
        prompt = st.chat_input("Ask questions about your transaction history...")
        qid = st.session_state.query_counter

        if prompt:
            st.session_state.digger_messages.append(
                {"query_id": qid, "role": "user", "content": prompt}
            )

            with st.spinner("Generating SQL query..."):
                result      = get_mistral_response(prompt, data_digger_prompt_template)
                sql_query   = result["query"]

            try:
                with st.spinner("Executing query..."):
                    result, columns = read_sql_query(sql_query, mysql_config)

                if (
                    isinstance(result, list)
                    and result
                    and isinstance(result[0], str)
                    and result[0].startswith("Error:")
                ):
                    formatted_response = (
                        f"**SQL Query:**\n```sql\n{sql_query}\n```\n\n"
                        f"**Error:**\n{result[0]}"
                    )
                    st.session_state.digger_messages.append(
                        {"query_id": qid, "role": "assistant", "content": formatted_response}
                    )
                else:
                    nl_response = natural_language_interpretation(
                        prompt, sql_query, columns, result
                    )
                    formatted_response = (
                        f"**SQL Query:**\n```sql\n{sql_query}\n```\n\n"
                        f"**Insights:**\n{nl_response}"
                    )
                    st.session_state.digger_messages.append(
                        {"query_id": qid, "role": "assistant", "content": formatted_response}
                    )
                    if result and len(result) > 0:
                        st.session_state.dataframes[qid] = pd.DataFrame(result, columns=columns)

                st.session_state.query_counter += 1

            except Exception as e:
                formatted_response = (
                    f"**SQL Query:**\n```sql\n{sql_query}\n```\n\n"
                    f"**Error:**\n{str(e)}"
                )
                st.session_state.digger_messages.append(
                    {"query_id": qid, "role": "assistant", "content": formatted_response}
                )

    with chat_container:
        for message in st.session_state.digger_messages:
            qid = message["query_id"]
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if (
                    message["role"] == "assistant"
                    and qid in st.session_state.get("dataframes", {})
                ):
                    st.dataframe(st.session_state.dataframes[qid])


def fin_mentor():
    chat_container  = st.container()
    input_container = st.container()

    if "mentor_messages" not in st.session_state:
        st.session_state.mentor_messages = []

    st.session_state.mentor_chain = get_mentor_chain()

    with input_container:
        prompt = st.chat_input("What is your finance question?")
        if prompt:
            st.session_state.mentor_messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                response = query_chain(st.session_state.mentor_chain, prompt)
            st.session_state.mentor_messages.append({"role": "assistant", "content": response})

    with chat_container:
        for message in st.session_state.mentor_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


def custom_bot():
    """Custom Bot page with top navigation for two different bots."""
    st.markdown("""
    <style>
        * { font-family: Verdana, sans-serif !important; }
        .stTabs [data-baseweb="tab-list"] {
            display: flex; justify-content: center;
            gap: 8px; border-bottom: 2px solid #4e807c;
        }
        .stTabs [data-baseweb="tab"] div {
            height: 50px; width: 380px;
            background-color: #78c4be; color: #333333;
            border-radius: 8px 8px 0 0; padding: 10px;
            text-align: center; font-weight: bold !important;
            font-size: 18px !important; cursor: pointer;
        }
        .stTabs [aria-selected="true"] div {
            background-color: #4e807c; color: white; font-weight: bold !important;
        }
        .stChatInputContainer {
            position: sticky; bottom: 0;
            background-color: white; z-index: 1; padding-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.write("## 💬 Financial Assistant")
    st.write(
        "Choose between two specialized bots: one that analyzes your transaction "
        "history for insights, and another that provides expert financial advice."
    )

    tab1, tab2 = st.tabs(["DataDigger📈: History-Based", "FinMentor🧠: Intelligence-Based"])

    with tab1:
        st.write("#### Welcome to DataDigger!")
        st.write("Your financial history, decoded with precision.")
        data_digger()

    with tab2:
        st.write("#### Welcome to FinMentor!")
        st.write("Smart financial advice, simplified.")
        fin_mentor()
