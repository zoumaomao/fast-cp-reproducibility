from __future__ import annotations

import numpy as np


def interpolate_nan_1d(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float32).copy()
    mask = np.isfinite(x)
    if mask.all():
        return x
    if not mask.any():
        return np.zeros_like(x, dtype=np.float32)
    idx = np.arange(x.size)
    x[~mask] = np.interp(idx[~mask], idx[mask], x[mask])
    return x


def fill_nans(x: np.ndarray) -> np.ndarray:
    return np.vstack([interpolate_nan_1d(row) for row in x]).astype(np.float32)


def corrupt_batch(x: np.ndarray, kind: str, severity: float, rng: np.random.Generator) -> np.ndarray:
    if kind == "clean" or severity <= 0:
        return x.astype(np.float32).copy()
    if kind == "gap":
        return _gap(x, severity, rng)
    if kind == "noise":
        return _noise(x, severity, rng)
    if kind == "drift":
        return _drift(x, severity, rng)
    if kind == "mixed":
        return _mixed(x, severity, rng)
    if kind == "warp":
        return _warp(x, severity, rng)
    raise ValueError(f"Unknown corruption kind: {kind}")


def _gap(x: np.ndarray, severity: float, rng: np.random.Generator) -> np.ndarray:
    out = x.astype(np.float32).copy()
    length = out.shape[1]
    gap_len = max(1, int(round(length * severity)))
    for row in out:
        start = int(rng.integers(0, max(1, length - gap_len + 1)))
        row[start : start + gap_len] = np.nan
    return out


def _noise(x: np.ndarray, severity: float, rng: np.random.Generator) -> np.ndarray:
    scale = np.nanstd(x, axis=1, keepdims=True)
    scale = np.where(scale < 1e-8, 1.0, scale)
    return (x + rng.normal(0.0, severity, size=x.shape).astype(np.float32) * scale).astype(np.float32)


def _drift(x: np.ndarray, severity: float, rng: np.random.Generator) -> np.ndarray:
    length = x.shape[1]
    base = np.linspace(1.0 - severity, 1.0 + severity, length, dtype=np.float32)
    signs = rng.choice(np.array([-1.0, 1.0], dtype=np.float32), size=(x.shape[0], 1))
    drift = np.where(signs > 0, base, base[::-1])
    return (x * drift).astype(np.float32)


def _mixed(x: np.ndarray, severity: float, rng: np.random.Generator) -> np.ndarray:
    out = _gap(x, severity, rng)
    out = _noise(out, severity, rng)
    drift_severity = min(0.40, 2.0 * severity)
    return _drift(out, drift_severity, rng)


def _warp(x: np.ndarray, severity: float, rng: np.random.Generator) -> np.ndarray:
    out = np.empty_like(x, dtype=np.float32)
    length = x.shape[1]
    src = np.linspace(0.0, 1.0, length)
    for i, row in enumerate(x):
        anchors = np.linspace(0.0, 1.0, 6)
        offsets = rng.normal(0.0, severity * 0.08, size=anchors.size)
        offsets[0] = 0.0
        offsets[-1] = 0.0
        warped = np.clip(anchors + offsets, 0.0, 1.0)
        warped = np.maximum.accumulate(warped)
        if warped[-1] <= warped[0]:
            out[i] = row
            continue
        warped = (warped - warped[0]) / (warped[-1] - warped[0])
        target = np.interp(src, warped, anchors)
        out[i] = np.interp(target, src, row).astype(np.float32)
    return out
