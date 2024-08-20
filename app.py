import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import google.generativeai as genai

# Set up your Gemini AI API key
client = genai.configure(api_key="AIzaSyBw902ueMsy1kqZiZHPWQ4Ir85JmF4z9KY")

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

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Echo'),
    dcc.Input(id='user-input', type='text', placeholder='What is up?', style={'width': '100%'}),
    html.Button('Send', id='send-button', n_clicks=0),
    html.Div(id='chat-history', children=[])
])

@app.callback(
    Output('chat-history', 'children'),
    Input('send-button', 'n_clicks'),
    State('user-input', 'value'),
    State('chat-history', 'children')
)
def update_chat(n_clicks, prompt, chat_history):
    if not prompt:
        return chat_history

    # Check if the user is asking for the chatbot's name
    if prompt.lower() in ["what is your name?", "who are you?", "what's your name?", "what is your name", "who are you", "what's your name", "do you have a name"]:
        response_text = "Hi, my name is Echo AI. How may I assist you today?"
    else:
        # Start a chat session if not already started
        if 'chat_session' not in app.server.config:
            app.server.config['chat_session'] = model.start_chat(history=[])

        chat_session = app.server.config['chat_session']

        # Send message to the chat session
        response = chat_session.send_message(prompt)
        response_text = response.text

    # Update chat history
    chat_history.append(html.Div([
        html.Div(f"User: {prompt}", style={'font-weight': 'bold'}),
        html.Div(f"Assistant: {response_text}")
    ]))

    return chat_history

if __name__ == '__main__':
    app.run_server(debug=True)