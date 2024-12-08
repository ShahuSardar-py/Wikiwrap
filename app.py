import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser 
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from appv2 import search_and_fetch
from groq._base_client import APIStatusError
import json
# Access the GROQ_API_KEY
load_dotenv()
import getpass
import os
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

#LLM setup
llm=ChatGroq(
    temperature=1,
    model_name="llama-3.1-70b-versatile"
)


def get_response(data,style):
    prompt_template = PromptTemplate.from_template("""
        Topic content: {data}. User has selected {style} category
                                                   The provided content is sourced from Wikipedia. Understand and summarize it according to the style the user wants it in. Here is a manual for you to understand user's intent.
                                                   If category is "For presentations" then: Create detailed, structured summaries suitable for academic or professional submissions.
                                                   If category is "General Knowledge & Understanding" then: Summarize the topic in plain and simple language suitable for a general audience, avoiding technical terms.
                                                   If category is "Fact-Checking" then: Provide a factual, bullet-pointed summary of the topic, emphasizing verifiable information and avoiding interpretations.
                                                    NO PREAMBLE
                                                   """
    )
    prompt_template.invoke({"data": data, "style": style})
    chain_response =  prompt_template| llm
    try:
        res = chain_response.invoke({"data": data,"style": style})
        return res.content
    
    except APIStatusError as e:
        try:
            # Attempt to parse the error details as JSON
            error_details = json.loads(e.response.text)  # Use `.text` to get the raw content
            error_code = error_details.get("error", {}).get("code")
            
            if error_code == "rate_limit_exceeded":
                st.error("Hey 👋 This is a toy project running on Rate limited APIs. the article you searched looks too large to handle. Please try something else")
            else:
                st.error("An unexpected error occurred: " + error_details.get("error", {}).get("message", "Unknown error."))
        
        except Exception:
            # Fallback for unparseable error response
            st.error("An unexpected error occurred while processing your request.")
        
        return None





