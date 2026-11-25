# Build notes: miami-flight-policy (wave 3, 2026-11-24)

Built to `pilot_work/tier_plan/build/WAVE3_BUILD_BRIEF.md` from the frozen handbook
`pilot_work/originals/miami/frozen/miami_policy.txt` (University of Miami Travel Policy, PolicyStat ID 9607266,
effective 04/2021; 3,442 words, 289 lines, 23,362 characters, sha256 f05a964f...56c6fb02e; under 10,000 words, so 24
scenarios). Made with `_template/instantiate.py --slug miami --task-id book-miami-flight --currency USD --background 0
--scenarios 24`. The user was asleep; every choice below is the recommended one, taken without asking.

## Flight rules the handbook supports (frozen line numbers)

| Clause | Lines | Operator / kind | Used by |
|---|---|---|---|
| Prior approval of all travel by the supervisor and the supervising dean or VP; for faculty also Faculty Affairs (COVID-19 guidance) | 17-19 | mandatory | every trip record; thistle-pier (hold) |
| Travel authorized by the supervisor before arrangements; airfare through the Travel Portal | 34-37, 47-48, 112-114 | mandatory | every trip record |
| Always select the lowest fares available | 47-49 | general duty | accepted section on lowest-fare cases |
| Fly America: flights charged to federal awards on U.S. flag carriers | 58-59 | mandatory | pompano-ridge |
| Exceptions in advance by an EVP or designee | 60-63 | approver | accepted role on unclear holds |
| Domestic travel includes Guam, American Samoa, Puerto Rico, Virgin Islands | 74-76 | definition | brine-lattice |
| Lowest available fare within two hours of the desired departure or arrival time | 115-116 | "within" (inclusive; one case with wide margins, no twin) | heron-gable, lumen-bay |
| Lowest Logical Fare offered; $200 threshold | 117-118, 123, 128-129 | "within $200" inclusive | snook-larder, marlin-cove, every better-cabin case |
| Business reason required: fare $200 over the LLF; premium economy for flight under 4 hours; business/first for flight under 8 hours | 120-122 + 126-127 | "under" strict | ibis-quarry/osprey-quill, tarpon-mesa/manatee-reed, mangrove-lute, cypress-ember, kestrel-isle, vesper-tide, jasmine-shoal |
| Basic economy within policy within $200 | 130-134 | permission | not testable (see below) |
| Business trips normally commence one day before; up to one day after | 135-138 | "normally" | saffron-key (business day) |
| Personal extension: comparison non-refundable coach quote; reimbursement the lesser fare | 139-144 | mandatory | saffron-key |
| Connecting flights considered if savings exceed $200 and travel time grows by no more than two hours | 149-150 | "exceeds" strict, "not more than" inclusive; "should be considered" | pelican-arch, egret-sable/snook-larder, anhinga-dell/gannet-wold |
| International travel: the International Travel Approval policy's approvals before booking | 233-235 | mandatory | every trip abroad holds them; brine-lattice (not needed) |
| Companion payable only with a University position and a significant contribution | 269-272 | mandatory | lumen-bay, wren-hollow |
| University business only (scope, allowable expense, University Funds) | 26-31, 68-70, 106-107 | mandatory | ochre-fen |

Not tested, with reasons: basic economy (the shared `Offer` has no fare-brand field; template change request below);
price-match through Travel Incorporated and booking outside the portal (the agent is the portal; no decision field
for "send to the agency"); group travel of 10 or more through a Travel Incorporated agent (same reason; it appears as
a distractor in heron-gable); "Alternative Routing/Airports ... should be considered" (lesson 8: no record names an
alternate airport); the granting agency's own rules superseding the policy (lines 50-51; no slot left in the mix);
unused tickets, lodging, car rental. No overnight-stop rule exists, so no overnight overlay is required.

## Decisions taken (recommended choices)

1. **Bullets printed out of order.** Lines 120-122 belong under "An appropriate business reason will be required
   when booking:" (126-127), as the README of the frozen copy says. Read so, a better cabin is within policy without
   a reason only when the flight is not "under" the limit and the fare is within $200 of the lowest economy fare.
   Every booked better cabin (mangrove-lute, ibis-quarry, tarpon-mesa) is within $200 of the lowest economy fare, so
   the open question whether "lowest logical airfare" in line 120 means the lowest economy fare or the lowest fare of
   the cabin never matters. For business this needs a promotional business fare ($1,290 against $1,120 economy to
   Sao Paulo); the request says there is a promotion.
