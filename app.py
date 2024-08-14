import streamlit as st
import google.generativeai as genai  # Assuming gemini_ai is the library for Gemini AI

# Adding title
st.title('Chatbot')

# Set up your Gemini AI API key
genai.configure(api_key = st.secrets["Api_key"])

#genai.configure(api_key='AIzaSyBw902ueMsy1kqZiZHPWQ4Ir85JmF4z9KY')

# Define generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# Start a chat session
chat_session = model.start_chat(
    history=[]
)

st.write('Welcome to the chatbot! Please do ask your question and I will try to answer it.')

question = st.text_input('Ask a question:', key='unique_key')

if question:
    response = chat_session.send_message(question)
    st.write(response.text)
