from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

SKILLS = [
    "python","machine learning","nlp","data analysis",
    "sql","docker","aws","deep learning","api development"
]

# Precompute skill embeddings
skill_embeddings = model.encode(SKILLS, convert_to_tensor=True)

def detect_ai_skills(text):

    text_embedding = model.encode(text, convert_to_tensor=True)

    scores = util.cos_sim(text_embedding, skill_embeddings)[0]

    detected = []

    for i, score in enumerate(scores):
        if score > 0.4:   # similarity threshold
            detected.append(SKILLS[i])

    return detected
