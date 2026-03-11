from sentence_transformers import SentenceTransformer, util

# Load AI model once (very important)
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(resume_text, job_text):

    # Convert text into embeddings (AI vectors)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    # Compute cosine similarity
    similarity_score = util.cos_sim(resume_embedding, job_embedding)

    score = round(float(similarity_score[0][0]) * 100, 2)

    return score
