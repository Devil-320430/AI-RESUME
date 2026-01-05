# AI Resume Checker

A web application that analyzes resumes for ATS-friendliness, checks for missing skills based on job roles, and provides AI-powered improvement suggestions.

## Features

- Upload PDF resumes
- Select job roles (Web Developer, Data Scientist, Software Engineer)
- Extract text from PDFs
- Match skills against job requirements
- Calculate ATS compatibility score (0-100)
- Identify missing skills
- Generate AI-powered improvement suggestions

## Requirements

- Python 3.7+
- Google Gemini API key (free tier available)

## Installation

1. Clone or download the project files.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your Google Gemini API key as an environment variable:
   ```
   export GOOGLE_API_KEY='your-gemini-api-key-here'
   ```
   Get a free API key from: https://makersuite.google.com/app/apikey

## Usage

1. Set your Google Gemini API key (get one from https://makersuite.google.com/app/apikey):
   ```
   export GOOGLE_API_KEY='your-gemini-api-key-here'
   ```
2. Run the application:
   ```
   "/YOUR PATH/.venv/bin/python" app.py
   ```
3. Open your browser and go to `http://127.0.0.1:5000/`
4. Upload a PDF resume and select a job role.
5. Click "Analyze Resume" to get results.

## How It Works

1. **Text Extraction**: Uses pdfplumber to extract text from uploaded PDFs.
2. **Skill Matching**: Compares extracted text against predefined skills for the selected job role.
3. **Scoring**: Calculates a score based on the percentage of matched skills.
4. **AI Suggestions**: Uses Google's Gemini AI (free tier) to generate personalized improvement suggestions based on your resume analysis.

## Customization

- Add more job roles and skills in `app.py` under `skills_db`.
- Modify the AI prompt in the `analyze` function for different suggestion styles.

## Note

If OpenAI API key is not set, the application will still work but will show a message instead of AI-generated suggestions.