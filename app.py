from flask import Flask, request, render_template, jsonify
import pdfplumber
import google.generativeai as genai
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


skills_db = {
    'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Python', 'Django'],
    'Data Scientist': ['Python', 'R', 'Machine Learning', 'SQL', 'Pandas', 'NumPy'],
    'Software Engineer': ['Java', 'C++', 'Python', 'Algorithms', 'Data Structures', 'Git'],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('resume')
    role = request.form.get('role')
    
    if not file or not role:
        return jsonify({'error': 'Invalid input: missing file or role'})
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'})
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        with pdfplumber.open(filepath) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
    except Exception as e:
        return jsonify({'error': f'Error extracting text from PDF: {str(e)}'})
    
    role_skills = skills_db.get(role, [])
    if not role_skills:
        return jsonify({'error': f'No skills defined for role: {role}'})
    
    text_lower = text.lower()
    matched = [skill for skill in role_skills if skill.lower() in text_lower]
    score = (len(matched) / len(role_skills)) * 100
    missing = [skill for skill in role_skills if skill not in matched]
    
    if GOOGLE_API_KEY:
        try:
            model = genai.GenerativeModel('gemini-flash-lite-latest')
            
            prompt = f"""You are a senior industry expert. Generate a response in exactly 5 concise lines for the {role} position. 
                        Use confident, impactful language. Based on my matched skills ({', '.join(matched)}) and missing skills ({', '.join(missing)}), 
                        explain my readiness for the role, what skills I must strengthen, which critical skills I must learn next, and 
                        how to present these effectively on my resume. Do not use bullet points or headings."""
            response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(
                max_output_tokens=500,
                temperature=0.7
            ))
            suggestions_text = response.text.strip()
                
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "rate limit" in error_msg:
                suggestions_text = "❌ Google Gemini API rate limit exceeded. Free tier allows 60 requests/minute. Please wait and try again."
            elif "api key" in error_msg:
                suggestions_text = "❌ Google API key not found. Please set the GOOGLE_API_KEY environment variable."
            else:
                suggestions_text = f"❌ AI suggestion error: {str(e)}"
    else:
        suggestions_text = "❌ Google API key not configured. Please set GOOGLE_API_KEY environment variable."
    
    os.remove(filepath)
    
    return jsonify({
        'score': round(score, 2),
        'matched': matched,
        'missing' : missing,
        'suggestions': suggestions_text
    })

if __name__ == '__main__':
    app.run(debug=True)