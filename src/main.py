import streamlit as st
import os
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
import tempfile
import shutil
import base64
from llama_index.readers.file import PDFReader

# Load environment variables
load_dotenv()


def run_single_model_optimization(
    documents,
    query_text: str,
    job_title: str,
    job_description: str,
    generative_model: str = "models/gemini-2.5-flash",
) -> str:
    """Run optimization using only the Generative Model's long context."""
    try:
        # Initialize Gemini
        llm = GoogleGenAI(model=generative_model, api_key=os.getenv("GEMINI_API_KEY"))

        # Extract all text from the resume documents
        resume_text = "\n".join([doc.text for doc in documents])

        # Combined Prompt: Uses the model as its own analyzer and optimizer
        full_prompt = f"""
        YOU ARE AN EXPERT CAREER COACH AND ATS SPECIALIST.
        
        INPUT DATA:
        1. RESUME CONTENT:
        {resume_text}
        
        2. TARGET JOB TITLE: {job_title}
        3. TARGET JOB DESCRIPTION:
        {job_description}
        
        USER REQUEST: {query_text}

        TASK:
        First, perform a deep analysis of the resume against the job description. 
        Then, provide a direct, structured response in this exact format:

        ## Key Findings
        • [2-3 bullet points highlighting main alignment and gaps]

        ## Specific Improvements
        • [3-5 bullet points with concrete suggestions]
        • Each bullet should start with a strong action verb
        • Include specific examples where possible

        ## Action Items
        • [2-3 specific, immediate steps to take]
        • Each item should be clear and implementable

        Keep all points concise and actionable. Do not include any thinking process or meta-commentary.
        """

        # Complete the request in one step
        response = llm.complete(full_prompt)

        return str(response)
    except Exception:
        raise


def display_pdf_preview(pdf_file):
    """Display PDF preview in the sidebar."""
    try:
        st.sidebar.subheader("Resume Preview")
        base64_pdf = base64.b64encode(pdf_file.getvalue()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
        st.sidebar.markdown(pdf_display, unsafe_allow_html=True)
        return True
    except Exception:
        st.sidebar.error(f"Error previewing PDF: {str(Exception)}")
        return False


def main():
    st.set_page_config(page_title="Resume Optimizer", layout="wide")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "docs_loaded" not in st.session_state:
        st.session_state.docs_loaded = False
    if "temp_dir" not in st.session_state:
        st.session_state.temp_dir = None
    if "current_pdf" not in st.session_state:
        st.session_state.current_pdf = None

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

                        # Verify text was extracted
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

            prompts = {
                "ATS Keyword Optimizer": "Identify and optimize ATS keywords. Focus on exact matches and semantic variations from the job description.",
                "Experience Section Enhancer": "Enhance experience section to align with job requirements. Focus on quantifiable achievements.",
                "Skills Hierarchy Creator": "Organize skills based on job requirements. Identify gaps and development opportunities.",
                "Professional Summary Crafter": "Create a targeted professional summary highlighting relevant experience and skills.",
                "Education Optimizer": "Optimize education section to emphasize relevant qualifications for this position.",
                "Technical Skills Showcase": "Organize technical skills based on job requirements. Highlight key competencies.",
                "Career Gap Framing": "Address career gaps professionally. Focus on growth and relevant experience.",
            }

            with st.spinner("Optimizing..."):
                try:
                    # Calling the single model optimization function
                    response = run_single_model_optimization(
                        st.session_state.documents,
                        prompts[optimization_type],
                        job_title,
                        job_description,
                        generative_model,
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception:
                    st.error(f"Error: {str(Exception)}")

    with col2:
        st.subheader("Optimization Results")
        for message in st.session_state.messages:
            st.markdown(message["content"])


if __name__ == "__main__":
    main()
