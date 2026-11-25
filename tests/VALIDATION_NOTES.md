# Validation notes: miami-flight-policy (paid wave 3 validation, 2026-11-25)

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/validation_w3_2026-11-25/miami-flight-policy@w3/`, arm
`full`, DeepSeek V4 Flash (Nebius), temperature 0, max_steps 6, max_tokens 8192, one run per scenario, at plugin
head 7aed5af. Line numbers are lines of `src/plugin/data/policy.txt`.

## Results

21/24 valid (87.5%), mean field score 0.938, **easy 5/5**. By category: boundary_twin 6/6, distractor 1/2, easy 5/5, flag 1/3, hidden_clause 2/2, multi_rule 4/4, refusal 2/2.
$0.00124 billed per run, 8,203 prompt tokens per call, 4.04 calls per run;
0 of 24 runs would exceed the hosted 65,536 cap.

## Every failure, classified

| scenario | category | submitted vs key | class | evidence |
|---|---|---|---|---|
| jasmine-shoal | flag | BOOK Delta premium economy, PREMIUM_ECONOMY_ALLOWED; key FLAG | model slip | "The flight is over 4 hours (about 5 hours flying time), so premium economy is permitted ... without a special business reason." Only connections are listed, and each flight is under 4 hours (110 and 200 minutes); it never asked whether line 121's "flight under 4 hours" means each flight or the journey. The twins ibis-quarry and osprey-quill passed. |
| saffron-key | distractor | REFUSE, PERSONAL_TRAVEL_NOT_COVERED; key BOOK JetBlue Friday ($289) | model slip | "a flight extended for personal travel requires a comparison non-refundable coach fare quote ... Since ... no such comparison quote is on file, the personal travel is not covered". Lines 139-144 ask for the comparison quote "obtained at the time of booking" and limit reimbursement to the lesser fare; the agent could have searched the business date (Monday, $214) itself. Nothing in lines 130-144 refuses the Friday ticket. |
| vesper-tide | flag | BOOK United economy, UPGRADE_NOT_ELIGIBLE; key FLAG | model slip | "the reason given (can't work in economy) is not an appropriate business reason". It took one reading of the undefined "appropriate business reason" (lines 122, 126-127) and never weighed that writing the grant renewal on board, due when the review starts, is University work. The twins cypress-ember and kestrel-isle passed. |

## Fixes

None. All 3 failures are model slips; no key was widened and no record changed.

## Q2

Unchanged: the always-cheapest agent passes **7/24 (29%)**.

## Re-score at the head (stored answers)

21/24 (no key changed). No re-run is required.

## Checks (at the notes commit)

`uv run pytest -q` (213 passed), `uv run ruff check .`, `uv lock --check`, `check_shared.py`, byte-identical `rules.py`,
`tools/stock_verify.py` (0 failures), stock `nanoagent plugin inspect .` (exit 0).
