"""The handbook-specific settings the template's acceptance tests read. Every other file in tests/ is the
template's and stays identical across plugins (see TEMPLATE_GUIDE.md)."""

from pathlib import Path

import contract

ROOT = Path(__file__).resolve().parents[1]

# Ids that are published or taken: a new plugin never reuses one (MASTER_PLAN section 4, "id check").
PUBLISHED_IDS = {
    "aiib-delegation-entitlement", "ec-mission-cabin-allowance", "ftr-city-pair-fare-selection",
    "gates-vendor-flight-ranking", "njc-cabin-meal-allowance", "sfc-travel-preapproval", "uc-g28-expense-audit",
    "un-staff-air-travel-audit", "vt-airfare-policy-booking", "wa-saam-travel-versioned-audit",
    "energy-corporate-flight-booking", "pharma-distributor-flight-booking", "shipping-company-flight-booking",
    "telecommunications-flight-booking", "preference-aware-flight-booking", "llm-context-compress",
    "weather-alert", "word-check", "arxiv-source",
}

# The frozen original's SHA256SUMS, when this checkout sits beside pilot_work/ (skipped elsewhere).
FROZEN_SHA256SUMS = ROOT.parents[1] / "pilot_work" / "originals" / "miami" / "frozen" / "SHA256SUMS"

# Scenario mix by primary category (EDGE_CASES.md section 5.2; the 24-scenario row).
MIX = {"easy": 5, "boundary_twin": 6, "multi_rule": 4, "hidden_clause": 2, "distractor": 2, "refusal": 2, "flag": 3}

# Overlay minimums (EDGE_CASES.md section 5.3) for the rules this handbook has. It has no overnight-stop rule.
OVERLAY_MINIMUMS = {
    "multi_leg": 3, "date_arithmetic": 2, "month_end": 1, "personal_travel": 1, "multi_traveller": 1,
    "dearer_option": 2, "upgrade_not_taken": 2, "outside_air_section": 2,
}

# Words a scenario id may not contain beyond the template's universal list: this handbook's rule and role
# terms.
ID_FORBIDDEN_TERMS = {
    "premium", "comfort", "business", "economy", "coach", "basic", "first", "spouse", "husband", "wife", "family",
    "companion", "personal", "vacation", "holiday", "wedding", "supervisor", "dean", "faculty", "affairs", "vice",
    "president", "executive", "nonstop", "direct", "connection", "connecting", "layover", "savings", "window",
    "portal", "federal", "grant", "nsf", "america", "flag", "carrier", "domestic", "international", "territory",
    "puerto", "rico", "group", "reason", "justification", "status", "miles", "points", "loyalty", "sold", "student",
    "staff", "professor", "covid", "approval", "quote", "extension", "tolerance", "lowest", "fare",
}

# The handbook-specific enums whose member words a scenario id may not contain either.
ID_CATEGORY_ENUMS = [contract.Passenger, contract.Purpose, contract.Routing, contract.SignOffSubject,
                     contract.UniversityRole]

# How many scenarios a degenerate agent may pass: one that always holds the right offer for approval, and
# one that always books the cheapest seat (with the right section).
MAX_PASS_ALWAYS_FLAG = 2
MAX_PASS_ALWAYS_LOWEST = 7

# Hand-built duration cases beyond the automatic both-sides tests: (rule, outbound scheduled minutes per
# flight, layovers, expected True / False / None for unclear). True: at or past the limit, so the better
# cabin needs no business reason.
DURATION_CASES = [
    ("premium-economy", [240], [], True),
    ("premium-economy", [239], [], False),
    ("premium-economy", [110, 200], [60], None),  # each flight under, journey over: unclear
    ("premium-economy", [170, 120], [65], None),
    ("premium-economy", [250, 100], [60], None),  # one flight under: per flight, that flight is under
    ("premium-economy", [240, 245], [60], True),  # every flight at or past the limit: every reading agrees
    ("premium-economy", [100, 80], [55], False),  # journey of 235 elapsed minutes: under on every reading
    ("premium-economy", [120, 60], [59], False),  # 239 elapsed minutes
    ("business", [480], [], True),
    ("business", [479], [], False),
    ("business", [300, 250], [90], None),
    ("business", [200, 200], [60], False),
    ("business", [480, 500], [90], True),
]
