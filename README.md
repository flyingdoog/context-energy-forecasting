# Context-Aware Energy Forecasting

**When Does Context Help Forecasting? An Empirical Study of Energy Systems**

Xu Zheng, Jingchao Ni, Mo Sha, and Dongsheng Luo

[Read the paper (PDF)](paper/context_energy_forecasting.pdf) · [LaTeX source](paper/main.tex) · [Data sources](code/docs/SOURCE_NOTES.md) · [Runtime guide](code/README.md)

This study asks when operational records improve forecasts beyond power history.
It covers water heaters, workplace and fast EV charging, and building air
conditioning, using four source collections: BPA, ACN-Data, EPFL, and CU-BEMS.
Ridge, LightGBM, and N-HiTS compare matched information conditions. A separate
record-reassignment experiment distinguishes a fitted predictor's sensitivity
from the effect of retraining with reassigned records.

## Contents

| Directory | Contents |
| --- | --- |
| `paper/` | Six-page manuscript, bibliography, vector figures, and tables |
| `results/` | Saved aggregate scores used in the paper |
| `code/src/`, `code/scripts/` | Source preparation, forecasting interfaces, scoring, and record-comparison tools |
| `code/tests/`, `code/docs/` | Runtime tests and source-specific instructions |
| `code/research_snapshot/` | Implementations from the completed research experiments |

Source records, prepared input/target packets, model weights, environments, and
prediction caches are not bundled. Obtain source data from the providers using
the guides below. The saved scores are sufficient to regenerate the paper's
figures and tables without downloading data or training models.

## Rebuild the paper

Run from the repository root in a Python environment (Python 3.12 was used):

```sh
python -m pip install -r code/requirements-paper.txt
python code/build_paper_assets.py
python code/build_pdf.py
```

The final command requires `pdflatex`, `bibtex`, `IEEEtran`, and `balance` in a
LaTeX installation. It writes `paper/context_energy_forecasting.pdf`.
To compile only the supplied manuscript and displays, skip the first two commands.
These commands do not run forecasting experiments.

## Prepare data and evaluate forecasts

Install `code/requirements-operational.txt`, then follow the
[runtime guide](code/README.md). Source guides assume the working directory is
`code/`:

- [BPA water heaters](code/docs/BPA_QUICKSTART.md)
- [ACN workplace charging](code/docs/ACN_QUICKSTART.md)
- [EPFL fast charging](code/docs/EPFL_QUICKSTART.md)
- [CU-BEMS air conditioning](code/docs/CU_BEMS_QUICKSTART.md)

The runtime preserves observation masks, native forecast intervals, device
identity, and complete-group membership. It supports
[custom forecasting models](code/docs/RECORD_CUSTOM_MODEL.md) and a
[four-arm record-association comparison](code/docs/RECORD_COMPARISON_RUNTIME.md).
Model dependencies are installed separately from preparation and scoring tools.

The research snapshot retains the original experimental directory conventions
and additional model dependencies; it is not a one-command retraining package.
See its [README](code/research_snapshot/README.md) before using those entries.

## Data attribution and licensing

Please retain provider attribution and observe each source's terms. BPA and ACN
redistribution permissions have not been established for this release, so this
repository supplies acquisition instructions rather than source or derived
data. See [source notes](code/docs/SOURCE_NOTES.md) and
[dependency notices](code/THIRD_PARTY_NOTICES.md). No license has yet been
selected for the original project code; third-party licenses do not license it.

## Citation

```bibtex
@misc{zheng2026contextenergy,
  title = {When Does Context Help Forecasting? An Empirical Study of Energy Systems},
  author = {Zheng, Xu and Ni, Jingchao and Sha, Mo and Luo, Dongsheng},
  year = {2026},
  howpublished = {Manuscript},
  url = {https://github.com/flyingdoog/context-energy-forecasting}
}
```
