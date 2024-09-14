import streamlit as st
import google.generativeai as genai
from PIL import Image

# Adding title and logo
# Create two columns
col1, col2 = st.columns([1, 8])
# Display the logo in the first column
with col1:
    st.image('static/images/logo.png', width=50, use_column_width='auto')
st.markdown('<style>img { border-radius: 50%; }</style>', unsafe_allow_html=True)

# Display the title in the second column
with col2:
    st.title('Echo')

st.write('I am a chatbot Created by **RIDA NOOR** to help you with your queries.')
st.write('Ask me anything!')

# Set up your Gemini AI APuI key
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
    st.session_state.messages = [
        {"role": "user", "content": "what is your name?, whats your name?, what are you called?, what do they call you?, what is your name, What is your name?, Whats your name" },
        {"role": "assistant", "content": "I am named as ECHO."}
    ]

# Load custom icons
user_icon = Image.open("static/images/user3.png")
bot_icon = Image.open("static/images/logo.png")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar=user_icon):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar=bot_icon):
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
    with st.chat_message("user", avatar=user_icon):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=bot_icon):
        st.markdown(response.text)
