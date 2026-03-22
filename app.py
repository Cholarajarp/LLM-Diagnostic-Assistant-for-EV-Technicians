import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

CHROMA_DIR = "chroma_db"
MODEL_NAME = "gpt2"

@st.cache_resource
def load_rag_pipeline():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    hf_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=150,
        max_length=None,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    prompt_template = """
    You are an expert EV Diagnostic Assistant. Use the following pieces of context from EV repair manuals to answer the technician's diagnostic query.
    If the context does not contain the answer, politely say "I cannot find the diagnostic procedure in the current manuals."
    
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

st.set_page_config(page_title="EV Diagnostic Assistant", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# Inject Global CSS to Hide Streamlit Elements (Deploy, Menu, Footer) and Modernize UI
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}

/* Global Font & Spacing Adjustments */
body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
}

/* Modernize general look */
.stTextInput > label {font-weight: bold;}
div.stButton > button:first-child {
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: bold;
    transition: all 0.3s ease;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar setup for Theme
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Electric_Car_Icon.png", width=80)
    st.title("⚡ Settings")
    
    st.markdown("---")
    st.subheader("🎨 UI Theme")
    theme_mode = st.radio("Choose Mode:", ["Light Mode", "Dark Mode"])
    
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.markdown("This assistant uses AI to help you diagnose EV issues by searching through deep technical manuals.")
    
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello Technician. What EV error code, symptom, or diagnostic procedure do you need help with today?"}
        ]
        st.rerun()

# Inject Custom CSS based on Theme selection
if theme_mode == "Dark Mode":
    dark_css = """
    <style>
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    .stSidebar {
        background-color: #1A1A1A;
        border-right: 1px solid #333;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #E0E0E0 !important;
    }
    /* Preformatted text / code blocks */
    pre, code {
        background-color: #2D2D2D !important;
        color: #E0E0E0 !important;
        border: 1px solid #444 !important;
        border-radius: 6px;
    }
    /* The bottom container block in dark mode */
    [data-testid="stBottomBlockContainer"] {
        background-color: #121212 !important;
    }
    .stChatFloatingInputContainer {
        background-color: #121212 !important;
    }
    div[data-testid="stBottom"] > div {
        background-color: #121212 !important;
    }
    div[data-testid="stBottom"] {
        background-color: #121212 !important;
    }
    /* Set the chat input wrapping components' background to dark */
    [data-testid="stChatInput"] {
        background-color: #1A1A1A !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 12px !important;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stChatInput"] * {
        background-color: transparent !important;
        color: white !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #888 !important;
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
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
    }
    .stAlert {
        background-color: #1A1A1A;
        border-left-color: #4CAF50;
        border-radius: 8px;
    }
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: #1A1A1A;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #333;
    }
    [data-testid="stExpander"] {
        background-color: #1A1A1A !important;
        border: 1px solid #333 !important;
        border-radius: 8px;
    }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    light_css = """
    <style>
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }
    .stSidebar {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    div[data-testid="stBottom"] > div {
        background-color: #F8FAFC !important;
    }
    div[data-testid="stBottom"] {
        background-color: #F8FAFC !important;
    }
    .stChatInput {
        background-color: transparent !important;
    }
    .stChatInput > div {
        background-color: #FFFFFF !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .stChatInput textarea {
        color: #1E293B !important;
        background-color: #FFFFFF !important;
    }
    div.stButton > button:first-child {
        background-color: #3B82F6;
        color: white;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #2563EB;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px;
    }
    </style>
    """
    st.markdown(light_css, unsafe_allow_html=True)

# Main Content Area Header
st.markdown("<h1 style='text-align: center; margin-bottom: 30px; font-weight: 800;'>⚡ EV Diagnostic Assistant</h1>", unsafe_allow_html=True)

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
        with st.spinner("🔍 Searching deep repair manuals..."):
            result = qa_chain.invoke({"query": prompt})
            response_text = result["result"]

            # Format the output with citations
            st.markdown(response_text)

            if result.get("source_documents"):
                st.markdown("---")
                st.markdown("📚 **Sources Cited:**")
                for i, doc in enumerate(result["source_documents"]):
                    source = doc.metadata.get("source", "Unknown")
                    page = doc.metadata.get("page", "Unknown")
                    
                    # Clean up source filename to look better
                    clean_source = source.split('/')[-1].split('\\')[-1].replace('_', ' ').replace('.pdf', '').title()
                    
                    with st.expander(f"📄 {clean_source} | Page: {page + 1}"):
                        st.markdown(f"*{doc.page_content}*")

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
