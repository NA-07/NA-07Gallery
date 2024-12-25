import streamlit as st
import sqlite3
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.wsgi import WSGIMiddleware

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect('contact_form.db')
    return conn

# Function to create the table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            comments TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert form data into the table
def insert_data(first_name, last_name, email, comments):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO personal (first_name, last_name, email, comments)
        VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, email, comments))
    conn.commit()
    conn.close()

# Streamlit app
def main():
    st.title("Contact Us from NA-07Gallery(7th Batch)")
    st.write("Have Queries? Send us a message now!")

    with st.form(key='contact_form'):
        first_name = st.text_input("First name", max_chars=100)
        last_name = st.text_input("Last name", max_chars=100)
        email = st.text_input("Email address")
        comments = st.text_area("Comments", max_chars=500)

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if not first_name or not last_name or not email or not comments:
                st.error("All fields are required.")
            elif '@' not in email:
                st.error("Invalid email format.")
            else:
                insert_data(first_name, last_name, email, comments)
                st.success(f"Thank you {first_name} {last_name}! Your details have been submitted successfully.")

if __name__ == "__main__":
    create_table()
    main()

# FastAPI app
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_form():
    with open("contact.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.post("/submit")
async def handle_form_submission(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    comments: str = Form(...)
):
    insert_data(first_name, last_name, email, comments)
    return {"message": "Form submitted successfully"}

# Integrate FastAPI with Streamlit
app.mount("/streamlit", WSGIMiddleware(main))