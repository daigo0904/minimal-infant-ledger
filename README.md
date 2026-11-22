# What Does a Minimal Infant Need to Become Social? — code and ledger

Code, preregistrations and per-world results for experiments **S1–S246** reported in the paper
*"What Does a Minimal Infant Need to Become Social? A Preregistered Phenomenon Ledger"* (ALIFE 2027 submission).

## Layout

| Path | Contents |
|---|---|
| `experiments/S<n>_<name>_<date>/` | One folder per experiment: `事前登録.md` (preregistration: hypotheses and pass thresholds written before the main run), scripts (`*.py`), results (`結果_本.json` = main run, 30 worlds; `結果_追試.json` = replication, 30 new worlds), logs |
| `ledger/台帳.html` | The phenomenon ledger (which reported human phenomena appeared in the model, and which did not) |
| `ledger/見取り図.html` | Overview map of all experiments |
| `preregistration_timestamps.tsv` | For each folder, the time (UTC) the preregistration and the main-run result were first committed in the author's working repository |

Folder and file names are in Japanese. Reported values are medians over 30 worlds; tuning used seeds 900–909, the main run and the replication each used 30 new seeds, and the usual pass threshold was 20/30 worlds (see each `事前登録.md`).

## Confirmatory test S252

Preregistration released before the run: doi:10.5281/zenodo.24432900 (archived 2026-11-22 03:36 UTC; run started 03:37 UTC). Result: 9 of 10 hypotheses passed in both runs; C5 (the bond's added effect is smaller in the unrelated world) failed in both runs, as predicted in the preregistration. Results are in `experiments/S252_*/結果_本.json` and `結果_追試.json`.

`analysis/effects.py` computes per-world effect sizes with bootstrap intervals for the paper's headline comparisons.

## Reproducing

- Environment used for all runs: Python 3.14.6, NumPy 2.5.1 (`requirements.txt`), macOS 27 on arm64. NumPy is the only dependency.
- Seeds, parameters and world settings are written in each experiment's script and preregistration; per-world raw values are in `結果_本.json` / `結果_追試.json` (key `行` or `値`), and each script recomputes its own summary.
- Quick check: `python3 analysis/check_reproduce.py` re-runs 12 stored worlds (S152 B0 and v4 on five chapters, S48, S41) through the frozen S252 script and compares them with the stored values. It prints `12/12 values reproduced exactly` on the machine above.
- The confirmatory test: `cd experiments/S252_*; python3 本番テスト.py 本` (and `追試`), about 25 minutes each on 8 cores.

## Running

Python 3 with NumPy. Run a script from inside its own folder, e.g.

```
cd experiments/S48_得と邪魔を分ける_20261118
python3 走らせる.py
```

Scripts load code from sibling experiment folders through `../`.

## Notes on this copy

- Absolute paths to the author's home directory were replaced by relative paths (`../`) in scripts and by `<experiments>/` in logs. Nothing else was changed.
- `preregistration_timestamps.tsv` comes from the author's private repository and cannot be checked independently; the archived snapshot of this repository fixes the state from its release date onward. 30 folders are tuning-only or diagnostic and have no main-run file.
- Experiments after S246 are not included, except `experiments/S252_*`: a confirmatory test on frozen code whose preregistration was released (and archived on Zenodo) before it was run.
- Branch `prereg-history` replays the original commit history of the S1–S246 folders (488 commits, original dates, author name replaced, same path substitutions). Commit dates in git can be set by the author, so this shows order, not proof.

## License

Code: MIT (see `LICENSE`). Results, preregistrations and ledger pages: CC BY 4.0.
