import numpy as np

def heuristic(a, b):
    return np.linalg.norm(a - b)

def best_first_search(feature, class_vectors):
    best_class = None
    best_score = float("inf")
    for label, vectors in class_vectors.items():
        for vec in vectors:
            score = heuristic(feature, vec)
            if score < best_score:
                best_score = score
                best_class = label
    return best_class