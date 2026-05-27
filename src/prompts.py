OPTIMIZATION_SELECTION_PROMPT = {
    "ATS Keyword Optimizer": "Identify and optimize ATS keywords. Focus on exact matches and semantic variations from the job description.",
    "Experience Section Enhancer": "Enhance experience section to align with job requirements. Focus on quantifiable achievements.",
    "Skills Hierarchy Creator": "Organize skills based on job requirements. Identify gaps and development opportunities.",
    "Professional Summary Crafter": "Create a targeted professional summary highlighting relevant experience and skills.",
    "Education Optimizer": "Optimize education section to emphasize relevant qualifications for this position.",
    "Technical Skills Showcase": "Organize technical skills based on job requirements. Highlight key competencies.",
    "Career Gap Framing": "Address career gaps professionally. Focus on growth and relevant experience.",
}

READING_AGENT_PROMPT = """
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
- [2-3 bullet points highlighting main alignment and gaps]
- Break line after each bullet point

## Specific Improvements
- [3-5 bullet points with concrete suggestions]
- Each bullet should start with a strong action verb
- Include specific examples where possible
- Break line after each bullet point

## Action Items
- [2-3 specific, immediate steps to take]
- Each item should be clear and implementable
- Break line after each bullet point

Keep all points concise and actionable. Do not include any thinking process or meta-commentary.
"""

WRITING_AGENT_PROMPT_INSTRUCTIONS = """
YOU ARE AN EXPERT LATEX RESUME WRITER.

Your task is to generate a complete, optimized LaTeX resume using the Harvard template format.

INPUT DATA:
1. ORIGINAL RESUME CONTENT:
{resume_text}

2. OPTIMIZATION RECOMMENDATIONS:
{recommendations}

3. TARGET JOB TITLE: {job_title}
4. TARGET JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
- Use ONLY the following LaTeX template structure
- Fill in all sections with real content from the resume and recommendations
- Incorporate recommended keywords and improvements naturally
- Quantify achievements where possible
- Begin each bullet point with a strong action verb
- Do not use personal pronouns
- Output ONLY valid LaTeX code, nothing else, no explanation, no markdown fences
- Keep it at maximum 1 page in length
"""

WRITING_AGENT_PROMPT_TEMPLATE = r"""
\documentclass[11pt]{article}
\usepackage{graphicx}
\setlength{\parindent}{0pt}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[brazil]{babel}
\usepackage{lipsum}
\usepackage[left=1.06cm,top=1.7cm,right=1.06cm,bottom=0.49cm]{geometry}
\begin{document}
\begin{center}
    \textbf{Firstname Lastname}\\
    \hrulefill
\end{center}
\begin{center}
    Home or Campus Street Address \textbullet \ City, State Zip \textbullet \ youremail@college.harvard.edu \textbullet \ phone number
\end{center}
\vspace{0.5pt}
\begin{center}
    \textbf{Education}
\end{center}
\textbf{Harvard University} \hfill City, State

Degree, Concentration. GPA [Note: GPA is Optional] \hfill Graduation Date

Relevant Coursework: [Note: Optional]

\vspace{12pt}
\begin{center}
    \textbf{Experience}
\end{center}
\textbf{Organization} \hfill City, State (or Remote)

\textbf{Position Title} \hfill Month Year - Month Year
\begin{itemize}[noitemsep, topsep=0pt, partopsep=0pt, parsep=0pt]
    \item Beginning with your most recent position, describe your experience, skills, and resulting outcomes.
    \item Begin each line with an action verb.
    \item Quantify where possible.
    \item Do not use personal pronouns.
\end{itemize}

\vspace{12pt}
\textbf{Organization} \hfill City, State (or Remote)

\textbf{Position Title} \hfill Month Year - Month Year
\begin{itemize}[noitemsep, topsep=0pt, partopsep=0pt, parsep=0pt]
    \item Describe your experience, skills, and resulting outcomes.
    \item Begin each line with an action verb.
    \item Quantify where possible.
    \item Do not use personal pronouns.
\end{itemize}

\begin{center}
    \textbf{Skills \& Interests}
\end{center}
\textbf{Technical:} List computer software and programming languages

\textbf{Language:} List foreign languages and your level of fluency

\textbf{Interests:} List activities you enjoy that may spark interview conversation

\end{document}
"""
