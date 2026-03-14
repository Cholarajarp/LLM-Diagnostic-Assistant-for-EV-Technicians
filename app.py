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

# Sidebar setup for Architecture and Dark/Light Mode
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Electric_Car_Icon.png", width=80)
    st.title("Settings & Info")

    st.subheader("UI Theme")
    theme_mode = st.radio("Choose Mode:", ["Light Mode", "Dark Mode"])

    st.subheader("RAG Architecture")
    st.markdown("""
    **Pipeline Flow:**
    1. **PDFs** (EV Manuals)
    2. **Langchain** (PyPDFLoader & TextSplitter)
    3. **HuggingFace** (`all-MiniLM-L6-v2`)
    4. **ChromaDB** (Local Vector Store)
    5. **Retriever** (Top-K Similarity Search)
    6. **LLM** (`GPT-2` text-generation)
    7. **Streamlit UI** (Response & Citations)
    """)

# Inject Custom CSS based on Theme
if theme_mode == "Dark Mode":
    dark_css = """
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    .stSidebar {
        background-color: #2D2D2D;
    }
    h1, h2, h3, h4, h5, h6, p, div {
        color: #E0E0E0 !important;
    }
    .stTextInput > div > div > input {
        background-color: #333333;
        color: white;
    }
    div[data-baseweb="button"] > button {
        background-color: #4CAF50;
        color: white;
    }
    .stAlert {
        background-color: #333333;
    }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    light_css = """
    <style>
    .stApp {
        background-color: #F8F9FA;
        color: #1E1E1E;
    }
    div[data-baseweb="button"] > button {
        background-color: #007BFF;
        color: white;
    }
    </style>
    """
    st.markdown(light_css, unsafe_allow_html=True)

# Main Content Area
col1, col2 = st.columns([1, 8])
with col1:
    st.title("⚡")
with col2:
    st.title("EV Technician Diagnostic Assistant")

st.markdown("---")
st.markdown("### Ask questions about EV error codes, diagnostic procedures, or repair steps.")

qa_chain = load_rag_pipeline()

query = st.text_input("Enter your diagnostic query (e.g., 'How to check Inverter resistance?' or 'BMS_a066'):", key="query_input")

if st.button("Get Diagnosis"):
    if query:
        with st.spinner("Searching deep repair manuals..."):
            result = qa_chain.invoke({"query": query})

            st.subheader("Diagnostic Response:")
            st.info(result["result"])

            st.subheader("Sources Cited:")
            for doc in result["source_documents"]:
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "Unknown")
                st.markdown(f"- **File:** `{source}` | **Page:** `{page}`")
                with st.expander(f"View Context Snippet from Page {page}"):
                    st.write(doc.page_content)
    else:
        st.warning("Please enter a query.")
