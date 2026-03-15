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
    .stBottom {
        background-color: transparent !important;
    }
    .stBottom > div {
        background-color: #121212 !important;
    }
    div[data-testid="stChatInput"] {
        background-color: #2D2D2D !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: white !important;
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
    .stBottom {
        background-color: transparent !important;
    }
    .stBottom > div {
        background-color: #F4F7F6 !important;
    }
    div[data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #007BFF !important;
        border-radius: 8px !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: black !important;
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

# Very hacky replacement just for testing
content = re.sub(r'\.stApp \{[^}]+\}.*?\.stAlert \{[^}]+\}', dark_css_replacement.strip(), content, flags=re.DOTALL)
content = re.sub(r'\.stApp \{[^\}]+\}\s*\.stChatInput \{.*?(?=</style>)', light_css_replacement.strip() + "\n    ", content, flags=re.DOTALL)

with open("app_test.py", "w") as f:
    f.write(content)
