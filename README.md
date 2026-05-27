# 📝 Resume Optimizer
 
An AI-powered resume optimization tool built with Streamlit and Google Gemini. Upload your resume, provide a job description, and get tailored optimization recommendations along with a generated LaTeX resume.
 
## Features
 
- **PDF Resume Upload** — extracts text from your resume automatically
- **7 Optimization Types** — ATS keywords, experience, skills, summary, education, technical skills, and career gap framing
- **AI-Powered Analysis** — uses Google Gemini 2.5 Flash to analyze your resume against the job description
- **LaTeX Resume Generation** — generates an optimized resume in Harvard template format
- **Overleaf Ready** — download the `.tex` file and compile on Overleaf for free
## Project Structure
 
```
resume-optimizer/
├── src/
│   ├── main.py              # Streamlit app entry point
│   ├── reading_agents.py    # Resume analysis agent
│   ├── writing_agents.py    # LaTeX resume generation agent
│   └── prompts.py           # All prompt templates
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
 
## Prerequisites
 
- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
## Setup
 
### Local
 
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cicd-project.git
   cd cicd-project
   ```
 
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
 
3. Create a `.env` file in the `src/` directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
 
4. Run the app:
   ```bash
   cd src
   streamlit run main.py
   ```
 
### Docker
 
1. Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
 
2. Build and run:
   ```bash
   docker compose up --build
   ```
 
3. Open [http://localhost:8501](http://localhost:8501)
## Usage
 
1. Select a Gemini model from the sidebar
2. Upload your resume (PDF)
3. Enter the job title and description
4. Select an optimization type
5. Click **Optimize Resume** to get recommendations
6. Click **Generate Optimized Resume** to get a LaTeX resume
7. Download the `.tex` file and paste into [Overleaf](https://www.overleaf.com) to export as PDF
## Environment Variables
 
| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key |
 
## Models Supported
 
- `models/gemini-2.5-flash` (recommended)
- `models/gemma-4-26b-a4b-it`