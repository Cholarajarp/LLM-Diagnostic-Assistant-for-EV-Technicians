import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

CHROMA_DIR = "chroma_db"
MODEL_NAME = "gpt2"

@st.cache_resource
def load_rag_pipeline():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 2})

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    hf_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    prompt_template = """
    Use the following pieces of context from EV repair manuals to answer the technician's diagnostic query.
    If the context does not contain the answer, say "I cannot find the diagnostic procedure in the current manuals."

    Context:
    {context}

    Technician Query: {question}

    Answer (Please include the source file and page number from the context):
    """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa_chain

st.set_page_config(page_title="EV Diagnostic Assistant", page_icon="⚡", layout="wide")

# Inject Global CSS to Hide Streamlit Elements (Deploy, Menu, Footer) and Modernize UI
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
/* Modernize general look */
.stTextInput > label {font-weight: bold;}
div.stButton > button:first-child {
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: bold;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar setup for Theme
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Electric_Car_Icon.png", width=80)
    st.title("Settings")

    st.markdown("---")
    st.subheader("UI Theme")
    theme_mode = st.radio("Choose Mode:", ["Light Mode", "Dark Mode"])

# Inject Custom CSS based on Theme selection
if theme_mode == "Dark Mode":
    dark_css = """
    <style>
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
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        color: white;
        border: 1px solid #4CAF50;
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
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    light_css = """
    <style>
    .stApp {
        background-color: #F4F7F6;
        color: #1E1E1E;
    }
    .stTextInput > div > div > input {
        border: 1px solid #007BFF;
    }
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3;
    }
    </style>
    """
    st.markdown(light_css, unsafe_allow_html=True)

# Main Content Area Header
st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>⚡ EV Diagnostic Assistant</h1>", unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello Technician. What EV error code, symptom, or diagnostic procedure do you need help with today?"}
    ]

# Display Chat History
for message in st.session_state.messages:
    avatar = "🛠️" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Load Pipeline
qa_chain = load_rag_pipeline()

# React to User Input
if prompt := st.chat_input("Ask about EV errors (e.g., 'BMS_a066' or 'How to check Inverter resistance?')"):
    # Display user message in chat message container
    st.chat_message("user", avatar="🛠️").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Searching deep repair manuals..."):
            result = qa_chain.invoke({"query": prompt})
            response_text = result["result"]

            # Format the output with citations
            st.markdown(response_text)

            if result.get("source_documents"):
                st.markdown("---")
                st.markdown("**Sources Cited:**")
                for doc in result["source_documents"]:
                    source = doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("page", "Unknown")
                    st.caption(f"File: `{source}` | Page: `{page}`")
                    with st.expander(f"View Context from {source}"):
                        st.markdown(f"*{doc.page_content}*")

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
