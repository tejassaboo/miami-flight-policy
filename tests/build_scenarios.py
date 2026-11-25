"""Writes the University of Miami scenario JSON files (an authoring aid, not a test; the JSON files are the truth).

    uv run python tests/build_scenarios.py

Expected answers are hand-written here; tests/test_scenarios.py checks them against rules.solve.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = (ROOT / "src/plugin/data/policy.txt").read_text(encoding="utf-8").split("\n")
OUT = ROOT / "src/plugin/data/scenarios"


def norm(text):
    return " ".join(text.split())


def keep(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    quote = text if quote is None else quote
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "sha256": hashlib.sha256(text.encode()).hexdigest(), "quote": quote, "why": why}


def aside(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "quote": quote, "why": why}


# ----- clauses the answers rest on -----
COVID = keep(17, 19, "All University-related travel must receive prior approval by the faculty or staff member's "
             "supervisor and the supervising dean or vice president. For faculty, approval must also be received from "
             "Faculty Affairs", "prior approval by the supervisor and the dean or VP; for faculty also Faculty Affairs")
AUTHORIZED = keep(34, 37, "the travel should be discussed and authorized by the supervisor prior to making travel "
                  "arrangements. When business travel is required and authorized, airfare reservations must be made "
                  "through the University of Miami Travel Portal", "the supervisor authorizes the trip before booking")
SUPERVISOR_FIRST = keep(47, 48, "secure approval from appropriate supervisor(s) prior to committing University funds or "
                        "incurring expenses", "approval from the supervisor before University funds are committed")
SCOPE = keep(26, 31, None, "the policy covers travel on University business")
PRUDENT = keep(47, 49, "Travelers are to exercise prudency when making travel reservations by always selecting the "
               "lowest fares available.", "the general duty: the lowest fares available")
FLY_AMERICA = keep(58, 59, None, "flights charged to federal awards are booked with U.S. flag air carriers")
ALLOWABLE = keep(68, 70, None, "an allowable expense is incurred for the primary benefit of university business")
COMPANION_DEF = keep(71, 72, None, "a companion is someone accompanying the person on University business")
DOMESTIC = keep(74, 76, None, "domestic travel includes U.S. possessions and territories such as Puerto Rico")
FUNDS = keep(106, 107, None, "University Funds")
WINDOW = keep(115, 116, None, "the lowest available fare within two hours of the desired departure or arrival time")
LLF = keep(117, 118, None, "the portal offers the Lowest Logical Fare")
OVER_200 = keep(120, 120, "Airfare that is $200 over the lowest logical airfare", "a fare $200 over the lowest "
                "logical airfare needs a business reason")
PE_BULLET = keep(121, 121, "Premium Economy/Comfort Plus ticket for flight under 4 hours",
                 "premium economy under 4 hours needs a business reason")
BUS_BULLET = keep(122, 122, "First Class/Business Class ticket for flight under 8 hours",
                  "business or first under 8 hours needs a business reason")
THRESHOLD = keep(123, 123, "reservations within the lowest airfare available threshold of $200.",
                 "reservations are expected within $200 of the lowest airfare")
REASON = keep(126, 127, "An appropriate business reason will be required when booking:",
              "the lead-in of the three bullets printed above it")
WITHIN = keep(128, 129, None, "a fare not within $200 of the lowest logical airfare needs a justification")
COMMENCE = keep(135, 136, "Business trips normally commence one day before the conference/meeting",
                "the business day is the day before the conference")
PERSONAL = keep(139, 144, None, "a personal extension needs a comparison coach quote; reimbursement is the lesser fare")
CONNECT = keep(149, 150, None, "connections are considered when they save more than $200 and add no more than two hours")
INTL = keep(233, 235, None, "international travel needs the International Travel Approval policy's approvals")
COMPANION = keep(269, 272, None, "a companion is payable only with a University position and a significant contribution")
TRAVEL_MGMT = keep(102, 104, None, "the Travel Management Department is responsible for the guidelines")
EXCEPTIONS = keep(62, 63, None, "exceptions are approved in advance by an Executive Vice President or designee")

# ----- nearby clauses that must not change the answer -----
FREQUENT = aside(145, 146, "University Travelers can earn airline points for business travel",
                 "the traveller keeps the points, but that does not choose the fare")
GROUP = aside(79, 80, "For airfare Group Travel is when 10 or more people are all traveling together",
              "a group rule for ten or more; the traveller books alone")
AFTER = aside(136, 138, "the University may reimburse the traveler for expenses up to one day after the conference end "
              "date", "a rule for the end of the trip, not the flight out")
AIRBNB = aside(191, 192, "University employees are authorized to use Airbnb for business if stays are four (4) days or "
               "longer", "a lodging rule with a day count")
BASIC = aside(130, 134, "Basic Economy options are available on the University Travel Portal and are considered within "
              "Travel Policy when the airfare is within $200 of the lowest logical airfare.",
              "a fare-type rule; the cheapest fare stays in policy")
TI_PERSONAL = aside(99, 101, "Travel Incorporated primary purpose is to assist with the needs of employees and students "
                    "traveling on company business or personal reservations.",
                    "the agency may help with personal reservations, but the University does not pay for them")
UNUSED = aside(173, 174, "The unused ticket may not be used for personal travel.", "about unused tickets")

# ----- builders -----

STAFF = [("SUPERVISOR", "Supervisor"), ("VICE_PRESIDENT", "Vice President")]


def approvals(role, names, whose="the traveller's"):
    """The trip approvals on file for a University traveller (lines 17-19, 34-37)."""
    signers = {"SUPERVISOR": "supervisor", "DEAN": "dean", "VICE_PRESIDENT": "vice president",
               "FACULTY_AFFAIRS": "Faculty Affairs"}
    roles = {"FACULTY": ["SUPERVISOR", "DEAN", "FACULTY_AFFAIRS"], "STAFF": ["SUPERVISOR", "VICE_PRESIDENT"],
             "STUDENT": ["SUPERVISOR", "DEAN"], "ACADEMIC_STAFF": ["SUPERVISOR", "DEAN"]}[role]
    assert len(names) == len(roles), (role, names)
    return [{"role": r, "name": n, "subject": "TRIP",
             "covers": f"Approves {whose} trip in advance, as {signers[r]}"} for r, n in zip(roles, names)]


def trip(**fields):
    base = {
        "traveller_name": "", "traveller_title": "", "university_role": "STAFF", "passenger": "TRAVELLER",
        "accompanies": "", "companion_contribution": "", "origin": "MIA", "destination": "", "travel_date": "",
        "return_date": "", "booking_date": "", "business_starts": "", "purpose": "", "purpose_kind": "MEETING",
        "funding": "Department operating budget", "personal_days": "", "requested_cabin": "ECONOMY",
        "requested_routing": "ANY", "requested_airline": "", "desired_departure": "", "stated_reason": "",
        "abroad_approvals_on_file": False, "sign_offs": [],
    }
    unknown = set(fields) - set(base)
    assert not unknown, unknown
    base.update(fields)
    return base


def offer(slot, flight, cabin, cents, seats=True, refundable=False):
    data = {"slot": slot, "flight": flight, "cabin": cabin, "fare_cents": cents}
    if not seats:
        data["seats"] = False
    if refundable:
        data["refundable"] = True
    return data


def expected(decision, slots, cabins, reasons, approvers, clauses, phrase=""):
    return {"decision": decision, "offer_slots": sorted(slots), "cabins": sorted(cabins), "reason_codes": sorted(reasons),
            "approvers": sorted(approvers), "clauses": sorted(clauses), "unclear_phrase": phrase}


def search(origin, destination, date, flights, offers, name="main"):
    return {"name": name, "origin": origin, "destination": destination, "date": date, "return_date": "",
            "background": 0, "flights": flights, "offers": offers}


S = []


def scenario(id, category, overlays, request, trip_, searches, exp, must_keep, notes, twin_of="", twin_fact="",
             flag_twins=(), ambiguity="none", distractors=(), hidden=None):
    if isinstance(searches, dict):
        searches = [searches]
    data = {
        "id": id, "category": category, "overlays": list(overlays), "twin_of": twin_of, "twin_fact": twin_fact,
        "flag_twins": list(flag_twins), "ambiguity_note": ambiguity, "request": request, "trip": trip_,
        "world": {"searches": searches}, "expected": exp, "must_keep": list(must_keep),
        "distractors": list(distractors), "design_notes": notes,
    }
    if hidden:
        data["answer_key_inputs"] = hidden
    S.append(data)


def roles_of(signoffs):
    return sorted({"NONE", *(record["role"] for record in signoffs)})


LOWEST = ["AIR_TRAVEL", "DEFINITIONS", "POLICY", "PROCEDURE"]
CABIN = ["AIR_TRAVEL", "PROCEDURE"]
PREAMBLE = ["POLICY", "PURPOSE", "SCOPE"]
LOW_KEEP = [WINDOW, LLF, PRUDENT]
APPROVED = [COVID, AUTHORIZED]
CLEAR_CONNECTION = ["ALTERNATE_ROUTE_TOO_EXPENSIVE", "ALTERNATE_ROUTE_WITHIN_MARGIN", "COST_SAVINGS", "LOWEST_FARE"]
# A declined nonstop request: more than $200 over, the nonstop needs a business reason a preference is not (audit).
DECLINED_NONSTOP = sorted([*CLEAR_CONNECTION, "BUSINESS_REASON_MISSING"])
DECLINED = ["BUSINESS_REASON_MISSING", "LONG_FLIGHT_CONDITION_NOT_MET", "UPGRADE_NOT_ELIGIBLE"]
PE_OK = ["FARE_WITHIN_TOLERANCE", "PREMIUM_ECONOMY_ALLOWED", "UPGRADE_WITHIN_FARE_MARGIN"]
UNCLEAR = ["APPROVAL_REQUIRED", "UNCLEAR_POLICY_TEXT"]
UNCLEAR_ROLES = ["EXECUTIVE_VICE_PRESIDENT", "NOT_NAMED", "TRAVEL_MANAGEMENT"]

# ===== easy (5) =====

signed = approvals("STUDENT", ["Prof. Lena Ortiz", "Dean Marcus Hale"])
scenario(
    "heron-gable", "easy", [],
    "Hi, I'm presenting a poster at the materials science symposium in Chicago on Friday morning. Can you book me "
    "Miami to O'Hare on Thursday, March 11th? I'd like to leave around 8 in the morning.",
    trip(traveller_name="Priya Natarajan", traveller_title="PhD student, Materials Science", university_role="STUDENT",
         destination="ORD", travel_date="2027-03-11", booking_date="2027-02-08", business_starts="2027-03-12 09:00",
         purpose="Poster presentation at a materials science symposium in Chicago", purpose_kind="CONFERENCE",
         funding="Graduate School student travel award", desired_departure="08:00", sign_offs=signed),
    search("MIA", "ORD", "2027-03-11", {
        "early": {"carrier": "AA", "depart": "06:40"},
        "morning": {"carrier": "UA", "depart": "08:30"},
        "late-morning": {"carrier": "AA", "depart": "09:50"},
        "afternoon": {"carrier": "AA", "depart": "13:15"},
        "evening": {"carrier": "UA", "depart": "18:20"},
    }, [
        offer("early-economy", "early", "ECONOMY", 25200),
        offer("morning-economy", "morning", "ECONOMY", 23100),
        offer("late-morning-economy", "late-morning", "ECONOMY", 24400),
        offer("afternoon-economy", "afternoon", "ECONOMY", 17800),
        offer("evening-economy", "evening", "ECONOMY", 16900),
    ]),
    expected("BOOK", ["morning-economy"], ["ECONOMY"], ["LOWEST_FARE", "REQUESTED_TIME_WINDOW"], roles_of(signed),
             LOWEST),
    [WINDOW, LLF, *APPROVED],
    "The traveller wants to leave around 08:00. Lines 115-116: the lowest available fare within two hours of the desired "
    "departure time. The 06:40, 08:30 and 09:50 flights are within two hours; the cheapest of them is United 08:30 at "
    "$231. The 13:15 and 18:20 flights are cheaper but more than two hours from the desired time. Supervisor (advisor) "
    "and dean approvals are on file (lines 17-19, 34-37).",
    distractors=[GROUP])

signed = approvals("FACULTY", ["Prof. Alan Brooks", "Dean Ruth Okafor", "Dr. Helen Marsh"])
scenario(
    "mangrove-lute", "easy", ["dearer_option"],
    "Miami to Seattle on April 20th for the ocean sciences workshop that opens the next morning. Premium economy "
    "please.",
    trip(traveller_name="Dr. Tomas Rivera", traveller_title="Associate Professor, Ocean Sciences",
         university_role="FACULTY", destination="SEA", travel_date="2027-04-20", booking_date="2027-03-15",
         business_starts="2027-04-21 09:00", purpose="Ocean sciences methods workshop in Seattle",
         purpose_kind="CONFERENCE", funding="Department operating budget", requested_cabin="PREMIUM_ECONOMY",
         sign_offs=signed),
    search("MIA", "SEA", "2027-04-20", {
        "american": {"carrier": "AA", "depart": "08:15"},
        "alaska": {"carrier": "AS", "depart": "10:40"},
        "delta": {"carrier": "DL", "depart": "13:05"},
    }, [
        offer("american-economy", "american", "ECONOMY", 46800),
        offer("american-premium", "american", "PREMIUM_ECONOMY", 61200),
        offer("alaska-economy", "alaska", "ECONOMY", 45500),
        offer("alaska-premium", "alaska", "PREMIUM_ECONOMY", 64000),
        offer("delta-economy", "delta", "ECONOMY", 47900),
        offer("delta-premium", "delta", "PREMIUM_ECONOMY", 63500),
    ]),
    expected("BOOK", ["american-premium"], ["PREMIUM_ECONOMY"], PE_OK, roles_of(signed), CABIN),
    [PE_BULLET, REASON, THRESHOLD, WITHIN, *APPROVED],
    "Nonstops of 345 scheduled minutes: not under 4 hours, so premium economy needs no business reason (lines 121, "
    "126-127). The cheapest premium economy fare ($612) is $157 over the lowest economy fare ($455), within the $200 "
    "threshold (lines 123, 128-129), so it is within policy and the traveller asks for it.")

scenario(
    "pelican-arch", "easy", ["multi_leg"],
    "Can you book me Miami to Phoenix on May 4th for the site visit at the solar test facility the next morning? I "
    "don't mind connecting if it saves real money.",
    trip(traveller_name="Gabriel Soto", traveller_title="Research Engineer, Energy Institute",
         destination="PHX", travel_date="2027-05-04", booking_date="2027-04-05", business_starts="2027-05-05 08:30",
         purpose="Site visit at a solar test facility near Phoenix", purpose_kind="SITE_VISIT",
         sign_offs=(signed := approvals("STAFF", ["Nadia Castillo", "VP Robert Lin"]))),
    search("MIA", "PHX", "2027-05-04", {
        "nonstop": {"carrier": "AA", "depart": "08:00", "minutes": [315]},
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "08:00", "minutes": [110, 255], "layovers": [60]},
    }, [
        offer("nonstop-economy", "nonstop", "ECONOMY", 54800),
        offer("atlanta-economy", "atlanta", "ECONOMY", 29800),
    ]),
    expected("BOOK", ["atlanta-economy"], ["ECONOMY"], CLEAR_CONNECTION, roles_of(signed), LOWEST),
    [CONNECT, LLF, PRUDENT, *APPROVED],
    "The one-stop through Atlanta saves $250 against the nonstop and, leaving at the same time, lands 110 minutes later "
    "(elapsed 425 against 315): it saves more than $200 and adds no more than two hours (lines 149-150), so it is the "
    "lowest logical fare; the traveller is happy to connect.")

signed = approvals("STAFF", ["Carla Mendes", "VP Steven Park"])
scenario(
    "cypress-ember", "easy", [],
    "Miami to Las Vegas on June 8th for the campus facilities conference that starts the next morning. I'd like "
    "business class, I just find it a lot more comfortable. If the policy doesn't allow it, book what it allows; I "
    "have to be at the conference.",
    trip(traveller_name="Derek Foster", traveller_title="Director, Facilities Operations", destination="LAS",
         travel_date="2027-06-08", booking_date="2027-05-10", business_starts="2027-06-09 09:00",
         purpose="Campus facilities management conference in Las Vegas", purpose_kind="CONFERENCE",
         requested_cabin="BUSINESS", stated_reason="I find business class a lot more comfortable", sign_offs=signed),
    search("MIA", "LAS", "2027-06-08", {
        "morning": {"carrier": "AA", "depart": "07:15"},
        "midday": {"carrier": "AA", "depart": "12:30"},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 31900),
        offer("morning-business", "morning", "BUSINESS", 98000),
        offer("midday-economy", "midday", "ECONOMY", 29800),
        offer("midday-business", "midday", "BUSINESS", 104000),
    ]),
    expected("BOOK", ["midday-economy"], ["ECONOMY"], DECLINED, roles_of(signed), sorted({*CABIN, *LOWEST})),
    [BUS_BULLET, REASON, LLF, PRUDENT, *APPROVED],
    "Nonstops of 280 scheduled minutes: business class for a flight under 8 hours needs an appropriate business reason "
    "(lines 122, 126-127); comfort is not one. Book the lowest logical economy fare, American 12:30 at $298.",
    hidden={"reason_kind": "personal"})

signed = approvals("STAFF", ["Monica Reyes", "VP Daniel Cho"])
scenario(
    "sawgrass-loom", "easy", ["upgrade_not_taken", "date_arithmetic"],
    "Miami to Madrid on the evening of September 14th for the partner universities' registrars meeting, which starts "
    "on the 16th. Economy is fine for this one, the cheapest you can find.",
    trip(traveller_name="Elena Navarro", traveller_title="Associate Registrar", destination="MAD",
         travel_date="2027-09-14", booking_date="2027-07-26", business_starts="2027-09-16 09:00",
         purpose="Registrars meeting of the partner universities in Madrid", purpose_kind="MEETING",
         abroad_approvals_on_file=True, sign_offs=signed),
    search("MIA", "MAD", "2027-09-14", {
        "american": {"carrier": "AA", "depart": "16:40"},
        "iberia": {"carrier": "IB", "depart": "18:05"},
    }, [
        offer("american-economy", "american", "ECONOMY", 73500),
        offer("american-business", "american", "BUSINESS", 410000),
        offer("iberia-economy", "iberia", "ECONOMY", 69000),
        offer("iberia-business", "iberia", "BUSINESS", 380000),
    ]),
    expected("BOOK", ["iberia-economy"], ["ECONOMY"], ["LOWEST_FARE"], roles_of(signed),
             sorted({*LOWEST, "INTERNATIONAL_TRAVEL"})),
    [LLF, PRUDENT, INTL, *APPROVED],
    "Overnight nonstops of 540 scheduled minutes, landing on the 15th. The traveller asks for the cheapest economy fare; "
    "the business cabin is not taken. The international approvals are on file (lines 233-235). Book Iberia at $690.",
    distractors=[aside(122, 122, "First Class/Business Class ticket for flight under 8 hours",
                       "a cabin the traveller does not ask for")])

# ===== boundary twins (6) =====

DEN_SIGNED = approvals("STAFF", ["Angela Pruitt", "VP Robert Lin"])
DEN_REQUEST = ("Miami to Denver on May 17th for the research computing workshop that starts the next morning. Premium "
               "economy please, if the policy allows it; otherwise book what it allows. I have to be at the workshop.")


def den_trip():
    return trip(traveller_name="Marcus Bell", traveller_title="Research Computing Analyst", destination="DEN",
                travel_date="2027-05-17", booking_date="2027-04-12", business_starts="2027-05-18 09:00",
                purpose="Research computing workshop in Denver", purpose_kind="CONFERENCE",
                requested_cabin="PREMIUM_ECONOMY", sign_offs=DEN_SIGNED)


def den(minutes):
    return search("MIA", "DEN", "2027-05-17", {
        "american": {"carrier": "AA", "depart": "07:10", "minutes": [minutes]},
        "united": {"carrier": "UA", "depart": "09:25", "minutes": [minutes]},
    }, [
        offer("american-economy", "american", "ECONOMY", 31800),
        offer("american-premium", "american", "PREMIUM_ECONOMY", 46800),
        offer("united-economy", "united", "ECONOMY", 30500),
        offer("united-premium", "united", "PREMIUM_ECONOMY", 46200),
    ])


scenario(
    "ibis-quarry", "boundary_twin", ["dearer_option"], DEN_REQUEST, den_trip(), den(240),
    expected("BOOK", ["united-premium"], ["PREMIUM_ECONOMY"], PE_OK, roles_of(DEN_SIGNED), CABIN),
    [PE_BULLET, REASON, THRESHOLD, WITHIN, *APPROVED],
    "Both nonstops are scheduled at exactly 240 minutes: not 'under 4 hours' (line 121), so premium economy needs no "
    "business reason; the cheapest premium economy fare ($462) is $157 over the lowest economy fare ($305), within $200 "
    "(lines 123, 128). Book it.",
    twin_of="osprey-quill", twin_fact="both nonstops scheduled at 240 or 239 minutes")

scenario(
    "osprey-quill", "boundary_twin", [], DEN_REQUEST, den_trip(), den(239),
    expected("BOOK", ["united-economy"], ["ECONOMY"], DECLINED, roles_of(DEN_SIGNED), sorted({*CABIN, *LOWEST})),
    [PE_BULLET, REASON, LLF, PRUDENT, *APPROVED],
    "Both nonstops are scheduled at 239 minutes: under 4 hours, so premium economy needs an appropriate business reason "
    "(lines 121, 126-127), and the traveller gives none. Book the lowest economy fare, United at $305.",
    twin_of="ibis-quarry", twin_fact="both nonstops scheduled at 240 or 239 minutes")

GRU_SIGNED = approvals("STAFF", ["Paula Ferreira", "VP Daniel Cho"])
GRU_REQUEST = ("Miami to Sao Paulo overnight on August 9th for the partner university visit, which starts on the "
               "11th. There's a promotion on business fares to Brazil right now, so business class please, if the "
               "policy allows it; otherwise book what it allows.")


def gru_trip():
    return trip(traveller_name="Rafael Costa", traveller_title="Director, International Partnerships",
                destination="GRU", travel_date="2027-08-09", booking_date="2027-06-21",
                business_starts="2027-08-11 09:00", purpose="Partnership visit to a university in Sao Paulo",
                purpose_kind="MEETING", requested_cabin="BUSINESS", abroad_approvals_on_file=True,
                sign_offs=GRU_SIGNED)


def gru(minutes):
    return search("MIA", "GRU", "2027-08-09", {
        "american": {"carrier": "AA", "depart": "21:30", "minutes": [minutes]},
        "latam": {"carrier": "LA", "depart": "23:10", "minutes": [minutes]},
    }, [
        offer("american-economy", "american", "ECONOMY", 118000),
        offer("american-business", "american", "BUSINESS", 129000),
        offer("latam-economy", "latam", "ECONOMY", 112000),
        offer("latam-business", "latam", "BUSINESS", 131000),
    ])


scenario(
    "tarpon-mesa", "boundary_twin", ["dearer_option"], GRU_REQUEST, gru_trip(), gru(480),
    expected("BOOK", ["american-business"], ["BUSINESS"],
             ["FARE_WITHIN_TOLERANCE", "INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED", "UPGRADE_WITHIN_FARE_MARGIN"],
             roles_of(GRU_SIGNED), sorted({*CABIN, "INTERNATIONAL_TRAVEL"})),
    [BUS_BULLET, REASON, THRESHOLD, WITHIN, INTL, *APPROVED],
    "Both nonstops are scheduled at exactly 480 minutes: not 'under 8 hours' (line 122), so business class needs no "
    "business reason; the cheapest business fare ($1,290) is $170 over the lowest economy fare ($1,120), within $200, so "
    "every reading of the lowest logical airfare agrees (lines 120, 123, 128). Book it.",
    twin_of="manatee-reed", twin_fact="both nonstops scheduled at 480 or 479 minutes")

scenario(
    "manatee-reed", "boundary_twin", [], GRU_REQUEST, gru_trip(), gru(479),
    expected("BOOK", ["latam-economy"], ["ECONOMY"], DECLINED, roles_of(GRU_SIGNED),
             sorted({*CABIN, *LOWEST, "INTERNATIONAL_TRAVEL"})),
    [BUS_BULLET, REASON, LLF, PRUDENT, INTL, *APPROVED],
    "Both nonstops are scheduled at 479 minutes: under 8 hours, so business class needs an appropriate business reason "
    "(lines 122, 126-127); a fare promotion is not one. Book the lowest economy fare, LATAM at $1,120.",
    twin_of="tarpon-mesa", twin_fact="both nonstops scheduled at 480 or 479 minutes")

MSP_SIGNED = approvals("ACADEMIC_STAFF", ["Prof. Karen Liu", "Dean Ruth Okafor"])
MSP_REQUEST = ("Miami to Minneapolis on October 5th for the planning retreat, which starts the next morning. I'd "
               "prefer the nonstop.")


def msp_trip():
    return trip(traveller_name="Jordan Pierce", traveller_title="Program Manager, School of Nursing", destination="MSP",
                travel_date="2027-10-05", booking_date="2027-09-07", business_starts="2027-10-06 09:00",
                purpose="Planning retreat with a partner nursing school in Minneapolis", purpose_kind="MEETING",
                requested_routing="NONSTOP", sign_offs=MSP_SIGNED)


def msp(connection_cents):
    return search("MIA", "MSP", "2027-10-05", {
        "nonstop": {"carrier": "AA", "depart": "08:00", "minutes": [210]},
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "08:00", "minutes": [110, 145], "layovers": [50]},
    }, [
        offer("nonstop-economy", "nonstop", "ECONOMY", 47100),
        offer("atlanta-economy", "atlanta", "ECONOMY", connection_cents),
    ])


scenario(
    "egret-sable", "boundary_twin", ["multi_leg"], MSP_REQUEST, msp_trip(), msp(27000),
    expected("BOOK", ["atlanta-economy"], ["ECONOMY"], DECLINED_NONSTOP, roles_of(MSP_SIGNED), LOWEST),
    [CONNECT, OVER_200, REASON, WITHIN, LLF, *APPROVED],
    "The connection saves $201 (more than $200) and lands 95 minutes after the nonstop (not more than two hours): it "
    "should be considered (lines 149-150) and is the lowest logical fare; the nonstop is more than $200 over it and "
    "needs a business reason (lines 120, 126-129), which a preference is not. Book the connection.",
    twin_of="snook-larder", twin_fact="connection fare 27000 or 27200 cents (saves 20100 or 19900 against the nonstop)")

scenario(
    "snook-larder", "boundary_twin", ["multi_leg", "dearer_option"], MSP_REQUEST, msp_trip(), msp(27200),
    expected("BOOK", ["nonstop-economy"], ["ECONOMY"],
             ["ALTERNATE_ROUTE_WITHIN_MARGIN", "FARE_WITHIN_TOLERANCE", "LOWEST_FARE"], roles_of(MSP_SIGNED), LOWEST),
    [CONNECT, THRESHOLD, WITHIN, LLF, *APPROVED],
    "The connection saves only $199: not more than $200, so it need not be considered (lines 149-150), and the "
    "requested nonstop is within $200 of the lowest fare, within policy (lines 123, 128-129). Book the nonstop.",
    twin_of="egret-sable", twin_fact="connection fare 27000 or 27200 cents (saves 20100 or 19900 against the nonstop)")

# ===== multi-rule (4) =====

SLC_SIGNED = approvals("STAFF", ["Brian Walsh", "VP Steven Park"])
SLC_REQUEST = ("Miami to Salt Lake City on November 2nd for the research administrators' training, which starts the "
               "next morning. I'd prefer the nonstop.")


def slc_trip():
    return trip(traveller_name="Lauren Kim", traveller_title="Grants Administrator, Office of Research",
                destination="SLC", travel_date="2027-11-02", booking_date="2027-10-04",
                business_starts="2027-11-03 09:00", purpose="Research administrators' training in Salt Lake City",
                purpose_kind="CONFERENCE", requested_routing="NONSTOP", sign_offs=SLC_SIGNED)


def slc(layover):
    return search("MIA", "SLC", "2027-11-02", {
        "nonstop": {"carrier": "AA", "depart": "07:30", "minutes": [320]},
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "07:30", "minutes": [110, 245], "layovers": [layover]},
    }, [
        offer("nonstop-economy", "nonstop", "ECONOMY", 58500),
        offer("atlanta-economy", "atlanta", "ECONOMY", 32500),
    ])


scenario(
    "anhinga-dell", "multi_rule", ["multi_leg"], SLC_REQUEST, slc_trip(), slc(85),
    expected("BOOK", ["atlanta-economy"], ["ECONOMY"], DECLINED_NONSTOP, roles_of(SLC_SIGNED), LOWEST),
    [CONNECT, OVER_200, REASON, WITHIN, LLF, *APPROVED],
    "The connection saves $260 and lands exactly 120 minutes after the nonstop (elapsed 440 against 320): not more than "
    "two hours, so it should be considered (lines 149-150) and is the lowest logical fare; the nonstop is $260 over it "
    "and needs a business reason (lines 120, 126-129). Book the connection.",
    twin_of="gannet-wold", twin_fact="layover 85 or 90 minutes (the connection lands 120 or 125 minutes after the nonstop)")

scenario(
    "gannet-wold", "multi_rule", ["multi_leg", "dearer_option"], SLC_REQUEST, slc_trip(), slc(90),
    expected("BOOK", ["atlanta-economy", "nonstop-economy"], ["ECONOMY"],
             ["ALTERNATE_ROUTE_TOO_EXPENSIVE", "ALTERNATE_ROUTE_WITHIN_MARGIN", "BUSINESS_REASON_MISSING",
              "CONNECTION_TOO_LONG", "COST_SAVINGS", "LOWEST_FARE"], roles_of(SLC_SIGNED), LOWEST),
    [CONNECT, OVER_200, REASON, LLF, *APPROVED],
    "The connection saves $260 but lands 125 minutes after the nonstop: more than two hours, outside the test of lines "
    "149-150, so the requested nonstop may be the lowest logical fare; it is also more than $200 over the cheaper "
    "connection (line 120). Both readings are defensible: the nonstop and the connection are both accepted.",
    twin_of="anhinga-dell", twin_fact="layover 85 or 90 minutes (the connection lands 120 or 125 minutes after the nonstop)")

signed = approvals("FACULTY", ["Prof. Alan Brooks", "Dean Ruth Okafor", "Dr. Helen Marsh"])
scenario(
    "kestrel-isle", "multi_rule", ["dearer_option"],
    "The dean asked me last night to present our proposal to the foundation board in Los Angeles tomorrow, March "
    "24th, at 4 pm. I've checked: economy is sold out on every flight that lands before then. Please book business "
    "on whatever gets me there in time.",
    trip(traveller_name="Dr. Sofia Alvarez", traveller_title="Professor, Public Health Sciences",
         university_role="FACULTY", destination="LAX", travel_date="2027-03-24", booking_date="2027-03-23",
         business_starts="2027-03-24 16:00", purpose="Proposal presentation to a foundation board in Los Angeles",
         purpose_kind="MEETING", requested_cabin="BUSINESS",
         stated_reason="Economy is sold out on every flight that lands before my 4 pm presentation", sign_offs=signed),
    search("MIA", "LAX", "2027-03-24", {
        "dawn": {"carrier": "AA", "depart": "07:00", "minutes": [330]},
        "morning": {"carrier": "AA", "depart": "09:30", "minutes": [330]},
        "late-morning": {"carrier": "DL", "depart": "11:00", "minutes": [330]},
        "afternoon": {"carrier": "AA", "depart": "15:30", "minutes": [330]},
        "evening": {"carrier": "AA", "depart": "17:45", "minutes": [330]},
    }, [
        offer("dawn-economy", "dawn", "ECONOMY", 38900, seats=False),
        offer("dawn-business", "dawn", "BUSINESS", 149000),
        offer("morning-economy", "morning", "ECONOMY", 36500, seats=False),
        offer("morning-business", "morning", "BUSINESS", 152000),
        offer("late-morning-economy", "late-morning", "ECONOMY", 35200, seats=False),
        offer("late-morning-business", "late-morning", "BUSINESS", 138000),
        offer("afternoon-economy", "afternoon", "ECONOMY", 34500),
        offer("afternoon-business", "afternoon", "BUSINESS", 129000),
        offer("evening-economy", "evening", "ECONOMY", 31900),
    ]),
    expected("BOOK", ["late-morning-business"], ["BUSINESS"],
             ["BUSINESS_REASON_DOCUMENTED", "LOWEST_FARE", "NO_ECONOMY_SEATS_URGENT"], roles_of(signed), LOWEST),
    [BUS_BULLET, REASON, LLF, *APPROVED],
    "The presentation starts at 16:00 in Los Angeles. The 07:00, 09:30 and 11:00 flights (330 minutes) land at 09:30, "
    "12:00 and 13:30 local; their economy seats are sold out. The 15:30 and 17:45 flights land after 16:00. Business "
    "class for a flight under 8 hours needs an appropriate business reason (lines 122, 126-127): no economy seat "
    "reaches the presentation, which is one. The lowest fare that lands in time is Delta business at $1,380.",
    hidden={"reason_kind": "economy_sold_out"})

signed = approvals("ACADEMIC_STAFF", ["Prof. Leah Grant", "Dean Ruth Okafor"])
LUMEN_WORLD = search("MIA", "PHL", "2027-04-07", {
    "dawn": {"carrier": "AA", "depart": "06:15"},
    "early": {"carrier": "AA", "depart": "07:20"},
    "late-morning": {"carrier": "AA", "depart": "10:40"},
    "afternoon": {"carrier": "AA", "depart": "13:50"},
}, [
    offer("dawn-economy", "dawn", "ECONOMY", 19800),
    offer("early-economy", "early", "ECONOMY", 24600),
    offer("late-morning-economy", "late-morning", "ECONOMY", 22900),
    offer("afternoon-economy", "afternoon", "ECONOMY", 20500),
])
scenario(
    "lumen-bay", "multi_rule", ["multi_traveller", "outside_air_section"],
    "Please book my wife, Dr. Ana Ruiz, Miami to Philadelphia on April 7th. She's a research scientist in our lab and "
    "co-presents our study with me at the cardiology symposium the next morning. We'd like to leave around 9 in the "
    "morning.",
    trip(traveller_name="Dr. Ana Ruiz", traveller_title="Research Scientist, Cardiology (wife of Prof. Mark Ruiz)",
         university_role="STAFF", passenger="COMPANION", accompanies="Prof. Mark Ruiz, her husband",
         companion_contribution="Co-presents the lab's study at the symposium", destination="PHL",
         travel_date="2027-04-07", booking_date="2027-03-08", business_starts="2027-04-08 09:00",
         purpose="Co-presenting a study at a cardiology symposium in Philadelphia", purpose_kind="CONFERENCE",
         desired_departure="09:00", sign_offs=signed),
    LUMEN_WORLD,
    expected("BOOK", ["late-morning-economy"], ["ECONOMY"],
             ["COMPANION_UNIVERSITY_ROLE", "LOWEST_FARE", "REQUESTED_TIME_WINDOW"], roles_of(signed),
             sorted({*LOWEST, "BOOKING_FOR_OTHERS"})),
    [COMPANION, WINDOW, LLF, *APPROVED],
    "A companion's expenses are payable only if the companion has a position with the University and travels to make "
    "a significant contribution (lines 269-272): Dr. Ruiz is a University research scientist who co-presents. The "
    "lowest fare within two hours of 09:00 (lines 115-116) is the 10:40 at $229; the 06:15 and 13:50 are cheaper but "
    "outside the window. Her own supervisor and dean approved her trip.",
    twin_of="wren-hollow", twin_fact="the spouse holds a University position and co-presents, or has none and goes "
    "along on holiday")

# ===== hidden clause (2) =====

signed = approvals("FACULTY", ["Prof. Irene Walsh", "Dean Paul Grant", "Dr. Helen Marsh"])
scenario(
    "pompano-ridge", "hidden_clause", ["synonym", "outside_air_section", "upgrade_not_taken"],
    "I'm presenting our NSF-funded coastal resilience results at a workshop in London; please book Miami to London "
    "Heathrow overnight on June 13th, charged to my NSF grant. Economy is fine. The workshop starts on the 15th.",
    trip(traveller_name="Dr. Kevin Osei", traveller_title="Associate Professor, Civil and Architectural Engineering",
         university_role="FACULTY", destination="LHR", travel_date="2027-06-13", booking_date="2027-04-26",
         business_starts="2027-06-15 09:00", purpose="Presenting research results at a coastal resilience workshop in "
         "London", purpose_kind="RESEARCH", funding="National Science Foundation research grant held by the traveller",
         abroad_approvals_on_file=True, sign_offs=signed),
    search("MIA", "LHR", "2027-06-13", {
        "american": {"carrier": "AA", "depart": "18:10", "minutes": [525]},
        "british": {"carrier": "BA", "depart": "19:00", "minutes": [530]},
        "virgin": {"carrier": "VS", "depart": "20:15", "minutes": [525]},
    }, [
        offer("american-economy", "american", "ECONOMY", 102000),
        offer("american-business", "american", "BUSINESS", 520000),
        offer("british-economy", "british", "ECONOMY", 79500),
        offer("virgin-economy", "virgin", "ECONOMY", 76000),
    ]),
    expected("BOOK", ["american-economy"], ["ECONOMY"], ["FLY_AMERICA_US_CARRIER_REQUIRED", "NATIONAL_CARRIER_REQUIRED",
                                                         "OPEN_SKIES_AGREEMENT"],
             roles_of(signed), ["DEFINITIONS", "INTERNATIONAL_TRAVEL", "POLICY"]),
    [FLY_AMERICA, INTL, *APPROVED],
    "An NSF grant is a federal award. Lines 58-59: flights charged to federal awards are booked with U.S. flag air "
    "carriers, so the cheaper Virgin Atlantic ($760) and British Airways ($795) fares are out; American at $1,020 is "
    "the only U.S. carrier. The clause sits among the policy statements, not in the air travel procedure.",
    hidden={"federal_award": True})

signed = approvals("STAFF", ["Luis Medina", "VP Daniel Cho"])
scenario(
    "brine-lattice", "hidden_clause", ["outside_air_section"],
    "Miami to San Juan on February 22nd, please, for the meeting with our Puerto Rico research partners the next "
    "morning.",
    trip(traveller_name="Isabel Cruz", traveller_title="Assistant Director, Sponsored Research", destination="SJU",
         travel_date="2027-02-22", booking_date="2027-01-25", business_starts="2027-02-23 09:00",
         purpose="Meeting with research partners in San Juan", purpose_kind="MEETING", sign_offs=signed),
    search("MIA", "SJU", "2027-02-22", {
        "morning": {"carrier": "AA", "depart": "08:10"},
        "midday": {"carrier": "AA", "depart": "12:35"},
        "orlando": {"carrier": "B6", "via": ["MCO"], "depart": "09:00", "layovers": [70]},
    }, [
        offer("morning-economy", "morning", "ECONOMY", 21400),
        offer("midday-economy", "midday", "ECONOMY", 18900),
        offer("orlando-economy", "orlando", "ECONOMY", 26900),
    ]),
    expected("BOOK", ["midday-economy"], ["ECONOMY"], ["LOWEST_FARE"], roles_of(signed),
             sorted({*LOWEST, "INTERNATIONAL_TRAVEL"})),
    [DOMESTIC, INTL, LLF, PRUDENT, *APPROVED],
    "No international approvals are on file, and none are needed: lines 74-76 define domestic travel as travel within "
    "the United States, its possessions and territories, including Puerto Rico, so the International Travel booking "
    "rule (lines 233-235) does not apply. Book the lowest fare, American 12:35 at $189.")

# ===== distractor (2) =====

signed = approvals("STAFF", ["Gloria Banks", "VP Steven Park"])
scenario(
    "marlin-cove", "distractor", [],
    "Miami to Detroit on March 2nd for the automotive research consortium review the next morning. Please put me on "
    "American: I have status there and the miles go to my account. If that isn't possible, book what the policy "
    "allows; I have to be at the review.",
    trip(traveller_name="Victor Hale", traveller_title="Director, Industry Partnerships", destination="DTW",
         travel_date="2027-03-02", booking_date="2027-02-01", business_starts="2027-03-03 09:00",
         purpose="Automotive research consortium review in Detroit", purpose_kind="MEETING",
         requested_airline="American Airlines",
         stated_reason="I have status with American and the miles go to my account", sign_offs=signed),
    search("MIA", "DTW", "2027-03-02", {
        "delta": {"carrier": "DL", "depart": "07:45"},
        "american": {"carrier": "AA", "depart": "08:30"},
        "american-later": {"carrier": "AA", "depart": "13:00"},
    }, [
        offer("delta-economy", "delta", "ECONOMY", 21400),
        offer("american-economy", "american", "ECONOMY", 44400),
        offer("american-later-economy", "american-later", "ECONOMY", 46800),
    ]),
    expected("BOOK", ["delta-economy"], ["ECONOMY"],
             ["BUSINESS_REASON_MISSING", "LOWEST_FARE", "LOYALTY_PROGRAM_PREFERENCE"], roles_of(signed), LOWEST),
    [OVER_200, REASON, WITHIN, THRESHOLD, LLF, *APPROVED],
    "The cheapest American fare is $230 over the lowest logical airfare (Delta $214): more than the $200 threshold, so "
    "it needs an appropriate business reason (lines 120, 123, 126-129). Airline status and miles are the traveller's "
    "own benefit; line 145-146 lets travellers earn points, not choose dearer fares. Book Delta.",
    distractors=[FREQUENT])

signed = approvals("STAFF", ["Nora Feld", "VP Daniel Cho"])
scenario(
    "saffron-key", "distractor", ["personal_travel", "date_arithmetic", "month_end"],
    "I'm speaking at the higher-education IT conference in Boston that opens Tuesday, December 1st at 8:30. I'd like "
    "to fly up the Friday before, November 27th, and spend the weekend with my sister first; I'll stay at her place. "
    "Please book the Friday flight from Miami.",
    trip(traveller_name="Hannah Brooks", traveller_title="Director, Academic Technology", destination="BOS",
         travel_date="2026-11-27", booking_date="2026-11-02", business_starts="2026-12-01 08:30",
         purpose="Speaking at a higher-education IT conference in Boston", purpose_kind="CONFERENCE",
         personal_days="A weekend with family in Boston before the conference", sign_offs=signed),
    [
        search("MIA", "BOS", "2026-11-27", {
            "jetblue": {"carrier": "B6", "depart": "07:30"},
            "american": {"carrier": "AA", "depart": "09:15"},
            "delta": {"carrier": "DL", "depart": "11:40"},
        }, [
            offer("friday-jetblue", "jetblue", "ECONOMY", 28900),
            offer("friday-american", "american", "ECONOMY", 31800),
            offer("friday-delta", "delta", "ECONOMY", 33500),
        ]),
        search("MIA", "BOS", "2026-11-30", {
            "jetblue": {"carrier": "B6", "depart": "08:00"},
            "american": {"carrier": "AA", "depart": "10:10"},
        }, [
            offer("monday-jetblue", "jetblue", "ECONOMY", 21400),
            offer("monday-american", "american", "ECONOMY", 22900),
        ], name="business-day"),
    ],
    expected("BOOK", ["friday-jetblue"], ["ECONOMY"], ["LOWEST_FARE", "PERSONAL_EXTENSION_COMPARISON",
                                                       "PERSONAL_TRAVEL_NOT_COVERED"],
             roles_of(signed), LOWEST),
    [PERSONAL, COMMENCE, *APPROVED],
    "The trip is extended for personal travel. Business trips normally commence one day before the conference (lines "
    "135-136): Monday, November 30. Lines 139-144: a comparison non-refundable coach quote for the business dates "
    "(JetBlue Monday $214) goes with the booking, and reimbursement is limited to the lesser fare. The flight the "
    "traveller will take is booked: JetBlue Friday at $289. The one-day-after and Airbnb day counts are distractors.",
    distractors=[AFTER, AIRBNB])

# ===== refusal (2) =====

signed = approvals("ACADEMIC_STAFF", ["Prof. Leah Grant", "Dean Ruth Okafor"], whose="Dr. Ana Ruiz's")
scenario(
    "wren-hollow", "refusal", ["multi_traveller", "personal_travel", "outside_air_section"],
    "Please book my husband, Daniel Ruiz, Miami to Philadelphia on April 7th. I'm co-presenting our lab's study at the "
    "cardiology symposium the next morning, and he's coming along to make a little holiday of it. We'd like to leave "
    "around 9 in the morning.",
    trip(traveller_name="Daniel Ruiz", traveller_title="Husband of Dr. Ana Ruiz", university_role="NO_UNIVERSITY_ROLE",
         passenger="COMPANION", accompanies="Dr. Ana Ruiz, his wife, a University research scientist",
         destination="PHL", travel_date="2027-04-07", booking_date="2027-03-08", business_starts="2027-04-08 09:00",
         purpose="Accompanying his wife to a cardiology symposium in Philadelphia", purpose_kind="CONFERENCE",
         funding="Charged with his wife's trip to the lab's operating budget", desired_departure="09:00",
         sign_offs=signed),
    LUMEN_WORLD,
    expected("REFUSE", [], ["NONE"], ["COMPANION_NOT_COVERED", "OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"],
             roles_of(signed),
             ["BOOKING_FOR_OTHERS", "DEFINITIONS"]),
    [COMPANION, COMPANION_DEF],
    "Lines 269-272: the expenses of a spouse accompanying the business traveller are not payable using University "
    "Funds unless the spouse has a position with the University and travels to make a significant contribution; Mr. "
    "Ruiz has neither. The University buys no ticket. The approvals on file are for Dr. Ana Ruiz's own trip (4(b)).",
    twin_of="lumen-bay", twin_fact="the spouse holds a University position and co-presents, or has none and goes "
    "along on holiday")

scenario(
    "ochre-fen", "refusal", ["personal_travel", "outside_air_section"],
    "Can you book me Miami to Denver on July 16th for my cousin's wedding? Put it on the department's travel card and "
    "I'll sort it out with them later.",
    trip(traveller_name="Kyle Jensen", traveller_title="IT Support Specialist", destination="DEN",
         travel_date="2027-07-16", booking_date="2027-06-14", business_starts="2027-07-17 16:00",
         purpose="A cousin's wedding in Denver", purpose_kind="PERSONAL",
         funding="The department's University Travel Card, to be repaid by the traveller"),
    search("MIA", "DEN", "2027-07-16", {
        "american": {"carrier": "AA", "depart": "08:20"},
        "united": {"carrier": "UA", "depart": "11:45"},
    }, [
        offer("american-economy", "american", "ECONOMY", 27800),
        offer("united-economy", "united", "ECONOMY", 25900),
    ]),
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"], ["NONE"],
             ["AIR_TRAVEL", "DEFINITIONS", "POLICY", "PROCEDURE", "PURPOSE", "SCOPE"]),
    [SCOPE, ALLOWABLE, FUNDS],
    "A wedding is personal travel, not University business. Lines 26-31: the policy covers travel on behalf of the "
    "University; lines 68-70: an allowable expense is incurred for the primary benefit of university business; lines "
    "106-107: University Funds. The University buys no ticket, card or not. Travel Incorporated may help with personal "
    "reservations (lines 99-101), but not on University funds.",
    distractors=[TI_PERSONAL, UNUSED])

# ===== flag (3) =====

signed = approvals("FACULTY", ["Prof. Alan Brooks", "Dean Ruth Okafor", "Dr. Helen Marsh"])
scenario(
    "vesper-tide", "flag", ["unclear_phrase"],
    "Miami to San Francisco on May 11th for the foundation site review the next morning. Business class please: I'll "
    "be writing the final sections of our grant renewal on the flight, it's due when the review starts, and I can't "
    "really work in economy. If the policy doesn't allow it, book what it allows.",
    trip(traveller_name="Dr. Grace Holloway", traveller_title="Professor, Biomedical Engineering",
         university_role="FACULTY", destination="SFO", travel_date="2027-05-11", booking_date="2027-04-12",
         business_starts="2027-05-12 09:00", purpose="Foundation site review of a research center in San Francisco",
         purpose_kind="RESEARCH", requested_cabin="BUSINESS",
         stated_reason="I need to write the final sections of the grant renewal on the flight; I can't work in economy",
         sign_offs=signed),
    search("MIA", "SFO", "2027-05-11", {
        "american": {"carrier": "AA", "depart": "08:05"},
        "united": {"carrier": "UA", "depart": "10:20"},
    }, [
        offer("american-economy", "american", "ECONOMY", 41200),
        offer("american-business", "american", "BUSINESS", 145000),
        offer("united-economy", "united", "ECONOMY", 39800),
        offer("united-business", "united", "BUSINESS", 139000),
    ]),
    expected("FLAG_FOR_APPROVAL", ["united-business", "united-economy"], ["BUSINESS", "ECONOMY"], UNCLEAR,
             [*UNCLEAR_ROLES, "SUPERVISOR"], CABIN, phrase="appropriate business reason"),
    [BUS_BULLET, REASON, TRAVEL_MGMT, EXCEPTIONS, *APPROVED],
    "Nonstops of 325 scheduled minutes: business class for a flight under 8 hours needs 'an appropriate business "
    "reason' (lines 122, 126-127), which the handbook never defines. Writing University work on board is a business "
    "task, but the wish is also about room to work. Hold the cheapest business fare (or the cheapest economy fare, the "
    "other reading's booking).",
    flag_twins=["cypress-ember", "kestrel-isle"],
    ambiguity={"phrase": "appropriate business reason",
               "readings": ["work for the University that has to be done on board is a business reason: business",
                            "the need is room to work, a comfort the traveller could plan around: economy"]},
    hidden={"reason_kind": "unclear"})

signed = approvals("STAFF", ["Angela Pruitt", "VP Robert Lin"])
scenario(
    "jasmine-shoal", "flag", ["unclear_phrase", "multi_leg"],
    "Miami to Denver on June 21st for the data science summer school, which starts the next morning. Premium economy "
    "please, if the policy allows it; otherwise book what it allows. I have to be there.",
    trip(traveller_name="Owen Pruitt", traveller_title="Data Scientist, Institute for Data Science", destination="DEN",
         travel_date="2027-06-21", booking_date="2027-05-24", business_starts="2027-06-22 09:00",
         purpose="Data science summer school in Denver", purpose_kind="CONFERENCE", requested_cabin="PREMIUM_ECONOMY",
         sign_offs=signed),
    search("MIA", "DEN", "2027-06-21", {
        "dallas": {"carrier": "AA", "via": ["DFW"], "depart": "07:40", "minutes": [170, 120], "layovers": [65]},
        "atlanta": {"carrier": "DL", "via": ["ATL"], "depart": "08:25", "minutes": [110, 200], "layovers": [60]},
    }, [
        offer("dallas-economy", "dallas", "ECONOMY", 33800),
        offer("dallas-premium", "dallas", "PREMIUM_ECONOMY", 49000),
        offer("atlanta-economy", "atlanta", "ECONOMY", 32400),
        offer("atlanta-premium", "atlanta", "PREMIUM_ECONOMY", 48800),
    ]),
    expected("FLAG_FOR_APPROVAL", ["atlanta-economy", "atlanta-premium"], ["ECONOMY", "PREMIUM_ECONOMY"], UNCLEAR,
             UNCLEAR_ROLES, CABIN, phrase="flight under 4 hours"),
    [PE_BULLET, REASON, THRESHOLD, TRAVEL_MGMT, EXCEPTIONS, *APPROVED],
    "Only connections are listed. Each flight is under 4 hours (110 and 200 minutes through Atlanta, 170 and 120 "
    "through Dallas), but each journey is not (310 and 290 minutes flying, 370 and 355 elapsed). Line 121 needs a "
    "business reason for premium economy on a 'flight under 4 hours' and does not say whether a connection is one "
    "flight or several. The cheapest premium economy fare is $164 over the lowest economy fare (within $200). Hold "
    "Delta premium economy (or Delta economy, the other reading's booking).",
    flag_twins=["ibis-quarry", "osprey-quill"],
    ambiguity={"phrase": "flight under 4 hours",
               "readings": ["the journey is the flight: over 4 hours, so premium economy needs no reason",
                            ("each flight is measured alone: all under 4 hours, so premium economy needs a reason "
                             "the traveller does not give: economy")]})

scenario(
    "thistle-pier", "flag", ["approval_required", "outside_air_section"],
    "Miami to Washington Dulles on January 25th, please, for the research symposium at Georgetown the next morning. "
    "I haven't sent the trip to my chair for approval yet, but please book it now while the fares are low.",
    trip(traveller_name="Dr. Samuel Adeyemi", traveller_title="Assistant Professor, Political Science",
         university_role="FACULTY", destination="IAD", travel_date="2027-01-25", booking_date="2026-12-28",
         business_starts="2027-01-26 09:00", purpose="Research symposium at Georgetown University",
         purpose_kind="CONFERENCE", sign_offs=[]),
    search("MIA", "IAD", "2027-01-25", {
        "united": {"carrier": "UA", "depart": "07:50"},
        "american": {"carrier": "AA", "depart": "10:15"},
        "united-later": {"carrier": "UA", "depart": "13:40"},
    }, [
        offer("united-economy", "united", "ECONOMY", 23600),
        offer("american-economy", "american", "ECONOMY", 21900),
        offer("united-later-economy", "united-later", "ECONOMY", 24800),
    ]),
    expected("FLAG_FOR_APPROVAL", ["american-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED"],
             ["DEAN", "FACULTY_AFFAIRS", "SUPERVISOR", "VICE_PRESIDENT"], sorted([*PREAMBLE, "DEFINITIONS"])),
    [AUTHORIZED, SUPERVISOR_FIRST, COVID, LLF],
    "Lines 34-37 and 47-48: the supervisor authorizes the trip, and approval from the appropriate supervisor is secured "
    "before University funds are committed; nothing is on file, and the chair has not been asked. Lines 17-19 (COVID-19 "
    "guidance) also ask for the supervising dean or vice president and, for faculty, Faculty Affairs; on any reading "
    "the supervisor's approval is awaited. Hold the lowest fare, American at $219.",
    flag_twins=["mangrove-lute", "heron-gable"],
    ambiguity="none: the supervisor's prior authorization (lines 34-37, 47-48) is missing on every reading, whether or "
    "not the COVID-19 approvals of lines 17-19 still apply")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    for data in S:
        (OUT / f"{data['id']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(S)} scenarios to {OUT}")


if __name__ == "__main__":
    main()
