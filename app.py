import ollama
import sqlite3
from tabulate import tabulate

while True:

    question = input("\nAsk SQL Question (type exit to quit): ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    prompt = f"""
    You are an SQL generator.

    Database Schema:

    Table Name: student

    Columns:
    id
    name 
    marks
    city

    Convert the following English sentence into valid SQLite SQL.

    Question:
    {question}

    Rules:
    1. Use ONLY table name student
    2. Use ONLY the columns above
    3. Return ONLY SQL
    4. No explanations
    5. No markdown
    """

    response = ollama.chat(
        model='phi3',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    sql_query = response['message']['content']

    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")
    sql_query = sql_query.strip()

    print("\nGenerated SQL:")
    print(sql_query)

    conn = sqlite3.connect("college.db")

    cursor = conn.cursor() 

    cursor.execute(sql_query)

    result = cursor.fetchall()
    print("\nResults:")
    headers = [column[0] for column in cursor.description]
    print(
        tabulate(
          result,
          headers=headers,
          tablefmt="grid"
        )
    )

    conn.close() 

