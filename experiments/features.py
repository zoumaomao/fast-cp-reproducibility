from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from experiments.corruptions import fill_nans


def z_norm(x: np.ndarray) -> np.ndarray:
    x = fill_nans(x)
    mean = x.mean(axis=1, keepdims=True)
    std = x.std(axis=1, keepdims=True)
    std = np.where(std < 1e-8, 1.0, std)
    return ((x - mean) / std).astype(np.float32)


@dataclass
class RandomConvFeatures:
    n_kernels: int = 256
    seed: int = 0
    lengths: tuple[int, ...] = (7, 9, 11)

    def fit(self, x: np.ndarray) -> "RandomConvFeatures":
        rng = np.random.default_rng(self.seed)
        series_len = x.shape[1]
        self.kernels_: list[tuple[np.ndarray, int]] = []
        for _ in range(self.n_kernels):
            length = int(rng.choice(self.lengths))
            length = min(length, series_len)
            weights = rng.normal(0.0, 1.0, size=length).astype(np.float32)
            weights -= weights.mean()
            max_dilation = max(1, (series_len - 1) // max(1, length - 1))
            dilation = int(rng.integers(1, max_dilation + 1))
            self.kernels_.append((weights, dilation))
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        x = z_norm(x)
        feature_blocks = [_basic_stats(x)]
        conv_features = np.empty((x.shape[0], self.n_kernels * 3), dtype=np.float32)
        for i, row in enumerate(x):
            pos = 0
            for weights, dilation in self.kernels_:
                values = _dilated_convolve_valid(row, weights, dilation)
                conv_features[i, pos] = np.mean(values > 0.0)
                conv_features[i, pos + 1] = np.max(values)
                conv_features[i, pos + 2] = np.mean(values)
                pos += 3
        feature_blocks.append(conv_features)
        return np.hstack(feature_blocks).astype(np.float32)

    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        return self.fit(x).transform(x)


def _dilated_convolve_valid(row: np.ndarray, weights: np.ndarray, dilation: int) -> np.ndarray:
    receptive = (len(weights) - 1) * dilation + 1
    if receptive > row.size:
        dilation = 1
        receptive = len(weights)
    count = row.size - receptive + 1
    out = np.empty(count, dtype=np.float32)
    offsets = np.arange(len(weights)) * dilation
    for i in range(count):
        out[i] = np.dot(row[i + offsets], weights)
    return out


def _basic_stats(x: np.ndarray) -> np.ndarray:
    diff = np.diff(x, axis=1)
    fft = np.abs(np.fft.rfft(x, axis=1))
    fft_sum = fft.sum(axis=1, keepdims=True) + 1e-8
    prob = fft / fft_sum
    entropy = -(prob * np.log(prob + 1e-8)).sum(axis=1, keepdims=True)
    return np.hstack(
        [
            x.mean(axis=1, keepdims=True),
            x.std(axis=1, keepdims=True),
            np.min(x, axis=1, keepdims=True),
            np.max(x, axis=1, keepdims=True),
            np.mean(np.abs(diff), axis=1, keepdims=True),
            entropy.astype(np.float32),
        ]
    ).astype(np.float32)


def perturbation_fingerprint(x_raw: np.ndarray, probs: np.ndarray | None = None) -> np.ndarray:
    missing = np.mean(~np.isfinite(x_raw), axis=1, keepdims=True).astype(np.float32)
    x = z_norm(x_raw)
    diff = np.diff(x, axis=1)
    var_ratio = (np.var(diff, axis=1, keepdims=True) / (np.var(x, axis=1, keepdims=True) + 1e-8)).astype(np.float32)

    fft = np.abs(np.fft.rfft(x, axis=1))
    fft_prob = fft / (fft.sum(axis=1, keepdims=True) + 1e-8)
    spectral_entropy = -(fft_prob * np.log(fft_prob + 1e-8)).sum(axis=1, keepdims=True).astype(np.float32)

    centered = x - x.mean(axis=1, keepdims=True)
    autocorr = np.mean(centered[:, :-1] * centered[:, 1:], axis=1, keepdims=True).astype(np.float32)
    drift = np.abs(x[:, x.shape[1] // 2 :].mean(axis=1, keepdims=True) - x[:, : x.shape[1] // 2].mean(axis=1, keepdims=True))
    amplitude = (np.ptp(x, axis=1, keepdims=True) / (np.std(x, axis=1, keepdims=True) + 1e-8)).astype(np.float32)

    blocks = [missing, var_ratio, spectral_entropy, autocorr, drift.astype(np.float32), amplitude]
    if probs is not None:
        sorted_probs = np.sort(probs, axis=1)
        top = sorted_probs[:, -1:]
        second = sorted_probs[:, -2:-1] if probs.shape[1] > 1 else np.zeros_like(top)
        blocks.extend([top.astype(np.float32), (top - second).astype(np.float32)])
    return np.hstack(blocks).astype(np.float32)

