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
- Experiments after S246 are not included.

## License

Code: MIT (see `LICENSE`). Results, preregistrations and ledger pages: CC BY 4.0.
