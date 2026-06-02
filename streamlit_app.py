import streamlit as st
from groq import Groq
import sqlite3
import pandas as pd

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- GROQ CLIENT ----------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []

if "sql_query" not in st.session_state:
    st.session_state.sql_query = ""

if "df" not in st.session_state:
    st.session_state.df = None

if "question" not in st.session_state:
    st.session_state.question = ""

# ---------------- FUNCTIONS ----------------

def clear_text():
    st.session_state.question = ""
    st.session_state.sql_query = ""
    st.session_state.df = None

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🤖 AI SQL ASSISTANT")

    st.write("Database: SQLite")

    st.divider()

    st.subheader("Recent Queries")

    if not st.session_state.history:
        st.caption("No queries yet")

    for q in reversed(st.session_state.history[-5:]):
        st.write("•", q)

# ---------------- MAIN UI ----------------

st.title("🤖 AI SQL Assistant")

st.caption(
    "Convert natural language into SQL queries."
)

st.text_input(
    "Ask your question",
    placeholder="Example: Show all students from Mumbai",
    key="question"
)

col1, col2 = st.columns(2)

with col1:
    generate = st.button(
        "🚀 Generate SQL",
        use_container_width=True
    )

with col2:
    st.button(
        "🗑 Clear Text",
        use_container_width=True,
        on_click=clear_text
    )

# ---------------- GENERATE SQL ----------------

if generate and st.session_state.question.strip():

    question = st.session_state.question.strip()

    st.session_state.history.append(question)

    prompt = f"""
You are an expert SQLite SQL generator.

Database Schema:

Table: students

Columns:
ID INTEGER
Name TEXT
python INTEGER
DBMS INTEGER
Percentage REAL
City TEXT

Question:
{question}

Rules:
- Return ONLY SQLite SQL.
- No explanation.
- No markdown.
- Use exact table and column names.
- Generate only SELECT statements.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER.
- For lowest marks use MIN().
- For highest marks use MAX().
"""

    try:

        with st.spinner("Generating SQL..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            sql_query = response.choices[0].message.content

            sql_query = sql_query.replace("```sql", "")
            sql_query = sql_query.replace("```", "")
            sql_query = sql_query.strip()

            st.session_state.sql_query = sql_query

        # ---------------- DATABASE ----------------

        if not sql_query.upper().startswith("SELECT"):
            st.error("Only SELECT queries are allowed.")
            st.stop()

        conn = sqlite3.connect("college.db")

        cursor = conn.cursor()

        try:

            cursor.execute(sql_query)

            result = cursor.fetchall()

            if cursor.description:

                headers = [
                    column[0]
                    for column in cursor.description
                ]

                df = pd.DataFrame(
                    result,
                    columns=headers
                )

                st.session_state.df = df

            else:
                st.session_state.df = pd.DataFrame()

        except Exception as sql_error:

            st.error(f"SQL Error: {sql_error}")

            st.session_state.df = None

        finally:

            conn.close()

    except Exception as e:

        st.error(f"Model Error: {e}")

# ---------------- SHOW SQL ----------------

if st.session_state.sql_query:

    st.subheader("Generated SQL")

    st.code(
        st.session_state.sql_query,
        language="sql"
    )

# ---------------- SHOW RESULTS ----------------

if st.session_state.df is not None:

    st.metric(
        "Rows Returned",
        len(st.session_state.df)
    )

    st.subheader("Results")

    st.dataframe(
        st.session_state.df,
        use_container_width=True
    )