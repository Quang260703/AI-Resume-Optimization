import streamlit as st
import os
from llama_index.core import SimpleDirectoryReader
import tempfile
import shutil
from llama_index.readers.file import PDFReader
from reading_agents import run_reading_agent
from writing_agents import run_writing_agent
from prompts import OPTIMIZATION_SELECTION_PROMPT


def main():
    st.set_page_config(
        page_title="Resume Optimizer", layout="wide", initial_sidebar_state="expanded"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "docs_loaded" not in st.session_state:
        st.session_state.docs_loaded = False
    if "temp_dir" not in st.session_state:
        st.session_state.temp_dir = None
    if "current_pdf" not in st.session_state:
        st.session_state.current_pdf = None
    if "optimization_done" not in st.session_state:
        st.session_state.optimization_done = False
    if "last_recommendation" not in st.session_state:
        st.session_state.last_recommendation = None
    if "latex_output" not in st.session_state:
        st.session_state.latex_output = None

    st.title("📝 Resume Optimizer")
    st.caption("Direct-Context Optimization via Gemini 2.5")

    with st.sidebar:
        generative_model = st.selectbox(
            "Generative Model",
            ["models/gemini-2.5-flash", "models/gemma-4-26b-a4b-it"],
            index=0,
        )

        st.divider()
        st.subheader("Upload Resume")
        uploaded_file = st.file_uploader("Choose your resume (PDF)", type="pdf")

        if uploaded_file is not None:
            if uploaded_file != st.session_state.current_pdf:
                st.session_state.current_pdf = uploaded_file
                try:
                    if not os.getenv("GEMINI_API_KEY"):
                        st.error("Missing Gemini API key")
                        st.stop()

                    if st.session_state.temp_dir:
                        shutil.rmtree(st.session_state.temp_dir)
                    st.session_state.temp_dir = tempfile.mkdtemp()

                    file_path = os.path.join(
                        st.session_state.temp_dir, uploaded_file.name
                    )
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    with st.spinner("Loading Resume..."):
                        loader = SimpleDirectoryReader(
                            st.session_state.temp_dir,
                            file_extractor={".pdf": PDFReader()},
                        )
                        documents = loader.load_data()

                        extracted_text = "\n".join([d.text for d in documents])
                        if not extracted_text.strip():
                            st.error(
                                "Extraction failed. Please try a different PDF format."
                            )
                        else:
                            st.session_state.docs_loaded = True
                            st.session_state.documents = documents
                            st.success(
                                f"✓ {len(documents)} pages loaded from Overleaf PDF"
                            )
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Job Information")
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description", height=200)

        st.subheader("Optimization Options")
        optimization_type = st.selectbox(
            "Select Optimization Type",
            [
                "ATS Keyword Optimizer",
                "Experience Section Enhancer",
                "Skills Hierarchy Creator",
                "Professional Summary Crafter",
                "Education Optimizer",
                "Technical Skills Showcase",
                "Career Gap Framing",
            ],
        )

        if st.button("Optimize Resume"):
            if not st.session_state.docs_loaded:
                st.error("Please upload your resume first")
                st.stop()
            if not job_title or not job_description:
                st.error("Please provide both job title and description")
                st.stop()

            with st.spinner("Optimizing..."):
                try:
                    response = run_reading_agent(
                        st.session_state.documents,
                        OPTIMIZATION_SELECTION_PROMPT[optimization_type],
                        job_title,
                        job_description,
                        generative_model,
                    )
                    st.session_state.messages.clear()
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    st.session_state.optimization_done = True
                    st.session_state.last_recommendation = response
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if st.session_state.get("optimization_done"):
            if st.button("Generate Optimized Resume"):
                if not job_title or not job_description:
                    st.error("Please provide both job title and description")
                    st.stop()
                with st.spinner("Generating LaTeX resume..."):
                    try:
                        latex_output = run_writing_agent(
                            st.session_state.documents,
                            st.session_state.last_recommendation,
                            job_title,
                            job_description,
                            generative_model,
                        )
                        st.session_state.latex_output = latex_output
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    with col2:
        st.subheader("Optimization Results")
        for message in st.session_state.messages:
            st.markdown(message["content"])

        if st.session_state.get("latex_output"):
            st.divider()
            st.subheader("Generated Resume")
            st.download_button(
                label="⬇️ Download .tex file",
                data=st.session_state.latex_output,
                file_name="optimized_resume.tex",
                mime="text/plain",
            )
            st.info(
                "📋 Paste the LaTeX code below into [Overleaf](https://www.overleaf.com) to compile your PDF for free."
            )
            st.code(st.session_state.latex_output, language="latex")


if __name__ == "__main__":
    main()
