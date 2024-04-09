from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from utilities.helpers import init_database, get_response
import streamlit as st
import os

# Load environment variables
load_dotenv()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]

st.set_page_config(page_title="Chat with PostgreSQL", page_icon=":speech_balloon:")

st.title("Chat with PostgreSQL")

with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat application using PostgreSQL. Connect to the database and start chatting.")

    st.text_input("Host", value=os.getenv("DB_HOST"), key="Host")
    st.text_input("Port", value=os.getenv("DB_PORT"), key="Port")
    st.text_input("User", value=os.getenv("DB_USER"), key="User")
    st.text_input("Password", type="password", value=os.getenv("DB_PASSWORD"), key="Password")
    st.text_input("Database", value=os.getenv("DB_NAME"), key="Database")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            st.session_state.db = db
            st.success("Connected to database!")

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")

if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
        st.markdown(response)

    st.session_state.chat_history.append(AIMessage(content=response))
