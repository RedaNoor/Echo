import streamlit as st
import google.generativeai as genai

# Adding title
st.title("Chatbot using Gemini API")

# Set up your Gemini AI API key
client = genai.configure(api_key=st.secrets["Api_key"])

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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Start a chat session if not already started
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    chat_session = st.session_state.chat_session

    # Send message to the chat session
    response = chat_session.send_message(prompt)
    
    # Update chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    # Display the new messages
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)
