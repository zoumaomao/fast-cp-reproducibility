from __future__ import annotations

import numpy as np


def inverse_probability_scores(probs: np.ndarray, y: np.ndarray) -> np.ndarray:
    return 1.0 - probs[np.arange(y.size), y]


def conformal_threshold(scores: np.ndarray, alpha: float) -> float:
    scores = np.asarray(scores, dtype=np.float64)
    if scores.size == 0:
        raise ValueError("Cannot compute conformal threshold with no calibration scores.")
    q = np.ceil((scores.size + 1) * (1.0 - alpha)) / scores.size
    q = min(1.0, float(q))
    return float(np.quantile(scores, q, method="higher"))


def prediction_sets_from_threshold(probs: np.ndarray, threshold: float) -> np.ndarray:
    return (1.0 - probs) <= threshold


def aps_scores(probs: np.ndarray, y: np.ndarray, raps_lambda: float = 0.0, raps_k: int = 0) -> np.ndarray:
    """Adaptive prediction set scores; RAPS is APS plus a rank penalty."""
    probs = np.asarray(probs, dtype=np.float64)
    y = np.asarray(y)
    order = np.argsort(-probs, axis=1)
    sorted_probs = np.take_along_axis(probs, order, axis=1)
    cumulative = np.cumsum(sorted_probs, axis=1)
    inverse_rank = np.empty_like(order)
    inverse_rank[np.arange(order.shape[0])[:, None], order] = np.arange(order.shape[1])[None, :]
    ranks = inverse_rank[np.arange(y.size), y]
    penalties = raps_lambda * np.maximum(ranks + 1 - raps_k, 0)
    return cumulative[np.arange(y.size), ranks] + penalties


def aps_prediction_sets(
    probs: np.ndarray,
    threshold: float,
    raps_lambda: float = 0.0,
    raps_k: int = 0,
) -> np.ndarray:
    probs = np.asarray(probs, dtype=np.float64)
    order = np.argsort(-probs, axis=1)
    sorted_probs = np.take_along_axis(probs, order, axis=1)
    cumulative = np.cumsum(sorted_probs, axis=1)
    ranks = np.arange(probs.shape[1], dtype=np.float64)[None, :]
    sorted_scores = cumulative + raps_lambda * np.maximum(ranks + 1 - raps_k, 0)
    sorted_sets = sorted_scores <= threshold
    sets = np.zeros_like(sorted_sets, dtype=bool)
    sets[np.arange(probs.shape[0])[:, None], order] = sorted_sets
    return sets


def mondrian_prediction_sets(
    calib_scores: np.ndarray,
    calib_groups: np.ndarray,
    test_probs: np.ndarray,
    test_group: str,
    alpha: float,
    fallback_threshold: float | None = None,
) -> np.ndarray:
    calib_groups = np.asarray(calib_groups)
    mask = calib_groups == test_group
    if np.any(mask):
        threshold = conformal_threshold(calib_scores[mask], alpha)
    elif fallback_threshold is not None:
        threshold = fallback_threshold
    else:
        threshold = conformal_threshold(calib_scores, alpha)
    return prediction_sets_from_threshold(test_probs, threshold)


def weighted_threshold(scores: np.ndarray, weights: np.ndarray, alpha: float) -> float:
    scores = np.asarray(scores, dtype=np.float64)
    weights = np.asarray(weights, dtype=np.float64)
    weights = np.maximum(weights, 1e-12)
    order = np.argsort(scores)
    scores_sorted = scores[order]
    weights_sorted = weights[order]
    cumulative = np.cumsum(weights_sorted) / np.sum(weights_sorted)
    idx = np.searchsorted(cumulative, 1.0 - alpha, side="left")
    idx = min(idx, scores_sorted.size - 1)
    return float(scores_sorted[idx])


def weighted_prediction_sets(
    calib_scores: np.ndarray,
    calib_fingerprints: np.ndarray,
    test_probs: np.ndarray,
    test_fingerprints: np.ndarray,
    alpha: float,
    bandwidth: float | None = None,
    global_threshold: float | None = None,
    global_mix: float = 0.0,
) -> np.ndarray:
    calib_z, test_z = _standardize(calib_fingerprints, test_fingerprints)
    if bandwidth is None:
        bandwidth = _median_bandwidth(calib_z)
    bandwidth = max(float(bandwidth), 1e-6)

    sets = np.zeros_like(test_probs, dtype=bool)
    for i, fp in enumerate(test_z):
        dist2 = np.sum((calib_z - fp) ** 2, axis=1)
        weights = np.exp(-dist2 / (2.0 * bandwidth * bandwidth))
        threshold = weighted_threshold(calib_scores, weights, alpha)
        if global_threshold is not None and global_mix > 0.0:
            threshold = (1.0 - global_mix) * threshold + global_mix * global_threshold
        sets[i] = (1.0 - test_probs[i]) <= threshold
    return sets


def metrics(prediction_sets: np.ndarray, y: np.ndarray, probs: np.ndarray) -> dict[str, float]:
    contains = prediction_sets[np.arange(y.size), y]
    sizes = prediction_sets.sum(axis=1)
    top1 = np.argmax(probs, axis=1)
    singleton = sizes == 1
    singleton_correct = (top1 == y) & singleton
    return {
        "coverage": float(np.mean(contains)),
        "avg_set_size": float(np.mean(sizes)),
        "singleton_rate": float(np.mean(singleton)),
        "singleton_accuracy": float(np.sum(singleton_correct) / max(1, np.sum(singleton))),
        "empty_rate": float(np.mean(sizes == 0)),
        "top1_accuracy": float(np.mean(top1 == y)),
        "ece": float(expected_calibration_error(probs, y)),
    }


def expected_calibration_error(probs: np.ndarray, y: np.ndarray, n_bins: int = 15) -> float:
    conf = np.max(probs, axis=1)
    pred = np.argmax(probs, axis=1)
    correct = pred == y
    ece = 0.0
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (conf > lo) & (conf <= hi)
        if np.any(mask):
            ece += np.mean(mask) * abs(np.mean(correct[mask]) - np.mean(conf[mask]))
    return ece


def smooth_probs(probs: np.ndarray, epsilon: float = 0.05) -> np.ndarray:
    k = probs.shape[1]
    return (1.0 - epsilon) * probs + epsilon / k


def _standardize(calib: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = calib.mean(axis=0, keepdims=True)
    std = calib.std(axis=0, keepdims=True)
    std = np.where(std < 1e-8, 1.0, std)
    return (calib - mean) / std, (test - mean) / std


def _median_bandwidth(x: np.ndarray, max_points: int = 512) -> float:
    if x.shape[0] > max_points:
        rng = np.random.default_rng(0)
        x = x[rng.choice(x.shape[0], size=max_points, replace=False)]
    if x.shape[0] < 2:
        return 1.0
    diffs = x[:, None, :] - x[None, :, :]
    distances = np.sqrt(np.sum(diffs * diffs, axis=-1))
    distances = distances[np.triu_indices_from(distances, k=1)]
    return float(np.median(distances[distances > 0])) if np.any(distances > 0) else 1.0
