# Independent audit: miami-flight-policy (2026-11-25, wave 3)

I audited the builder's commit cac7d69 against `pilot_work/tier_plan/build/WAVE3_AUDIT_BRIEF.md`,
`WAVE3_BUILD_BRIEF.md` (lessons 1-12), MASTER_PLAN section 4, EDGE_CASES 1-3 and 5, and the worked audits
(fedex-office, goodman-networks, hillrom, georgia-sao). I spent no money and pushed nothing. Line numbers refer to
the frozen handbook `src/plugin/data/policy.txt`.

## Method

I printed every `get_trip` record and every pinned `search_flights` result through the plugin's own tools. I
answered each case from the handbook text and those outputs only. Then I compared my answers with every accept set:
decision, offer, cabin, reason, approver and clause.

## Verdict

**Pass after fixes.** On all 21 non-flag cases, the key's decision and offer agree with my own reading.

- The two unclear flags are genuinely open.
  - `jasmine-shoal`: "flight under 4 hours" is unclear for a connection whose segments are each under 4 hours but
    whose journey is longer.
  - `vesper-tide`: it is unclear whether grant writing on board is an "appropriate business reason".
  - Each flag accepts the held offer of both readings, and each has clear twins on both sides.
- The decline sentence is in the task instructions.
- No request uses rule wording (no "$200", no "4 hours", no "lowest logical").
- The boundary twins each differ in one fact:
  - ibis-quarry/osprey-quill: 240 vs 239 minutes.
  - tarpon-mesa/manatee-reed: 480 vs 479 minutes.
  - egret-sable/snook-larder: $201 vs $199 saved.
  - anhinga-dell/gannet-wold: layover 85 vs 90 minutes.
  - lumen-bay/wren-hollow: whether the spouse holds a University role.
- Every keyed booking satisfies every constraint the handbook states.

The defects were the approval hold's dependence on the COVID-19 text, and some reason and clause sets that were
too narrow.

## The builder's open items, settled

1. **Out-of-order bullets (lines 120-122 printed above 126-127). Kept: they belong under "An appropriate business
   reason will be required when booking:".**
   - Lines 126-127 end in a colon with nothing after them.
   - Line 128 restates the first bullet in the same sense.
   - Read at their printed position, the bullets do not parse: they split "Travelers are expected to make ...
     reservations within the lowest airfare available threshold of $200".
   - On any reading the bullets list what falls outside the default expectation. None of them reaches a premium
     economy flight of 4 hours or more, or a business flight of 8 hours or more, when the fare is within $200. So no
     key turns on where the bullets go.
2. **mangrove-lute, ibis-quarry and tarpon-mesa book the requested better cabin. Kept as the only answer; economy is
   not added.** A careful reader does not decline these requests on the strength of line 49, for four reasons:
   - The specific rules make a fare within $200 of the lowest logical airfare a booking within policy that needs no
     justification. Line 123 says "expected to make reservations within the lowest airfare available threshold of
     $200". Line 128 limits the justification to "Bookings which are not the lowest airfare available or $200
     within the lowest logical airfare". Lines 130-131 say "within Travel Policy when ... within $200".
   - The bullets ask for a business reason only for premium economy "under 4 hours" and business "under 8 hours".
     If line 49 barred every better cabin, those limits would have no purpose. Line 126 adds that the portal "includes
     all ticket class options".
   - Line 49 ("always selecting the lowest fares available") is the general prudence statement of the definitions
     preamble. The $200 tolerance is the operative rule that puts it into practice.
   - The traveller asks for the cabin. Two requests say "if the policy allows it", and it does. The project rule is
     that permission is not obligation and the request decides (EDGE_CASES 3.17). Every other plugin keys granted
     premium cabins the same way.

   Accepting economy would also raise the always-cheapest baseline from 7 to 10 of 24 (42%), past the limit. For the
   same reason, `snook-larder` (nonstop requested, $199 saved) keeps the nonstop only. Below $200 the connection need
   not be considered (lines 149-150), and the nonstop is within the tolerance.
