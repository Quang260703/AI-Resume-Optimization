import os
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
from .prompts import WRITING_AGENT_PROMPT_INSTRUCTIONS, WRITING_AGENT_PROMPT_TEMPLATE

load_dotenv()


def run_writing_agent(
    documents,
    recommendations: str,
    job_title: str,
    job_description: str,
    generative_model: str = "models/gemini-2.5-flash",
) -> str:
    """Generate an optimized LaTeX CV from resume content and recommendations."""
    try:
        llm = GoogleGenAI(model=generative_model, api_key=os.getenv("GEMINI_API_KEY"))

        resume_text = "\n".join([doc.text for doc in documents])

        full_prompt = (
            WRITING_AGENT_PROMPT_INSTRUCTIONS.format(
                resume_text=resume_text,
                recommendations=recommendations,
                job_title=job_title,
                job_description=job_description,
            )
            + WRITING_AGENT_PROMPT_TEMPLATE
        )

        response = llm.complete(full_prompt)
        return str(response)

    except Exception:
        raise
