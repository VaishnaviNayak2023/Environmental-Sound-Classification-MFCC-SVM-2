import numpy as np
import random


def hill_climbing(feature, candidates, max_restarts=5):
    """
    Hill climbing with random restarts.

    Starting from a randomly chosen class, the algorithm iteratively
    moves to a neighbouring class that is closer (lower Euclidean
    distance) to the query feature vector.  Random restarts reduce the
    risk of getting trapped at a local optimum.

    Args:
        feature      : 1-D numpy array — the query feature vector.
        candidates   : dict {label: [vec1, vec2, ...]} — per-class prototype vectors.
        max_restarts : number of random restarts (default 5).

    Returns:
        The label of the best-matching class found.
    """
    labels = list(candidates.keys())

    def best_score_for(label):
        return min(np.linalg.norm(feature - v) for v in candidates[label])

    best_overall_class = None
    best_overall_score = float("inf")

    for _ in range(max_restarts):
        # --- Random start ---
        current_label = random.choice(labels)
        current_score = best_score_for(current_label)

        # --- Climb until no neighbour improves the score ---
        improved = True
        while improved:
            improved = False
            for neighbor_label in labels:
                if neighbor_label == current_label:
                    continue
                neighbor_score = best_score_for(neighbor_label)
                if neighbor_score < current_score:
                    current_score = neighbor_score
                    current_label = neighbor_label
                    improved = True

        # --- Keep best result across restarts ---
        if current_score < best_overall_score:
            best_overall_score = current_score
            best_overall_class = current_label

    return best_overall_class