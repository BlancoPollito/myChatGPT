#pip install streamlit langchain langchain-openai python-dotenv

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="StreamingBot", page_icon="🤖")

st.title("Hello Bozo")

#get response
def get_response(query, chat_history):
    template = """
    You are a python coder assistant, Answer the question considering the history of the conversation:
    
    Chat history: {chat_history}
    
    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()
 
    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": query
    })


#conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)


#user Input
user_query = st.chat_input("Well well well, looks who is here again!")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(ai_response))

save_button = st.button("Save Conversation")

if save_button:
    # Define the path to the save_chat_histories folder
    save_folder = os.path.join(os.path.dirname(__file__), "save_chat_histories")

    # Create the folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Define the file path with the current date for saving the chat history
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(save_folder, f"chat_history_{current_date}.txt")

    # Save the chat history to the file with the current date in the file name
    with open(file_path, "w", encoding='utf-8') as file:
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                file.write("User: " + message.content + "\n")
            elif isinstance(message, AIMessage):
                file.write("AI: " + message.content + "\n")

    st.success("Conversation saved for future usage")