import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser 
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq

load_dotenv()

import getpass
import os
load_dotenv()

# Access the GROQ_API_KEY
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
llm=ChatGroq(
    temperature=1,
    model_name="llama-3.1-70b-versatile"
)

def scraper(link):
    
    loader=WebBaseLoader(link)
    pg_data= loader.load().pop().page_content
    first_3000_words = pg_data[:3000]
    return first_3000_words
    


def get_response(data):

    prompt_template = PromptTemplate.from_template("Topic ontent: {first_3000_words}. The provided content is sourced from Wikipedia. Summarize and explain about it in simple terms. NO PREAMBLE ")

    prompt_template.invoke({"first_3000_words": "first_3000_words"})
    



    chain_response =  prompt_template| llm
    res = chain_response.invoke({"first_3000_words": data})
    return res.content

st.set_page_config(
    page_icon='🤖',
    initial_sidebar_state='auto',
    page_title="WikiAI"
)


url_input= st.text_input("Enter wikipedia url")
submit= st.button("Summarzie")





if submit:
    if url_input.strip():  # Ensure input is not empty
        try:
            final_Data = scraper(url_input)
            st.write(get_response(final_Data))
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid Wikipedia URL.")