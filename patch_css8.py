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
    /* The bottom container block in dark mode */
    [data-testid="stBottomBlockContainer"] {
        background-color: #121212 !important;
    }
    .stChatFloatingInputContainer {
        background-color: #121212 !important;
    }
    /* Set the chat input wrapping components' background to dark */
    [data-testid="stChatInput"] {
        background-color: #2D2D2D !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
        color: white !important;
    }
    [data-testid="stChatInput"] * {
        background-color: transparent !important;
        color: white !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #B0B0B0 !important;
    }
    /* Ensure no white background escapes */
    .stChatInputContainer {
        background-color: #121212 !important;
    }
    /* Send button */
    div.stButton > button:first-child {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049 !important;
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
    /* The bottom container block in light mode */
    [data-testid="stBottomBlockContainer"] {
        background-color: #F4F7F6 !important;
    }
    .stChatFloatingInputContainer {
        background-color: #F4F7F6 !important;
    }
    /* Set the chat input wrapping components' background to light */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #007BFF !important;
        border-radius: 8px !important;
        color: black !important;
    }
    [data-testid="stChatInput"] * {
        background-color: transparent !important;
        color: black !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #606060 !important;
    }
    /* Ensure no wrong background escapes */
    .stChatInputContainer {
        background-color: #F4F7F6 !important;
    }
    /* Send button */
    div.stButton > button:first-child {
        background-color: #007BFF !important;
        color: white !important;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3 !important;
    }
"""

content = re.sub(r'\.stApp \{[^}]+\}.*?\.stAlert \{[^}]+\}', dark_css_replacement.strip(), content, flags=re.DOTALL)
content = re.sub(r'\.stApp \{[^\}]+\}\s*\[data-testid="stBottomBlockContainer"\].*?(?=</style>)', light_css_replacement.strip() + "\n    ", content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
