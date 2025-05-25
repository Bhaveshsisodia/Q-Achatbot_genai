import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

# groq_api_key = os.getenv("GROQ_API_KEY")
# groq_api_key

## Langsmith Tracking

# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"]= "true"
# os.environ["LANGCHAIN_PROJECT"] = "Q&A Chat Bot"


prompt  = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that answers questions based on the provided context."),
        ("user", "Question : {question}"),

    ]
)

def generate_response(question, api_key, engine , temperature  , max_tokens):


    llm =ChatGroq(model=engine, groq_api_key=api_key)
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})

    return answer

st.title("Enchanced Q & A Chatbot with Groq")

st.sidebar.title("Settings")
api_key  = st.sidebar.text_input("Enter your Groq API Key", type="password")

## Drop down to select the model various Groq models
llm = st.sidebar.selectbox("Select an Groq Model",['gemma2-9b-it','llama3-8b-8192', 'llama-3.3-70b-versatile','llama-3.1-8b-instant'])

temperature  = st.sidebar.slider("Temperature",min_value =0.0 , max_value=1.0, value=0.7)

max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=3000, value=150)

## Main Interface for user input
st.write("Go ahead and ask your question!")
user_input = st.text_input("You:")

if user_input:
    response  = generate_response(user_input , api_key , llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter a question to get started.")



