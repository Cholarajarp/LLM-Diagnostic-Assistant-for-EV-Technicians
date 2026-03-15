import re

with open("app.py", "r") as f:
    content = f.read()

dark_css_replacement = """
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    .stSidebar {
        background-color: #1E1E1E;
    }
    h1, h2, h3, h4, h5, h6, p, div {
        color: #E0E0E0 !important;
    }
    /* The main bottom container */
    div[data-testid="stBottom"] > div {
        background-color: #121212 !important;
    }
    div[data-testid="stBottom"] {
        background-color: #121212 !important;
    }
    /* The chat input container */
    .stChatInput {
        background-color: #121212 !important;
    }
    /* The inner box of the chat input */
    .stChatInput > div {
        background-color: #2D2D2D !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
    }
    .stChatInput textarea {
        color: white !important;
        background-color: #2D2D2D !important;
    }
    /* Hide the send button background so it blends */
    .stChatInput button {
        background-color: transparent !important;
    }
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049;
    }
    .stAlert {
        background-color: #2D2D2D;
        border-left-color: #4CAF50;
    }
"""

light_css_replacement = """
    .stApp {
        background-color: #F4F7F6;
        color: #1E1E1E;
    }
    div[data-testid="stBottom"] > div {
        background-color: #F4F7F6 !important;
    }
    div[data-testid="stBottom"] {
        background-color: #F4F7F6 !important;
    }
    .stChatInput {
        background-color: #F4F7F6 !important;
    }
    .stChatInput > div {
        background-color: #FFFFFF !important;
        border: 1px solid #007BFF !important;
        border-radius: 8px !important;
    }
    .stChatInput textarea {
        color: black !important;
        background-color: #FFFFFF !important;
    }
    .stChatInput button {
        background-color: transparent !important;
    }
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3;
    }
"""

# Hard reset by reading from a backup or writing explicitly
