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
        max_new_tokens=256,
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

st.set_page_config(page_title="EV Diagnostic Assistant", page_icon="⚡", layout="centered")

st.title("⚡ EV Technician Diagnostic Assistant")
st.markdown("Ask questions about EV error codes, diagnostic procedures, or repair steps.")

qa_chain = load_rag_pipeline()

query = st.text_input("Enter your diagnostic query (e.g., 'What to do for High Voltage Battery Temperature High?'):")

if st.button("Get Diagnosis"):
    if query:
        with st.spinner("Searching repair manuals..."):
            result = qa_chain.invoke({"query": query})

            st.subheader("Diagnostic Response:")
            st.write(result["result"])

            st.subheader("Sources Cited:")
            for doc in result["source_documents"]:
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "Unknown")
                st.markdown(f"- **File:** {source} | **Page:** {page}")
                with st.expander("View Context Snippet"):
                    st.write(doc.page_content)
    else:
        st.warning("Please enter a query.")
