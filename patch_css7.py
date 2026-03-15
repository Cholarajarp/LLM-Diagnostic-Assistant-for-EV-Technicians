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
    /* Transparent backgrounds everywhere in the bottom fixed element */
    [data-testid="stBottomBlockContainer"] {
        background-color: #121212 !important;
    }
    [data-testid="stBottom"] > div {
        background-color: #121212 !important;
    }
    .stChatInput {
        background-color: #121212 !important;
    }
    /* Actual input text area wrapping box */
    [data-testid="stChatInput"] {
        background-color: #2D2D2D !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
    }
    textarea {
        color: white !important;
        background-color: #2D2D2D !important;
    }
    /* Send button */
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
    /* Transparent backgrounds everywhere in the bottom fixed element */
    [data-testid="stBottomBlockContainer"] {
        background-color: #F4F7F6 !important;
    }
    [data-testid="stBottom"] > div {
        background-color: #F4F7F6 !important;
    }
    .stChatInput {
        background-color: #F4F7F6 !important;
    }
    /* Actual input text area wrapping box */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #007BFF !important;
        border-radius: 8px !important;
    }
    textarea {
        color: black !important;
        background-color: #FFFFFF !important;
    }
    /* Send button */
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3;
    }
"""

content = re.sub(r'\.stApp \{[^}]+\}.*?\.stAlert \{[^}]+\}', dark_css_replacement.strip(), content, flags=re.DOTALL)
content = re.sub(r'\.stApp \{[^\}]+\}\s*\[data-testid="stBottom"\].*?(?=</style>)', light_css_replacement.strip() + "\n    ", content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