3. **COVID-19 approvals (lines 17-19). The lapsed reading is defensible, so `thistle-pier` was reworked.**
   - For the lapsed reading:
     - The paragraph labels itself COVID-19 guidance.
     - It ties the approvals to quarantine, testing and a "Return to Work Attestation".
     - It links to separate "full COVID-19 travel guidance".
     - It sits in a policy whose "Next Review: 04/2023" is four years before the 2027 trips.
     - The policy's own body states a standing approval rule that is narrower: the supervisor (lines 34-37, 47-48).
   - For applying it as written: "Current Status: Active" and "must".
   - Both readings are defensible. A hold that turns only on a missing Faculty Affairs approval therefore had two
     answers.
   - The rework: Dr. Adeyemi has nothing on file yet. The request now says "I haven't sent the trip to my chair for
     approval yet, but please book it now while the fares are low."
   - On every reading the supervisor's prior authorization is awaited. On the COVID reading the dean, or vice
     president, and Faculty Affairs are awaited too.
   - The key is still FLAG_FOR_APPROVAL of American $219 with APPROVAL_REQUIRED. Approvers are SUPERVISOR, DEAN,
     VICE_PRESIDENT and FACULTY_AFFAIRS (rule 4': only awaited roles, never NONE). Clauses add DEFINITIONS, because
     lines 47-48 are filed under it.
   - The id, category and flag twins are unchanged, and the world is unchanged apart from the empty `sign_offs`.
   - No other key depends on lines 17-19. Every BOOK accepts NONE and each role on file, so a reader who treats the
     guidance as lapsed still passes.
   - `rules.solve` now raises on missing approvals beside approvals on file, so no future case can turn on the
     COVID-only approvals.
4. **gannet-wold accepts either flight. Kept.**
   - The connection saves $260 but adds 125 minutes, which fails the "not more than two hours" limb of lines 149-150.
     So the connection need not be considered, and the requested nonstop can be the lowest logical fare.
   - Yet the nonstop is still more than $200 over the cheaper fare (line 120), so the connection is defensible too.
   - The twin `anhinga-dell` (120 minutes, inclusive) keys the connection only, so the pair still tests the boundary.
5. **saffron-key: book the Friday flight. Kept as the only offer.**
   - Lines 139-144 allow a flight "extended for personal travel". They require a comparison quote for the business
     dates and limit reimbursement to the lesser fare.
   - The ticket is therefore the one the traveller flies: JetBlue on Friday, November 27, at $289. The Monday,
     November 30 fare of $214 is the comparison quote, not the purchase.
   - A Monday ticket is a flight she will not take, and the request explicitly asks for Friday. Nothing in the text
     makes the University buy the comparison fare. No approval is pending, so a hold is not defensible either.

## Defects found and fixed

| Scenario | Problem | Fix |
|---|---|---|
| `thistle-pier` | The hold turned only on the COVID-19 Faculty Affairs approval (lines 17-19), which a careful reader may treat as lapsed (see item 3) | Nothing is on file and the request says the chair has not been asked. The hold awaits the supervisor on every reading. Approvers are SUPERVISOR, DEAN, VICE_PRESIDENT and FACULTY_AFFAIRS. Clauses add DEFINITIONS. must_keep adds lines 47-48 |
| `anhinga-dell`, `egret-sable`, `gannet-wold` | Booking the connection declines the requested nonstop. The handbook's ground is that a nonstop more than $200 over needs a business reason, which a preference is not (lines 120, 126-129). BUSINESS_REASON_MISSING was not accepted (lessons 5 and 12) | BUSINESS_REASON_MISSING added (only where the nonstop was requested, so `pelican-arch` is unchanged) |
| `kestrel-isle`, `saffron-key` | LOWEST_FARE was accepted, but the lowest-fare sections (POLICY and DEFINITIONS for lines 47-49) were not, unlike every other lowest-fare booking (builder's decision 10) | Clauses are now AIR_TRAVEL, DEFINITIONS, POLICY and PROCEDURE |
| `ochre-fen` | A refusal of a personal flight may fairly cite the air section (lines 112-114: airfare paid by University Funds that is an Allowable Expense) | AIR_TRAVEL and PROCEDURE added |
| `wren-hollow` | A spouse on holiday is outside the policy's University-business scope. OUTSIDE_POLICY_SCOPE is a fair reason, and `ochre-fen` already accepts it | OUTSIDE_POLICY_SCOPE added |

The changes are in `src/plugin/rules.py` (with `verifier/rules.py` copied over it and byte-identical), in
`tests/build_scenarios.py`, and in the regenerated scenario JSON. I updated the README table rows and the prose on
approvals, declined-nonstop reasons and the approval hold.

## Seen and kept

- **`heron-gable` (cheapest UA 08:30 at $231 within two hours of 08:00).** The $169 flight at 18:20 still lands
  before the Friday poster. But lines 115-116 direct the lowest fare within two hours of the desired time, and that
  is the careful answer. The other in-window flights ($244 and $252) are not the lowest, so they stay rejected.
  `lumen-bay` follows the same pattern.
- **`pompano-ridge`.** The text says "U.S. flag air carriers". Only British and Virgin Atlantic undercut American,
  and both are UK airlines. So the outside fact that the US-EU Open Skies agreement admits EU airlines cannot change
  the answer, and the key follows the text.
- **`manatee-reed`.** A fare promotion is no business reason. Business on a 479-minute flight needs one under
  bullet 3 even though the fare is within $200. The two bullets are independent conditions.
- **`kestrel-isle`.** The Delta 11:00 business fare at $1,380 is the lowest fare that lands before 16:00. Economy
  is sold out on every flight that arrives in time, which is clearly an appropriate business reason.
- **Unclear-flag approvers** (NOT_NAMED, TRAVEL_MANAGEMENT, EXECUTIVE_VICE_PRESIDENT, plus SUPERVISOR on
  `vesper-tide`). These are generous enough, and never NONE.

## Baselines

- Always-cheapest (cheapest seated offer, LOWEST_FARE, NONE): **MAX_PASS_ALWAYS_LOWEST 7 -> 7** (29%). It passes
  `anhinga-dell`, `brine-lattice`, `egret-sable`, `gannet-wold`, `marlin-cove`, `pelican-arch` and `sawgrass-loom`.
  I recounted this through the verifier.
- Always-flag: 2 (`jasmine-shoal`, `vesper-tide`). `thistle-pier` does not accept NOT_NAMED.

## Acceptance outputs (after the fixes)

```
$ uv run pytest -q
213 passed
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages in 8ms
$ python3 ../_template/check_shared.py .
: ok
$ <stock python> ../_template/tools/stock_verify.py .
24 scenarios, 0 failures (every scenario right=True score=1.00 identical=True wrong-decision-rejected=True)
$ <stock nanoagent> plugin inspect .
exit 0
$ cmp src/plugin/rules.py verifier/rules.py
identical
```
