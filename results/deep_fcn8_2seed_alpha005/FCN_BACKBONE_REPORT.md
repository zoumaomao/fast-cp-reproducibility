# FCN Backbone Check

Eight UCR datasets, two seeds, FCNClassifier for 20 epochs, alpha=0.05. FAST-CP mixed uses lambda=0.35 and the same augmented calibration pool as Aug SCP.

| Corruption | FAST cov. | Aug cov. | Cov. delta | Set reduction | n cells |
|---|---:|---:|---:|---:|---:|
| Overall | 0.9541 | 0.9556 | -0.0014 | 0.0139 | 144 |
| drift | 0.9519 | 0.9544 | -0.0026 | 0.0139 | 48 |
| gap | 0.9426 | 0.9431 | -0.0005 | 0.0139 | 48 |
| noise | 0.9679 | 0.9691 | -0.0012 | 0.0138 | 48 |

Overall 95% bootstrap intervals:
- Set-size reduction: 0.0139, CI [0.0090, 0.0194].
- Coverage delta: -0.0014, CI [-0.0024, -0.0006].
