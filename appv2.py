import wikipedia
import streamlit as st

def search_and_fetch(query):
    title = None
    page_content = None
    
    try:
        # Try to fetch the page from Wikipedia
        page = wikipedia.page(query)
        title = page.title
        page_content = page.content
        
    except wikipedia.DisambiguationError as e:
        st.error(f"Please be more specific. Did you mean one of these: {e.options}")
    
    except wikipedia.PageError:
        st.error("Page not found.")
    
    # Return None if no content was found
    if title and page_content:
        return title, page_content
    else:
        return None, None
