import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

st.title("🤖 Chatbot!")


if 'messages' not in st.session_state:
    st.session_state.messages =[]

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

prompt = st.chat_input("prompt = st.chat_input('💬 Ask your any question here...'")

if prompt:
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({'role':'user','content':prompt})

    groq_sys_prompt =ChatPromptTemplate.from_template ("""
    You are very smart at everything, you always. Anwer the following question: {user_prompt}
    """)

    GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
    #print(GROQ_API_KEY)
    
    model = "llama3-8b-8192"
    groq_chat = ChatGroq(
        groq_api_key = GROQ_API_KEY,
        model_name = model
    )

    chain = groq_sys_prompt | groq_chat | StrOutputParser()

    response = chain.invoke({"user_prompt":prompt})

   # response = "I am your Assistant!"
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({'role':'assistant','content':response})
