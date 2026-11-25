# University of Miami Travel Policy Flight Booking

**Source of the handbook:** http://umiami.policystat.com/policy/9607266/. The agent reads it verbatim (bundled at `src/plugin/data/policy.txt`); flights, fares and trips are synthetic.

**No affiliation with the University of Miami.** The handbook is the University's public *Travel Policy*
(PolicyStat ID 9607266, effective April 2021, <http://umiami.policystat.com/policy/9607266/>), bundled verbatim
for research.

A `nanoagent.plugin/v0001` plugin. An agent handles one traveller's flight request under the University's real
travel policy: it reads the trip record, searches a simulated flight world and submits **BOOK**, **REFUSE** or
**FLAG_FOR_APPROVAL** with the offer, cabin, reason, approver and policy section. A deterministic Python verifier,
with no LLM, rebuilds the offers and the policy's answer itself and checks every field. Built from the
original-handbook template (`handbook_plugins/_template`); `tests/build_scenarios.py` writes the scenario files.

## The handbook and the harness flag

The frozen text (`src/plugin/data/policy.txt`, 3,442 words, 289 lines, 23,362 characters, sha256
`f05a964f...56c6fb02e`, equal to `pilot_work/originals/miami/frozen/SHA256SUMS`) is never paraphrased, and the task
text restates no rule. Under stock NanoAgent the agent does not see it: the plugin then runs as the `off` baseline.
The `harness.policy` switch of the NanoAgent fork (github.com/tejassaboo/nanoagent, branch `policy-switch`) adds it to
the system prompt: `harness.policy: full` adds all of it, and the selection methods add parts of it. These plugins
are meant to run with `query: instructions+input`, so a selector sees the traveller's request.

The extraction prints the three justification bullets (lines 120-122) above the sentence that introduces them
(lines 126-127, "An appropriate business reason will be required when booking:"), and the PolicyStat left-column
headings where each page's text starts (PURPOSE/SCOPE/POLICY stacked at lines 13-15). The text is kept as extracted;
the clause accept sets take every heading a reader could file a sentence under.

**Size.** Calibrated on the paid Thornton and NJC validation runs (about 0.2 tokens a character of handbook plus
1,800 for the rest of the first prompt), the first call under `full` is about 6,500 input tokens, the second about
7,100 (plus the trip record) and the third 8,000 to 9,300 (plus 2 to 9 offers). A 3-call run is about 22,000 to
23,000 input tokens and ends near 33,000 with the final message and output: far under the hosted cap of 65,536,
with room for three or four extra tool calls (for example the comparison search of `saffron-key`).

## Task

- **Input:** `TaskInput`: `scenario` (one of 24 case ids) and `request`, the traveller's own words.
- **Steps:** `get_trip`, then `search_flights` on the trip's route and date, then `submit`.
- **Output:** `BookingOutput`: `decision`, `offer_id` (empty when refusing), `cabin` (`NONE` when refusing),
  `reason_code`, `approver` and `clause`, each from a closed list. The reason list is the template's shared list
  plus `REQUESTED_TIME_WINDOW`, `FARE_WITHIN_TOLERANCE`, `BUSINESS_REASON_MISSING`, `BUSINESS_REASON_DOCUMENTED`,
  `FLY_AMERICA_US_CARRIER_REQUIRED`, `OPEN_SKIES_AGREEMENT`, `COMPANION_UNIVERSITY_ROLE` and
  `PERSONAL_EXTENSION_COMPARISON`, and decoy codes from other handbooks' rules. Fares are in cents of US dollars.
- **Success:** every field is one the answer key accepts; the cabin is graded as the chosen offer's own. Score =
  fields right / 6.
- **Trip approvals.** Lines 17-19 require prior approval of all University travel by the supervisor and the
  supervising dean or vice president, and for faculty also by Faculty Affairs. Every trip record holds the approvals
  it has; a booking accepts each of those roles and `NONE` (template rule 4'), a refusal accepts `NONE` and the
  roles on file (rule 4(b)), and a hold accepts only the awaited roles. Lines 17-19 are COVID-19 guidance a reader
  may take as lapsed, so no answer depends on them alone: the one approval hold (`thistle-pier`) has nothing on file,
  and the supervisor's authorization of lines 34-37 and 47-48 is awaited on every reading.
- **Reasons on a declined request.** The task instructions say that when the booking is not what the traveller asked
  for, the reason code gives why the request is declined. A declined premium economy or business cabin accepts
  `BUSINESS_REASON_MISSING`, `UPGRADE_NOT_ELIGIBLE` and `LONG_FLIGHT_CONDITION_NOT_MET`, not `LOWEST_FARE`
  (`cypress-ember`, `osprey-quill`, `manatee-reed`); the Fly America case does not accept `LOWEST_FARE`
  (`pompano-ridge`). A nonstop declined because the connection passes the handbook's own savings and time test
  accepts `LOWEST_FARE` beside the specific codes and `BUSINESS_REASON_MISSING` (the nonstop, more than $200 over,
  needs a business reason; `egret-sable`, `anhinga-dell`, `gannet-wold`), and so does the airline wish
  declined on the $200 tolerance of the lowest airfare (`marlin-cove`).
- **Hidden facts** (`answer_key_inputs`, never shown): how the traveller's stated reason reads (`cypress-ember`
  personal, `kestrel-isle` economy sold out, `vesper-tide` unclear) and that the NSF grant of `pompano-ridge` is a
  federal award.

| Scenario | Category | Expected decision (offer; cabin) | Reason | Approver | Clause (frozen lines of must_keep) |
|---|---|---|---|---|---|
| `cypress-ember` | easy | BOOK (midday-economy; ECONOMY) | BUSINESS_REASON_MISSING or LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (122, 126-127, 117-118, 47-49, 17-19, 34-37) |
| `heron-gable` | easy | BOOK (morning-economy; ECONOMY) | LOWEST_FARE or REQUESTED_TIME_WINDOW | DEAN or NONE or SUPERVISOR | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (115-116, 117-118, 17-19, 34-37) |
| `mangrove-lute` | easy | BOOK (american-premium; PREMIUM_ECONOMY) | FARE_WITHIN_TOLERANCE or PREMIUM_ECONOMY_ALLOWED or UPGRADE_WITHIN_FARE_MARGIN | DEAN or FACULTY_AFFAIRS or NONE or SUPERVISOR | AIR_TRAVEL or PROCEDURE (121, 126-127, 123, 128-129, 17-19, 34-37) |
| `pelican-arch` | easy | BOOK (atlanta-economy; ECONOMY) | ALTERNATE_ROUTE_TOO_EXPENSIVE or ALTERNATE_ROUTE_WITHIN_MARGIN or COST_SAVINGS or LOWEST_FARE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (149-150, 117-118, 47-49, 17-19, 34-37) |
| `sawgrass-loom` | easy | BOOK (iberia-economy; ECONOMY) | LOWEST_FARE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or INTERNATIONAL_TRAVEL or POLICY or PROCEDURE (117-118, 47-49, 233-235, 17-19, 34-37) |
| `egret-sable` | boundary_twin | BOOK (atlanta-economy; ECONOMY) | ALTERNATE_ROUTE_TOO_EXPENSIVE or ALTERNATE_ROUTE_WITHIN_MARGIN or BUSINESS_REASON_MISSING or COST_SAVINGS or LOWEST_FARE | DEAN or NONE or SUPERVISOR | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (149-150, 120, 126-127, 128-129, 117-118, 17-19, 34-37) |
| `ibis-quarry` | boundary_twin | BOOK (united-premium; PREMIUM_ECONOMY) | FARE_WITHIN_TOLERANCE or PREMIUM_ECONOMY_ALLOWED or UPGRADE_WITHIN_FARE_MARGIN | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or PROCEDURE (121, 126-127, 123, 128-129, 17-19, 34-37) |
| `manatee-reed` | boundary_twin | BOOK (latam-economy; ECONOMY) | BUSINESS_REASON_MISSING or LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or INTERNATIONAL_TRAVEL or POLICY or PROCEDURE (122, 126-127, 117-118, 47-49, 233-235, 17-19, 34-37) |
| `osprey-quill` | boundary_twin | BOOK (united-economy; ECONOMY) | BUSINESS_REASON_MISSING or LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (121, 126-127, 117-118, 47-49, 17-19, 34-37) |
| `snook-larder` | boundary_twin | BOOK (nonstop-economy; ECONOMY) | ALTERNATE_ROUTE_WITHIN_MARGIN or FARE_WITHIN_TOLERANCE or LOWEST_FARE | DEAN or NONE or SUPERVISOR | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (149-150, 123, 128-129, 117-118, 17-19, 34-37) |
| `tarpon-mesa` | boundary_twin | BOOK (american-business; BUSINESS) | FARE_WITHIN_TOLERANCE or INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED or UPGRADE_WITHIN_FARE_MARGIN | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or INTERNATIONAL_TRAVEL or PROCEDURE (122, 126-127, 123, 128-129, 233-235, 17-19, 34-37) |
| `anhinga-dell` | multi_rule | BOOK (atlanta-economy; ECONOMY) | ALTERNATE_ROUTE_TOO_EXPENSIVE or ALTERNATE_ROUTE_WITHIN_MARGIN or BUSINESS_REASON_MISSING or COST_SAVINGS or LOWEST_FARE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (149-150, 120, 126-127, 128-129, 117-118, 17-19, 34-37) |
| `gannet-wold` | multi_rule | BOOK (atlanta-economy or nonstop-economy; ECONOMY) | ALTERNATE_ROUTE_TOO_EXPENSIVE or ALTERNATE_ROUTE_WITHIN_MARGIN or BUSINESS_REASON_MISSING or CONNECTION_TOO_LONG or COST_SAVINGS or LOWEST_FARE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (149-150, 120, 126-127, 117-118, 17-19, 34-37) |
| `kestrel-isle` | multi_rule | BOOK (late-morning-business; BUSINESS) | BUSINESS_REASON_DOCUMENTED or LOWEST_FARE or NO_ECONOMY_SEATS_URGENT | DEAN or FACULTY_AFFAIRS or NONE or SUPERVISOR | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (122, 126-127, 117-118, 17-19, 34-37) |
| `lumen-bay` | multi_rule | BOOK (late-morning-economy; ECONOMY) | COMPANION_UNIVERSITY_ROLE or LOWEST_FARE or REQUESTED_TIME_WINDOW | DEAN or NONE or SUPERVISOR | AIR_TRAVEL or BOOKING_FOR_OTHERS or DEFINITIONS or POLICY or PROCEDURE (269-272, 115-116, 117-118, 17-19, 34-37) |
| `brine-lattice` | hidden_clause | BOOK (midday-economy; ECONOMY) | LOWEST_FARE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or INTERNATIONAL_TRAVEL or POLICY or PROCEDURE (74-76, 233-235, 117-118, 47-49, 17-19, 34-37) |
| `pompano-ridge` | hidden_clause | BOOK (american-economy; ECONOMY) | FLY_AMERICA_US_CARRIER_REQUIRED or NATIONAL_CARRIER_REQUIRED or OPEN_SKIES_AGREEMENT | DEAN or FACULTY_AFFAIRS or NONE or SUPERVISOR | DEFINITIONS or INTERNATIONAL_TRAVEL or POLICY (58-59, 233-235, 17-19, 34-37) |
| `marlin-cove` | distractor | BOOK (delta-economy; ECONOMY) | BUSINESS_REASON_MISSING or LOWEST_FARE or LOYALTY_PROGRAM_PREFERENCE | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (120, 126-127, 128-129, 123, 117-118, 17-19, 34-37) |
| `saffron-key` | distractor | BOOK (friday-jetblue; ECONOMY) | LOWEST_FARE or PERSONAL_EXTENSION_COMPARISON or PERSONAL_TRAVEL_NOT_COVERED | NONE or SUPERVISOR or VICE_PRESIDENT | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE (139-144, 135-136, 17-19, 34-37) |
| `ochre-fen` | refusal | REFUSE (none; NONE) | OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED | NONE | AIR_TRAVEL or DEFINITIONS or POLICY or PROCEDURE or PURPOSE or SCOPE (26-31, 68-70, 106-107) |
| `wren-hollow` | refusal | REFUSE (none; NONE) | COMPANION_NOT_COVERED or OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED | DEAN or NONE or SUPERVISOR | BOOKING_FOR_OTHERS or DEFINITIONS (269-272, 71-72) |
| `jasmine-shoal` | flag | FLAG_FOR_APPROVAL (atlanta-economy or atlanta-premium; ECONOMY or PREMIUM_ECONOMY) | APPROVAL_REQUIRED or UNCLEAR_POLICY_TEXT | EXECUTIVE_VICE_PRESIDENT or NOT_NAMED or TRAVEL_MANAGEMENT | AIR_TRAVEL or PROCEDURE (121, 126-127, 123, 102-104, 62-63, 17-19, 34-37) |
| `thistle-pier` | flag | FLAG_FOR_APPROVAL (american-economy; ECONOMY) | APPROVAL_REQUIRED | DEAN or FACULTY_AFFAIRS or SUPERVISOR or VICE_PRESIDENT | DEFINITIONS or POLICY or PURPOSE or SCOPE (34-37, 47-48, 17-19, 117-118) |
| `vesper-tide` | flag | FLAG_FOR_APPROVAL (united-business or united-economy; BUSINESS or ECONOMY) | APPROVAL_REQUIRED or UNCLEAR_POLICY_TEXT | EXECUTIVE_VICE_PRESIDENT or NOT_NAMED or SUPERVISOR or TRAVEL_MANAGEMENT | AIR_TRAVEL or PROCEDURE (122, 126-127, 102-104, 62-63, 17-19, 34-37) |

Mix (EDGE_CASES.md 5.2, 24 row): 5 easy, 6 boundary twins, 4 multi-rule, 2 hidden clause, 2 distractor, 2 refusal,
3 flags (12.5%). Decisions: 19 BOOK (15 economy, 2 premium economy, 2 business), 2 REFUSE, 3 FLAG_FOR_APPROVAL.
Twin pairs: 240 against 239 scheduled minutes for premium economy (`ibis-quarry`, `osprey-quill`); 480 against 479
for business (`tarpon-mesa`, `manatee-reed`); a connection saving $201 against $199 (`egret-sable`, `snook-larder`);
a connection landing 120 against 125 minutes after the nonstop (`anhinga-dell`, `gannet-wold`); a spouse with and
without a University position (`lumen-bay`, `wren-hollow`).

Each hold has clear twins on both sides:

- **"appropriate business reason"** (lines 122, 126-127): undefined. `vesper-tide` (business on a 325-minute flight
  to write a grant renewal on board); twins `cypress-ember` (comfort: economy) and `kestrel-isle` (economy sold out
  on every flight landing in time: business).
- **"flight under 4 hours"** (line 121): whether a connection is one flight or several. `jasmine-shoal` (only
  connections, each flight under 4 hours, each journey over); twins `ibis-quarry` (240-minute nonstop: premium
  economy) and `osprey-quill` (239: economy).
- **Approval required.** `thistle-pier`: a professor who has not yet sent the trip to the chair for approval
  (lines 34-37, 47-48; lines 17-19 add the dean and Faculty Affairs if the COVID-19 guidance still applies). Hold the
  lowest fare for `SUPERVISOR` (or `DEAN`, `VICE_PRESIDENT`, `FACULTY_AFFAIRS`); twins `mangrove-lute` (faculty, all
  approvals on file) and `heron-gable` (a student, approvals on file).

Unclear holds accept `UNCLEAR_POLICY_TEXT` or `APPROVAL_REQUIRED`, the held offer of either reading (the cheapest
better cabin or the cheapest economy fare), and `NOT_NAMED`, `TRAVEL_MANAGEMENT` (lines 102-104) or
`EXECUTIVE_VICE_PRESIDENT` (exceptions, lines 62-63) as the approver (`vesper-tide` also `SUPERVISOR`).

**Duration (`rules.over`).** "premium-economy" (240) and "business" (480): a flight at or past the limit is not
"under" it, so the better cabin needs no business reason; a connection is True only when every flight is at or past
the limit, False when the whole elapsed journey is short of it, unclear (`None`) between. `handbook.json`
`background_offers` is 0 and every pinned search sets `background: 0`, so every listed offer is a pinned one and a
search the case does not pin lists nothing.

Degenerate agents (`tests/test_verifier.py`): one that always holds the right offer as unclear passes 2 cases
(`jasmine-shoal`, `vesper-tide`); one that always books the cheapest seat with `LOWEST_FARE`, `NONE` and the first
accepted section passes 7 of 24 (`anhinga-dell`, `brine-lattice`, `egret-sable`, `gannet-wold`, `marlin-cove`,
`pelican-arch`, `sawgrass-loom`).

## Tools

| Tool | Does | Code |
|---|---|---|
| `booking_requirements` | The trip record's fields, the world's conventions (local times, dates, fares, sold-out seats) and its airports | `src/plugin/guide.py` |
| `get_trip` | A case's request and trip record: traveller and role, route, dates, when the work begins, funding, requested cabin, routing, airline and departure time, stated reason, approvals on file | `src/plugin/tools.py` |
| `search_flights` | Every offer on a route and local date: the pinned scenario offers; a search the case does not pin lists nothing and says so | `src/plugin/world.py` |
| `solve_booking` | The answer key (`rules.solve`), the agent task's `reference`, never shown to the agent | `src/plugin/rules.py` |

| Task | Does | Runner |
|---|---|---|
| `book-miami-flight` | Handles one booking request | `agent`, with `get_trip` and `search_flights`; reference `solve_booking` |
| `booking-requirements` | Shows `booking_requirements` | `tool` |
| `search-flights` | Shows `search_flights` | `tool` |

## Layout

- `contract.py`: the template's shared contract plus this policy's scenario ids, approvers, sections, reason codes
  and trip record.
- `src/plugin/`: `world.py`, `scenarios.py`, `guide.py`, `answer.py`, `tools.py` (shared), `rules.py` (this
  policy's rules, citing frozen lines), `__main__.py`.
- `src/plugin/data/`: `policy.txt` (frozen), `handbook.json`, `scenarios/*.json`.
- `verifier/`: byte-identical copies of the shared modules and `rules.py`, plus `booking.py` and `tools.py`.
- `tests/`: the template's acceptance suite; `tests/plugin_spec.py` holds this policy's settings.
- `tests/build_scenarios.py`: writes the scenario files (an authoring aid, not a test).
- `tests/BUILD_NOTES.md`: decisions taken during the build, the blind read and the acceptance outputs.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv lock --check
python3 ../_template/check_shared.py .
# from a NanoAgent checkout (read-only use):
nanoagent plugin inspect <this folder>
nanoagent plugin pack <this folder> /tmp/miami-flight-policy.tar.gz
# from this folder, with that checkout's Python:
/path/to/nanoagent/nanoagent/.venv/bin/python ../_template/tools/stock_verify.py .
```

Offline: `hosts: []`, an empty `.env`, `write: []`, no clock (each case fixes its `booking_date`).
