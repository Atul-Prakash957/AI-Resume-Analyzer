import re


def load_skills():
    with open("DATA/skill_list.txt", "r", encoding="utf-8") as f:
        skills = [line.strip().lower() for line in f if line.strip()]
    return skills


def normalize_text(text):
    text = text.lower()

    normalization_dict = {
        # Programming
        r"\bpy\b": "python",
        r"\bpython3\b": "python",
        r"\bjs\b": "javascript",
        r"\bts\b": "typescript",
        r"\bgolang\b": "go",
        r"\bcpp\b": "c++",
        r"\bc\s*sharp\b": "c#",
        r"\bpy3\b": "python",
        r"\breact js\b": "react",
        r"\bnodejs\b": "nodejs",
        r"\bexpress js\b": "expressjs",
        r"\bnext js\b": "nextjs",
        r"\bmongo db\b": "mongodb",
        r"\bpostgre\b": "postgresql",
        r"\bpower bi\b": "power bi",
        r"\bexcel\b": "excel",
        # AI/ML
        r"\bml\b": "machine learning",
        r"\bdl\b": "deep learning",
        r"\bai\b": "artificial intelligence",
        r"\bnlp\b": "natural language processing",
        r"\bcv\b": "computer vision",
        r"\brl\b": "reinforcement learning",

        # Data
        r"\bds\b": "data science",
        r"\beda\b": "data analysis",
        r"\bstats\b": "statistics",

        # Libraries
        r"\bsklearn\b": "scikit-learn",
        r"\bscikit learn\b": "scikit-learn",
        r"\btf\b": "tensorflow",
        r"\btorch\b": "pytorch",

        # Cloud
        r"\baws cloud\b": "aws",
        r"\bamazon cloud\b": "aws",
        r"\bgcp cloud\b": "google cloud",
        r"\bgoogle cloud platform\b": "google cloud",
        r"\bazure cloud\b": "azure",

        # Frameworks
        r"\breact\.js\b": "react",
        r"\breactjs\b": "react",
        r"\bnode\.js\b": "nodejs",
        r"\bnode js\b": "nodejs",
        r"\bvue\.js\b": "vue",
        r"\bnext\.js\b": "nextjs",
        r"\bexpress\.js\b": "express",

        # Databases
        r"\bpostgres\b": "postgresql",
        r"\bmongo\b": "mongodb",
        r"\bms sql\b": "sql",

        # DevOps
        r"\bk8s\b": "kubernetes",
        r"\bci/cd\b": "devops",
        r"\bci cd\b": "devops",

        # Tools
        r"\bpowerbi\b": "power bi",
        r"\bms excel\b": "excel",

        # APIs
        r"\brestful api\b": "rest api",

        # OOP
        r"\bobject oriented programming\b": "oop",

        # Systems
        r"\bdistributed system\b": "distributed systems",
    }

    for pattern, replacement in normalization_dict.items():
        text = re.sub(pattern, replacement, text)

    return text


def clean_text(text):
    """
    Keep + and # for c++ and c#
    """
    text = re.sub(r"[^a-zA-Z0-9+#\s]", " ", text)
    return text


def extract_skills(text):
    text = normalize_text(text)
    text = clean_text(text)

    skill_list = load_skills()

    extracted_skills = set()

    for skill in skill_list:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            extracted_skills.add(skill)

    return list(extracted_skills)