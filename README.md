# Recoup — deterministic reconciliation core

A small payment-reconciliation core: normalize source records, match candidates deterministically, and keep recovery authorization outside probabilistic logic.

Money is integer paise. Matching requires equal amount and a bounded timestamp window; reference equality raises confidence. Each right-side transaction is used at most once. Recovery is a separate deterministic gate with explicit amount limits.

There is **no money-execution API and no LLM dependency**. A future diagnosis layer may classify ambiguous exceptions, but model output must never authorize a financial action.

## Test
`pip install -e . && pytest -q`

## Evaluation
`python eval.py` is a correctness smoke test, not a production benchmark.

## License
MIT.
