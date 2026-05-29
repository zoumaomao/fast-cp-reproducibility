from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np
import requests
from sklearn.preprocessing import LabelEncoder


UCR_URL = "https://www.timeseriesclassification.com/aeon-toolkit/{name}.zip"


def download_ucr_dataset(name: str, data_dir: str | Path = "data/raw") -> Path:
    data_dir = Path(data_dir)
    out_dir = data_dir / name
    train_file = out_dir / f"{name}_TRAIN.txt"
    test_file = out_dir / f"{name}_TEST.txt"
    if train_file.exists() and test_file.exists():
        return out_dir

    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = data_dir / f"{name}.zip"
    if not zip_path.exists():
        response = requests.get(UCR_URL.format(name=name), timeout=60)
        response.raise_for_status()
        if not response.content.startswith(b"PK"):
            raise RuntimeError(f"Dataset download for {name} did not return a zip archive.")
        zip_path.write_bytes(response.content)

    with zipfile.ZipFile(io.BytesIO(zip_path.read_bytes())) as archive:
        archive.extractall(out_dir)
    if not train_file.exists() or not test_file.exists():
        raise FileNotFoundError(f"Could not find {name}_TRAIN.txt and {name}_TEST.txt in {out_dir}")
    return out_dir


def _load_txt(path: Path) -> tuple[np.ndarray, np.ndarray]:
    rows: list[list[str]] = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped:
            rows.append(stripped.replace(",", " ").split())
    if not rows:
        raise ValueError(f"No rows found in {path}")
    labels = np.array([row[0] for row in rows])
    values = np.array([[float(v) for v in row[1:]] for row in rows], dtype=np.float32)
    return values, labels


def load_ucr_dataset(name: str, data_dir: str | Path = "data/raw") -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    out_dir = download_ucr_dataset(name, data_dir)
    x_train, y_train_raw = _load_txt(out_dir / f"{name}_TRAIN.txt")
    x_test, y_test_raw = _load_txt(out_dir / f"{name}_TEST.txt")

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train_raw)
    y_test = encoder.transform(y_test_raw)
    return x_train, y_train, x_test, y_test

