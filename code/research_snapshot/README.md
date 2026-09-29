# Archived experimental implementations

These files preserve the implementation context for the already completed
Ridge, LightGBM, N-HiTS, declarations, and record-reassignment studies. They
are copied from the original workspace, without being rerun or rewritten.
The original result-directory conventions are retained. They are not a
one-command portable retraining package.

For portable source preparation, input views, prediction submissions, scoring,
and the default four-arm tree comparison, use the parent `code/scripts/` and
`code/docs/RECORD_COMPARISON_RUNTIME.md`. Acquire source records and prepare
packets locally using the source guides; neither packets nor ACN donor records
are included in this repository. Adapt archived paths to your local directories.

For manuscript reproduction without experiments, use
`python code/build_paper_assets.py` from the release root. Existing scores
already support every result in the paper. Do not run the archived training
entries merely to regenerate the PDF.
