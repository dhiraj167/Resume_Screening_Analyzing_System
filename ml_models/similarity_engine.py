"""
Similarity Engine: Computes cosine similarity between resume and job embeddings.
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(embedding1: list, embedding2: list) -> float:
    """
    Compute cosine similarity between two embeddings.
    Returns a score from 0 to 100.
    """
    if not embedding1 or not embedding2:
        return 0.0
    vec1 = np.array(embedding1).reshape(1, -1)
    vec2 = np.array(embedding2).reshape(1, -1)
    score = cosine_similarity(vec1, vec2)[0][0]
    return round(float(score) * 100, 2)


def rank_candidates(job_embedding: list, candidate_embeddings: list) -> list:
    """
    Rank candidates by similarity to a job embedding.
    Returns indices in descending order of similarity.
    """
    if not job_embedding or not candidate_embeddings:
        return []
    job_vec = np.array(job_embedding).reshape(1, -1)
    candidate_matrix = np.array(candidate_embeddings)
    scores = cosine_similarity(job_vec, candidate_matrix)[0]
    ranked_indices = np.argsort(scores)[::-1].tolist()
    ranked_scores = [round(float(scores[i]) * 100, 2) for i in ranked_indices]
    return list(zip(ranked_indices, ranked_scores))


def find_skill_gap(resume_skills: list, required_skills: list) -> dict:
    """
    Compare resume skills to job-required skills.
    Returns matched and missing skill lists.
    """
    resume_lower = [s.lower().strip() for s in resume_skills]
    required_lower = [s.lower().strip() for s in required_skills]
    matched = [s for s in required_lower if s in resume_lower]
    missing = [s for s in required_lower if s not in resume_lower]
    return {
        'matched': matched,
        'missing': missing,
        'match_percentage': round(len(matched) / len(required_lower) * 100, 2) if required_lower else 0.0
    }
