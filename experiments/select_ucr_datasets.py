from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from experiments.data import load_ucr_dataset


UCR_CANDIDATES = [
    "ACSF1",
    "Adiac",
    "ArrowHead",
    "Beef",
    "BeetleFly",
    "BirdChicken",
    "BME",
    "Car",
    "CBF",
    "Chinatown",
    "ChlorineConcentration",
    "Coffee",
    "Computers",
    "CricketX",
    "CricketY",
    "CricketZ",
    "DiatomSizeReduction",
    "DistalPhalanxOutlineAgeGroup",
    "DistalPhalanxOutlineCorrect",
    "DistalPhalanxTW",
    "Earthquakes",
    "ECG200",
    "ECG5000",
    "ECGFiveDays",
    "FaceAll",
    "FaceFour",
    "FacesUCR",
    "FiftyWords",
    "Fish",
    "GunPoint",
    "GunPointAgeSpan",
    "GunPointMaleVersusFemale",
    "GunPointOldVersusYoung",
    "Ham",
    "Herring",
    "InsectEPGRegularTrain",
    "InsectEPGSmallTrain",
    "ItalyPowerDemand",
    "Lightning2",
    "Lightning7",
    "Meat",
    "MedicalImages",
    "MiddlePhalanxOutlineAgeGroup",
    "MiddlePhalanxOutlineCorrect",
    "MiddlePhalanxTW",
    "MoteStrain",
    "OliveOil",
    "OSULeaf",
    "Plane",
    "ProximalPhalanxOutlineAgeGroup",
    "ProximalPhalanxOutlineCorrect",
    "ProximalPhalanxTW",
    "ShapeletSim",
    "SonyAIBORobotSurface1",
    "SonyAIBORobotSurface2",
    "Strawberry",
    "SwedishLeaf",
    "Symbols",
    "SyntheticControl",
    "ToeSegmentation1",
    "ToeSegmentation2",
    "Trace",
    "TwoLeadECG",
    "UMD",
    "Wine",
    "WordSynonyms",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select a systematic small-to-medium UCR subset.")
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--out-csv", default="results/ucr_selection/ucr_selected.csv")
    parser.add_argument("--out-json", default="results/ucr_selection/ucr30_datasets.json")
    parser.add_argument("--target-count", type=int, default=30)
    parser.add_argument("--max-total", type=int, default=2500)
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--max-classes", type=int, default=20)
    parser.add_argument("--candidates", nargs="*", default=UCR_CANDIDATES)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows: list[dict[str, object]] = []
    selected: list[str] = []
    for name in args.candidates:
        row: dict[str, object] = {"dataset": name}
        try:
            x_train, y_train, x_test, y_test = load_ucr_dataset(name, args.data_dir)
            n_train = int(x_train.shape[0])
            n_test = int(x_test.shape[0])
            length = int(x_train.shape[1])
            n_classes = int(len(set(y_train.tolist()) | set(y_test.tolist())))
            total = n_train + n_test
            row.update(
                {
                    "n_train": n_train,
                    "n_test": n_test,
                    "n_total": total,
                    "length": length,
                    "n_classes": n_classes,
                }
            )
            if n_classes < 2:
                row.update({"selected": False, "reason": "fewer_than_two_classes"})
            elif total > args.max_total:
                row.update({"selected": False, "reason": "too_many_examples"})
            elif length > args.max_length:
                row.update({"selected": False, "reason": "too_long"})
            elif n_classes > args.max_classes:
                row.update({"selected": False, "reason": "too_many_classes"})
            elif len(selected) >= args.target_count:
                row.update({"selected": False, "reason": "target_count_reached"})
            else:
                selected.append(name)
                row.update({"selected": True, "reason": "selected"})
        except Exception as exc:
            row.update({"selected": False, "reason": f"{type(exc).__name__}: {exc}"})
        rows.append(row)

    df = pd.DataFrame(rows)
    out_csv = Path(args.out_csv)
    out_json = Path(args.out_json)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    out_json.write_text(json.dumps({"datasets": selected, "count": len(selected)}, indent=2))
    print(df.to_string(index=False))
    print(f"\nSelected {len(selected)} datasets: {' '.join(selected)}")
    print(f"Wrote {out_csv} and {out_json}")


if __name__ == "__main__":
    main()
