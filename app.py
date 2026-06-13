from flask import Flask, render_template, request
import PyPDF2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def detect_skills(text):
    skills_db = [
        "python", "html", "css", "javascript",
        "mongodb", "mysql", "flask", "java"
    ]

    found = []

    for skill in skills_db:
        if skill.lower() in text.lower():
            found.append(skill)

    return found

def calculate_score(skills):
    score = len(skills) * 10

    if score > 100:
        score = 100

    return score

def career_recommendation(skills):

    if "python" in skills:
        return "Python Developer"

    elif "html" in skills and "css" in skills:
        return "Frontend Developer"

    elif "mongodb" in skills:
        return "Full Stack Developer"

    else:
        return "Software Developer"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    text = ""

    pdf_reader = PyPDF2.PdfReader(filepath)

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    skills = detect_skills(text)

    score = calculate_score(skills)

    career = career_recommendation(skills)

    if score >= 80:
        performance = "Excellent"
    elif score >= 50:
        performance = "Good"
    else:
        performance = "Needs Improvement"

    return render_template(
        "result.html",
        skills=skills,
        score=score,
        career=career,
        performance=performance
    )

if __name__ == "__main__":
    app.run(debug=True)