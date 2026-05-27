import os
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
from .prompts import READING_AGENT_PROMPT

# Load environment variables
load_dotenv()


def run_reading_agent(
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
        full_prompt = READING_AGENT_PROMPT.format(
            resume_text=resume_text,
            job_title=job_title,
            job_description=job_description,
            query_text=query_text,
        )

        # Complete the request in one step
        response = llm.complete(full_prompt)

        return str(response)
    except Exception:
        raise
