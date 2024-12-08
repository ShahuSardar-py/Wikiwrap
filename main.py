import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser 
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
import wikipedia
from app import get_response
from appv2 import search_and_fetch


st.set_page_config(
    page_icon='🤖',
    page_title="WikiAI"
)

user_input= st.text_input("Search WikiAI")
content_style = st.selectbox(
    "I need summary for:",
    ["For presentations", "General Knowledge & Understanding", "Fact-Checking"]
)
submit= st.button("Search & Summarize")


if submit:
    if user_input:
        content = search_and_fetch(user_input)
        if content:
            # Generate summary using the selected style
            title, page_content = content
            summary = get_response(page_content, content_style)
            st.subheader(f"AI Summary for {content_style} on {title}")
            st.write(summary)
    else:
        st.error("Please enter a keyword.")