2. **Duration measure.** Scheduled minutes, strict "under": 240 and 480 are not under. A connection is clear only
   when every flight is at or past the limit (no reason needed on every reading) or the whole elapsed journey is
   short of it (needed on every reading); between is the jasmine-shoal flag. Background offers are 0 everywhere.
3. **What counts as an appropriate business reason.** Clear no: comfort (cypress-ember), a fare promotion
   (manatee-reed), airline status and miles (marlin-cove), no reason at all (osprey-quill). Clear yes: every economy
   seat that lands before the work begins is sold out (kestrel-isle). Open: work that must be done on board
   (vesper-tide, the flag). The classification is in `answer_key_inputs.reason_kind`, never shown.
4. **Connecting flights and the $200 tolerance work together.** Savings over $200 and no more than two hours added:
   the connection only, because the nonstop is then more than $200 over the lowest logical fare (needs a reason a
   preference is not). Savings under $200: the requested nonstop only (within the tolerance; permission not
   obligation, the request decides). Savings over $200 but more than two hours added: both (the connection need not
   be considered, yet the nonstop is still more than $200 over it). Exactly $200 is never used (line 120's "$200
   over" and line 123's "threshold of $200" meet there). Same departure time on every pair, so added elapsed time and
   later arrival agree.
5. **Time window.** "within two hours" read inclusive; in both window cases the flights that could change the answer
   are far from the edge (heron-gable: the cheaper 13:15 and 18:20 leave 315 and 620 minutes after 08:00; lumen-bay:
   the cheaper 06:15 and 13:50 leave 165 minutes before and 290 after 09:00), so no twin sits on the boundary.
6. **Trip approvals and rule 4'.** Staff: SUPERVISOR and VICE_PRESIDENT; academic staff and students: SUPERVISOR and
   DEAN; faculty: also FACULTY_AFFAIRS. A booking accepts NONE and every role on file; a refusal accepts NONE and the
   roles on file (wren-hollow's approvals are Dr. Ana Ruiz's own trip's); ochre-fen has none on file, so NONE only.
   thistle-pier accepts FACULTY_AFFAIRS only. Unclear holds accept NOT_NAMED, TRAVEL_MANAGEMENT (lines 102-104: the
   department responsible for the guidelines) and EXECUTIVE_VICE_PRESIDENT (exceptions, lines 62-63), plus SUPERVISOR
   for vesper-tide (the supervisor authorizes the trip and its business purpose, lines 47-48); never NONE. Being
   lenient there fails no correct answer.
7. **COVID-19 guidance (lines 17-19) is applied as written.** It is mandatory text in the frozen policy. Every record
   holds those approvals except thistle-pier, the one approval hold. Risk: a reader may treat the guidance as
   expired; the record then still shows that no Faculty Affairs approval exists.
8. **Fly America.** An NSF grant is a federal award (common usage; EDGE_CASES 3.9 lists this synonym). The hidden
   input says so. U.S. flag carriers are the U.S. airlines of the shared world. Codeshares are not modelled.
9. **Personal extension (saffron-key).** The ticket is the one the traveller will fly (Friday, November 27); the
   business day is November 30, the day before the conference (lines 135-136), across the month end; the comparison
   search on November 30 is pinned and cheaper, so the always-cheapest agent (which takes the cheapest offer of
   every pinned search) books the wrong day.
10. **Sections.** PolicyStat's headings are printed stacked or ahead of their text, so: preamble sentences accept
    PURPOSE, SCOPE, POLICY; lines 43-66 accept POLICY and DEFINITIONS; the air section accepts AIR_TRAVEL and
    PROCEDURE; lowest-fare bookings accept all four of AIR_TRAVEL, PROCEDURE, POLICY, DEFINITIONS; trips abroad also
    accept INTERNATIONAL_TRAVEL; companions BOOKING_FOR_OTHERS (and DEFINITIONS for the refusal).
11. **Reason codes.** Handbook codes: REQUESTED_TIME_WINDOW, FARE_WITHIN_TOLERANCE, BUSINESS_REASON_MISSING,
    BUSINESS_REASON_DOCUMENTED, FLY_AMERICA_US_CARRIER_REQUIRED, OPEN_SKIES_AGREEMENT, COMPANION_UNIVERSITY_ROLE,
    PERSONAL_EXTENSION_COMPARISON. Decoys (subjects grepped in the frozen text, none present): WEEKEND_TRAVEL_HOME,
    WEEKEND_TRIP_NOT_EARNED, CREATIVE_TICKETING, DENIED_BOARDING_NOT_ALLOWED, CHANCELLOR_WRITTEN_AUTHORIZATION,
    DOUBLE_BOOKING_PROHIBITED, SAME_CLASS_AS_CUSTOMER, TRAVEL_PACKAGE_NOT_ITEMIZED. Dropped: PRIVATE_AIRCRAFT_NOT_APPROVED
    (line 32 "team charters"), NEXT_OF_KIN_TRAVEL (family members in the companion clause), EXTENDED_TRAVEL_SAVINGS
    (line 139 "extended for personal travel"), CANDIDATE_TRIP_NOT_COVERED (job candidates are Travelers, line 95),
    AGENCY_EXEMPTION_NOT_MET (Travel Incorporated). Declined requests follow lesson 12 (README "Reasons on a declined
    request").
12. **No round trips.** Every case is one way; `return_date` is empty everywhere.
13. **Degenerate baselines.** Always-flag passes 2 (the two unclear holds); always-cheapest (LOWEST_FARE, NONE) passes
    7 of 24 (29%): anhinga-dell, brine-lattice, egret-sable, gannet-wold, marlin-cove, pelican-arch, sawgrass-loom.

## Hosted-cap estimate

0.2 tokens a character of policy plus 1,800 (Thornton/NJC paid calibration): call 1 about 6,500 input tokens, call 2
about 7,100, call 3 8,000-9,300 (2 to 9 offers); a 3-call run about 22,000-23,000 input tokens, about 33,000 with the
final message and output. Under the 65,536 hosted cap with room for three or four extra tool calls.

## Blind read (non-flag scenarios), from the handbook text and the tool outputs only

I dumped `get_trip` and every pinned `search_flights` output (all listed offers; background is 0) and re-derived each
answer from the frozen text, not from rules.py.

| Scenario | My reading | Agrees |
|---|---|---|
| anhinga-dell | DL via ATL $325 vs AA nonstop $585: saves $260, lands 120 min later (440 vs 320 elapsed), not more than two hours: connection; the nonstop is $260 over the LLF and a preference is no business reason | yes |
| brine-lattice | San Juan is domestic (74-76), so no international approvals needed: cheapest AA 12:35 $189 | yes |
| cypress-ember | 280-min nonstops, business under 8 h needs a business reason, comfort is not: AA 12:30 economy $298 | yes |
| egret-sable | DL via ATL $270 vs AA nonstop $471: saves $201 (> $200), +95 min: connection | yes |
| gannet-wold | saves $260 but +125 min: outside the connection test, nonstop still $260 over: either | yes |
| heron-gable | desired 08:00: 06:40/08:30/09:50 within two hours, cheapest UA 08:30 $231; 13:15 and 18:20 outside | yes |
| ibis-quarry | 240 min is not under 4 h; cheapest PE UA $462 is $157 over economy $305: UA premium economy | yes |
| kestrel-isle | presentation 16:00 LAX; economy sold out on the 07:00/09:30/11:00 (land 09:30/12:00/13:30), later flights land after 16:00; sold-out coach is a business reason: DL 11:00 business $1,380 | yes |
| lumen-bay | wife is a University research scientist who co-presents (269-272): payable; desired 09:00, 07:20 and 10:40 inside, cheapest 10:40 $229 | yes |
| manatee-reed | 479 min is under 8 h; a fare promotion is no business reason: LATAM economy $1,120 | yes |
| mangrove-lute | 345-min nonstops; cheapest PE AA $612, $157 over economy $455: AA premium economy | yes |
| marlin-cove | AA $444 is $230 over Delta $214; status/miles no business reason (points clause 145-146 a distractor): Delta | yes |
| ochre-fen | a cousin's wedding is personal, not University business: REFUSE | yes |
| osprey-quill | 239 min is under 4 h, no reason given: UA economy $305 | yes |
| pelican-arch | DL via ATL $298 vs AA nonstop $548: saves $250, +110 min, traveller open to connecting: connection | yes |
| pompano-ridge | NSF grant is a federal award: U.S. flag carrier only, AA $1,020 (VS $760, BA $795 out) | yes |
| saffron-key | personal weekend first; book the Friday flight (B6 $289) with the Monday Nov 30 comparison quote (B6 $214); reimbursement the lesser | yes |
| sawgrass-loom | economy asked: Iberia $690; international approvals on file | yes |
| snook-larder | saves only $199: nonstop requested and within $200: AA nonstop $471 | yes |
| tarpon-mesa | 480 min is not under 8 h; business AA $1,290 is $170 over economy $1,120: AA business | yes |
| wren-hollow | husband has no University position, holiday: REFUSE (269-272) | yes |

All 21 non-flag scenarios agree. Least certain (two-reader risk): the three booked better cabins (mangrove-lute,
ibis-quarry, tarpon-mesa), where a strict reader of line 49 ("always selecting the lowest fares available") might book
economy despite the $200 threshold and the bullets' exemption; gannet-wold (accept both by design); saffron-key (a
reader might book the Monday business-day fare, which the traveller will not fly); thistle-pier (a reader may treat the
COVID-19 guidance as lapsed).

## Template change requests

1. A fare-brand field on the shared `Offer` (e.g. `basic_economy: bool`) would let handbooks with basic-economy rules
   (Miami lines 130-134, and VT) test them. Not needed for this build.
2. As FedEx noted: the shared duration hook models absolute limits only; the connection's "travel time" increase is
   coded as constants in rules.py and tested through its twin pair.

## Acceptance outputs (final)

```
$ uv run pytest -q
213 passed in 2.04s
$ uv run ruff check .
All checks passed!
$ uv lock --check
Resolved 42 packages in 9ms
$ python3 ../_template/check_shared.py .
: ok
$ nanoagent plugin inspect .  (stock checkout)
exit 0
$ nanoagent plugin pack . /tmp/miami-flight-policy.tar.gz  (stock checkout)
packed . into /tmp/miami-flight-policy.tar.gz (166974 bytes)
$ python ../_template/tools/stock_verify.py .  (stock checkout Python)
anhinga-dell         right=True score=1.00 identical=True wrong-decision-rejected=True
brine-lattice        right=True score=1.00 identical=True wrong-decision-rejected=True
cypress-ember        right=True score=1.00 identical=True wrong-decision-rejected=True
egret-sable          right=True score=1.00 identical=True wrong-decision-rejected=True
gannet-wold          right=True score=1.00 identical=True wrong-decision-rejected=True
heron-gable          right=True score=1.00 identical=True wrong-decision-rejected=True
ibis-quarry          right=True score=1.00 identical=True wrong-decision-rejected=True
jasmine-shoal        right=True score=1.00 identical=True wrong-decision-rejected=True
kestrel-isle         right=True score=1.00 identical=True wrong-decision-rejected=True
lumen-bay            right=True score=1.00 identical=True wrong-decision-rejected=True
manatee-reed         right=True score=1.00 identical=True wrong-decision-rejected=True
mangrove-lute        right=True score=1.00 identical=True wrong-decision-rejected=True
marlin-cove          right=True score=1.00 identical=True wrong-decision-rejected=True
ochre-fen            right=True score=1.00 identical=True wrong-decision-rejected=True
osprey-quill         right=True score=1.00 identical=True wrong-decision-rejected=True
pelican-arch         right=True score=1.00 identical=True wrong-decision-rejected=True
pompano-ridge        right=True score=1.00 identical=True wrong-decision-rejected=True
saffron-key          right=True score=1.00 identical=True wrong-decision-rejected=True
sawgrass-loom        right=True score=1.00 identical=True wrong-decision-rejected=True
snook-larder         right=True score=1.00 identical=True wrong-decision-rejected=True
tarpon-mesa          right=True score=1.00 identical=True wrong-decision-rejected=True
thistle-pier         right=True score=1.00 identical=True wrong-decision-rejected=True
vesper-tide          right=True score=1.00 identical=True wrong-decision-rejected=True
wren-hollow          right=True score=1.00 identical=True wrong-decision-rejected=True
24 scenarios, 0 failures
```
