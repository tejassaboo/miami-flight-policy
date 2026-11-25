"""The answer key's rules for the University of Miami Travel Policy (PolicyStat ID 9607266, effective April
2021), as exact integer code. Byte-identical in src/plugin/rules.py and verifier/rules.py; it imports only
modules a verifier may use.

Every rule cites the frozen handbook text (src/plugin/data/policy.txt) by line. Where the text leaves an
answer open, the rule returns FLAG_FOR_APPROVAL with the unclear words, and a scenario may depend on each
unclear phrase at most once (tests/test_scenarios.py). Combinations no scenario needs raise ValueError, so a
new scenario cannot fall silently into untested logic.

The extraction prints the three justification bullets (lines 120-122) above the sentence that introduces them
("An appropriate business reason will be required when booking:", lines 126-127). Read in order: a fare $200
over the lowest logical airfare, premium economy "for flight under 4 hours" and business or first "for flight
under 8 hours" each need an appropriate business reason. A fare within $200 of the lowest logical airfare is
within policy (lines 123, 128-131).

The duration hook. "Under 4 hours" and "under 8 hours" are strict: a nonstop scheduled at exactly 240 (480)
minutes is not under, so its premium economy (business) seat needs no business reason. ``over`` answers
whether an offer is at or past the limit (no reason needed). For a connection, "flight" may mean one segment
or the journey: when every segment is at or past the limit every reading agrees (True); when the whole
elapsed journey is short of it every reading agrees (False); otherwise the reading is unclear (None). The
world's scheduled minutes are the only flight times known when the ticket is bought.

Approvers. Lines 17-19 require prior approval of all University travel by the supervisor and the supervising
dean or vice president, and for faculty also by Faculty Affairs; lines 34-37 and 47-48 require the
supervisor's authorization before arrangements are made. Every trip record holds the sign-offs it has. Under
the template's rule 4' (SYNC_NOTES.md), a booking accepts each of those roles and NONE; a refusal does not use
them, so it accepts NONE and those roles (rule 4(b)); a hold accepts only the awaited role (or the roles the
text points to for an unclear clause), never NONE.
"""

from contract import (
    Approver,
    Cabin,
    Clause,
    Decision,
    Passenger,
    Purpose,
    ReasonCode,
    Routing,
    SignOffSubject,
    UniversityRole,
)

from .world import clock_minutes, date_of, day_number

HANDBOOK = "University of Miami Travel Policy, PolicyStat ID 9607266, effective April 2021"

# Each closed-list section and the heading it names in the frozen text (tests check every heading is there).
# The extraction prints the left-column headings where each page's text starts (PURPOSE/SCOPE/POLICY stacked
# at lines 13-15, DEFINITIONS at 42 above policy statements, PROCEDURE and AIR TRAVEL at 82-83 above more
# definitions), so the accept sets below take every heading a reader could file a sentence under.
CLAUSE_HEADINGS = {
    Clause.PURPOSE: "PURPOSE:",
    Clause.SCOPE: "SCOPE:",
    Clause.POLICY: "POLICY:",
    Clause.DEFINITIONS: "DEFINITIONS:",
    Clause.PROCEDURE: "PROCEDURE:",
    Clause.AIR_TRAVEL: "AIR TRAVEL",
    Clause.LODGING: "LODGING",
    Clause.CAR_RENTAL: "CAR RENTAL",
    Clause.INTERNATIONAL_TRAVEL: "INTERNATIONAL TRAVEL",
    Clause.BOOKING_FOR_OTHERS: "BOOKING FOR OTHERS",
    Clause.APPROVAL_SIGNATURES: "Approval Signatures",
    Clause.APPLICABILITY: "Applicability",
}

# The handbook's duration thresholds (the per-handbook duration hook; tests/test_duration.py tests both
# sides of each). ">=" is inclusive: a flight of exactly the limit is not "under" it.
DURATION_RULES = (
    {"name": "premium-economy", "minutes": 240, "operator": ">=", "lines": [121, 121],
     "quote": "Premium Economy/Comfort Plus ticket for flight under 4 hours"},
    {"name": "business", "minutes": 480, "operator": ">=", "lines": [122, 122],
     "quote": "First Class/Business Class ticket for flight under 8 hours"},
)
LIMITS = {rule["name"]: rule["minutes"] for rule in DURATION_RULES}

# Handbook-specific conventions shown by booking_requirements, beyond the template's (none here).
CONVENTIONS = ()

# Lines 120, 123, 128-131: within $200 of the lowest logical airfare is within policy; more needs a reason.
TOLERANCE_CENTS = 20_000
# Lines 149-150: a connection "should be considered if fare savings exceeds $200 and does not increase travel
# time by more than two hours" (strict on the savings, inclusive on the time).
SAVINGS_CENTS = 20_000
ADDED_MINUTES = 120
# Lines 115-116: "the lowest available fare within two hours of the desired departure or arrival time".
WINDOW_MINUTES = 120
# Lines 58-59: flights charged to federal awards on U.S. flag air carriers (as search_flights names them).
US_CARRIERS = ("American Airlines", "Delta Air Lines", "United Airlines", "Alaska Airlines", "JetBlue",
               "Southwest Airlines")
# Lines 74-76: domestic travel is within the United States, its possessions and territories, including Guam,
# American Samoa, Puerto Rico and the Virgin Islands (ISO codes of the world's airports).
DOMESTIC_COUNTRIES = ("US", "PR", "GU")
TERRITORIES = ("PR", "GU")

HIDDEN_KEYS = {"reason_kind", "federal_award"}
REASON_KINDS = ("none", "personal", "unclear", "economy_sold_out")

LOWEST_CLAUSES = [Clause.AIR_TRAVEL, Clause.PROCEDURE, Clause.POLICY, Clause.DEFINITIONS]
CABIN_CLAUSES = [Clause.AIR_TRAVEL, Clause.PROCEDURE]
PREAMBLE_CLAUSES = [Clause.PURPOSE, Clause.SCOPE, Clause.POLICY]
UNCLEAR_REASONS = [ReasonCode.UNCLEAR_POLICY_TEXT, ReasonCode.APPROVAL_REQUIRED]
# An unclear clause: no interpreter is named; the Travel Management Department is responsible for the guidelines
# (lines 102-104) and exceptions go to an Executive Vice President (lines 62-63).
UNCLEAR_ROLES = [Approver.NOT_NAMED, Approver.TRAVEL_MANAGEMENT, Approver.EXECUTIVE_VICE_PRESIDENT]
DURATION_PHRASE = "flight under 4 hours"
REASON_PHRASE = "appropriate business reason"
DECLINED = [ReasonCode.UPGRADE_NOT_ELIGIBLE, ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET,
            ReasonCode.BUSINESS_REASON_MISSING]


def over(rule, offer):
    """True, False or None (unclear): whether ``offer``'s flights out are at or past the handbook's ``rule``
    limit, so that the better cabin needs no business reason."""
    if rule not in LIMITS:
        raise ValueError(f"unknown duration rule {rule!r}")
    if offer.return_segments:
        raise ValueError("a round trip is not modelled by this handbook's scenarios")
    limit = LIMITS[rule]
    if min(segment.scheduled_minutes for segment in offer.segments) >= limit:
        return True
    return False if offer.elapsed_minutes < limit else None


def by_value(items):
    return sorted(set(items), key=lambda item: item.value)


def answer(decision, offers, reasons, approvers, clauses, why, phrase=""):
    return {
        "decision": decision,
        "offer_ids": sorted(offer.offer_id for offer in offers),
        "cabins": by_value(offer.cabin for offer in offers) or [Cabin.NONE],
        "reason_codes": by_value(reasons),
        "approvers": by_value(approvers),
        "clauses": by_value(clauses),
        "unclear_phrase": phrase,
        "explanation": why,
    }


def cheapest(offers):
    if not offers:
        return []
    low = min(offer.fare_cents for offer in offers)
    return [offer for offer in offers if offer.fare_cents == low]


def ids(offers):
    return {offer.offer_id for offer in offers}


def one(offers, what):
    if len(offers) != 1:
        raise ValueError(f"{what}: {len(offers)} offers tie or none is listed; not modelled")
    return offers[0]


def on_route(trip, offers, date):
    return [offer for offer in offers if offer.segments[0].origin == trip.origin.code
            and offer.segments[-1].destination == trip.destination.code and offer.segments[0].depart_local[:10] == date]


def in_time(trip, offer):
    """Whether the offer lands at or before the work begins (both local at the destination)."""
    return offer.segments[-1].arrive_local <= trip.business_starts


def in_window(trip, offer):
    """Lines 115-116: within two hours of the desired departure time (inclusive)."""
    leaves = clock_minutes(offer.segments[0].depart_local[11:])
    return abs(leaves - clock_minutes(trip.desired_departure)) <= WINDOW_MINUTES


def economy_choice(trip, economy):
    """The economy offers the handbook accepts, their reasons, sections and a note: the lowest logical fare
    (lines 115-118, 49), with the connecting-flights test of lines 149-150 and the $200 tolerance of lines
    120, 123 and 128."""
    low = cheapest(economy)
    if not low:
        raise ValueError("no economy offer can be bought")
    if any(offer.stops > 1 for offer in low):
        raise ValueError("a cheapest fare with two or more connections is not modelled")
    nonstops = cheapest([offer for offer in economy if offer.stops == 0])
    if all(offer.stops == 0 for offer in low) or not nonstops:
        if trip.requested_routing == Routing.NONSTOP and any(offer.stops for offer in low):
            raise ValueError("a nonstop request with no nonstop listed is not modelled")
        return low, [ReasonCode.LOWEST_FARE], [], "lines 115-118: the lowest logical fare"
    connection, nonstop = one(low, "cheapest connection"), one(nonstops, "cheapest nonstop")
    savings = nonstop.fare_cents - connection.fare_cents
    added = connection.elapsed_minutes - nonstop.elapsed_minutes
    if connection.segments[0].depart_local != nonstop.segments[0].depart_local:
        raise ValueError("a connection and a nonstop leaving at different times are not modelled")
    if savings == TOLERANCE_CENTS:
        raise ValueError("a nonstop exactly $200 above the connection is not modelled")
    if savings > SAVINGS_CENTS and added <= ADDED_MINUTES:
        # The nonstop is more than $200 over the lowest logical airfare and the connection passes the
        # handbook's own test: the connection. LOWEST_FARE stays beside the specific codes (lead's decision).
        reasons = [ReasonCode.COST_SAVINGS, ReasonCode.ALTERNATE_ROUTE_TOO_EXPENSIVE, ReasonCode.LOWEST_FARE,
                   ReasonCode.ALTERNATE_ROUTE_WITHIN_MARGIN]
        return ([connection], reasons, [],
                (f"lines 149-150: the connection saves {savings} cents (more than $200) and adds {added} minutes (not "
                 "more than two hours), so it is the lowest logical fare; the nonstop is more than $200 over it "
                 "and needs a business reason (lines 120, 126-129), which a wish for a nonstop is not"))
    if trip.requested_routing != Routing.NONSTOP:
        raise ValueError("a cheaper connection outside the test, for a traveller who did not ask for a nonstop, "
                         "is not modelled")
    if savings < TOLERANCE_CENTS:
        reasons = [ReasonCode.FARE_WITHIN_TOLERANCE, ReasonCode.ALTERNATE_ROUTE_WITHIN_MARGIN, ReasonCode.LOWEST_FARE]
        return ([nonstop], reasons, [],
                (f"lines 149-150: the connection saves only {savings} cents (not more than $200), so it need not be "
                 "considered; the requested nonstop is within $200 of the lowest fare, within policy (lines 123, "
                 "128-131)"))
    reasons = [ReasonCode.CONNECTION_TOO_LONG, ReasonCode.LOWEST_FARE, ReasonCode.COST_SAVINGS,
               ReasonCode.ALTERNATE_ROUTE_TOO_EXPENSIVE, ReasonCode.ALTERNATE_ROUTE_WITHIN_MARGIN]
    return ([connection, nonstop], reasons, [],
            (f"lines 149-150: the connection saves {savings} cents but adds {added} minutes (more than two hours), "
             "outside the test, so the requested nonstop may be the logical fare; since the nonstop is also more "
             "than $200 over the cheaper connection (lines 120, 128), both are accepted"))


def solve(trip, offers, hidden):
    """The answer key for one trip and the offers on its searches: the decision, and every accepted offer id,
    cabin, reason, approver and section. ``hidden`` (the scenario's answer_key_inputs) may give how the
    traveller's stated reason reads (``reason_kind``) and whether the funding is a federal award."""
    if set(hidden) - HIDDEN_KEYS or hidden.get("reason_kind", "none") not in REASON_KINDS:
        raise ValueError(f"unknown answer_key_inputs {hidden!r}")
    if trip.return_date:
        raise ValueError("a round-trip ticket is not modelled")
    if any(record.subject != SignOffSubject.TRIP for record in trip.sign_offs):
        raise ValueError("an exception on file is not modelled")
    roles = [record.role for record in trip.sign_offs]
    unused = [Approver.NONE, *roles]
    if trip.passenger == Passenger.COMPANION:
        position = trip.university_role != UniversityRole.NO_UNIVERSITY_ROLE
        if position != bool(trip.companion_contribution):
            raise ValueError("a companion with a position but no contribution, or the reverse, is not modelled")
        if not position:
            return answer(Decision.REFUSE, [], [ReasonCode.COMPANION_NOT_COVERED,
                                                ReasonCode.PERSONAL_TRAVEL_NOT_COVERED],
                          unused, [Clause.BOOKING_FOR_OTHERS, Clause.DEFINITIONS],
                          "Lines 269-272: the expenses of a spouse, family member or other person accompanying the "
                          "business traveller are not payable using University Funds unless that person has a "
                          "position with the University and travels to make a significant contribution; this "
                          "companion has none. The University buys no ticket.")
    elif trip.university_role == UniversityRole.NO_UNIVERSITY_ROLE or trip.companion_contribution or trip.accompanies:
        raise ValueError("a traveller outside the University, or a companion field on a traveller, is not modelled")
    if trip.purpose_kind == Purpose.PERSONAL:
        if trip.passenger != Passenger.TRAVELLER:
            raise ValueError("a personal trip by a companion is not modelled")
        return answer(Decision.REFUSE, [], [ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE],
                      unused, [*PREAMBLE_CLAUSES, Clause.DEFINITIONS],
                      "Lines 26-31 and 43-46: the policy covers travel on University business; lines 68-70: an "
                      "allowable expense is incurred for the primary benefit of university business; lines "
                      "106-107: University Funds. A personal trip is not University business, so the University "
                      "buys no ticket.")
    missing = []
    if Approver.SUPERVISOR not in roles:
        missing.append(Approver.SUPERVISOR)
    if Approver.DEAN not in roles and Approver.VICE_PRESIDENT not in roles:
        missing.append(Approver.DEAN)
    if trip.university_role == UniversityRole.FACULTY and Approver.FACULTY_AFFAIRS not in roles:
        missing.append(Approver.FACULTY_AFFAIRS)
    if missing not in ([], [Approver.FACULTY_AFFAIRS]):
        raise ValueError(f"missing trip approvals {missing} are not modelled")
    countries = {trip.origin.country, trip.destination.country}
    abroad = not countries <= set(DOMESTIC_COUNTRIES)
    if abroad != trip.abroad_approvals_on_file:
        raise ValueError("a trip abroad without its approvals, or approvals for a domestic trip, is not modelled")
    result = book(trip, offers, hidden, [Approver.NONE, *roles], abroad)
    if trip.passenger == Passenger.COMPANION:
        if result["decision"] != Decision.BOOK:
            raise ValueError("a companion hold is not modelled")
        result["reason_codes"] = by_value([*result["reason_codes"], ReasonCode.COMPANION_UNIVERSITY_ROLE])
        result["clauses"] = by_value([*result["clauses"], Clause.BOOKING_FOR_OTHERS])
        result["explanation"] += (" Lines 269-272: the companion holds a position with the University and travels to "
                                  "make a significant contribution, so the ticket is payable.")
    if abroad:
        # Lines 233-235: international travel is booked after its approvals; the section is a fair citation.
        result["clauses"] = by_value([*result["clauses"], Clause.INTERNATIONAL_TRAVEL])
    if countries & set(TERRITORIES):
        result["clauses"] = by_value([*result["clauses"], Clause.DEFINITIONS, Clause.INTERNATIONAL_TRAVEL])
        result["explanation"] += (" Lines 74-76: travel to a U.S. territory such as Puerto Rico is domestic, so the "
                                  "approvals for international travel (lines 233-235) are not needed.")
    if missing:
        if result["decision"] != Decision.BOOK or result["reason_codes"] != [ReasonCode.LOWEST_FARE]:
            raise ValueError("a missing Faculty Affairs approval on anything but a plain lowest-fare booking is not "
                             "modelled")
        result.update(decision=Decision.FLAG_FOR_APPROVAL, reason_codes=[ReasonCode.APPROVAL_REQUIRED],
                      approvers=[Approver.FACULTY_AFFAIRS], clauses=by_value(PREAMBLE_CLAUSES))
        result["explanation"] = ("Lines 17-19: all University-related travel must receive prior approval by the "
                                 "supervisor and the supervising dean or vice president, and for faculty also from "
                                 "Faculty Affairs. The supervisor and dean have approved; Faculty Affairs has not. "
                                 "Hold the fare the policy would buy: " + result["explanation"])
    return result


def book(trip, offers, hidden, approvers, abroad):
    """The booking for a University traveller whose trip approvals are on file."""
    kind = hidden.get("reason_kind", "none")
    route = on_route(trip, offers, trip.travel_date)
    timely = [offer for offer in route if in_time(trip, offer)]
    if len(timely) != len(route) and kind != "economy_sold_out":
        raise ValueError("flights landing after the work begins are modelled only for the sold-out case")
    candidates = timely
    if trip.desired_departure:
        candidates = [offer for offer in candidates if in_window(trip, offer)]
    federal = hidden.get("federal_award", False)
    if federal:
        candidates = [offer for offer in candidates if offer.carrier in US_CARRIERS]
    seated = [offer for offer in candidates if offer.seats_available]
    economy = [offer for offer in seated if offer.cabin == Cabin.ECONOMY]
    if trip.personal_days:
        return personal(trip, offers, economy, approvers)
    if trip.requested_cabin == Cabin.PREMIUM_ECONOMY:
        return premium(trip, route, seated, economy, approvers, kind)
    if trip.requested_cabin == Cabin.BUSINESS:
        return business(trip, route, candidates, seated, economy, approvers, kind, abroad)
    if trip.requested_cabin != Cabin.ECONOMY or kind != "none":
        raise ValueError("this economy request is not modelled")
    if federal:
        return fly_america(trip, timely, economy, approvers)
    return economy_request(trip, timely, economy, approvers)


def economy_request(trip, timely, economy, approvers):
    chosen, reasons, clauses, note = economy_choice(trip, economy)
    notes = [note]
    if trip.desired_departure:
        everywhere = cheapest([offer for offer in timely if offer.seats_available and offer.cabin == Cabin.ECONOMY])
        if reasons != [ReasonCode.LOWEST_FARE] or ids(everywhere) & ids(chosen):
            raise ValueError("a time window that changes nothing, or a window with connections, is not modelled")
        reasons = [*reasons, ReasonCode.REQUESTED_TIME_WINDOW]
        notes.append("lines 115-116: the lowest available fare within two hours of the desired departure time; "
                     "cheaper flights leave further from it")
    if trip.requested_airline:
        if reasons != [ReasonCode.LOWEST_FARE]:
            raise ValueError("an airline wish beside other tests is not modelled")
        wished = cheapest([offer for offer in economy if offer.carrier == trip.requested_airline])
        if not wished or ids(wished) & ids(chosen):
            raise ValueError("an airline wish that the lowest fare already meets is not modelled")
        extra = wished[0].fare_cents - chosen[0].fare_cents
        if extra <= TOLERANCE_CENTS:
            raise ValueError("an airline wish within $200 is not modelled")
        # Declined on the $200 tolerance of the lowest airfare (lines 120, 123, 128), a lowest-fare rule itself.
        reasons = [ReasonCode.LOWEST_FARE, ReasonCode.LOYALTY_PROGRAM_PREFERENCE, ReasonCode.BUSINESS_REASON_MISSING]
        notes.append(f"lines 120, 123, 126-129: the {trip.requested_airline} fare is {extra} cents over the lowest "
                     "logical airfare, more than $200, which needs an appropriate business reason; earning the "
                     "traveller's own airline points (lines 145-146) is not one")
    return answer(Decision.BOOK, chosen, reasons, approvers, [*LOWEST_CLAUSES, *clauses], "; ".join(notes) + ".")


def fly_america(trip, timely, economy, approvers):
    """Lines 58-59: flights charged to federal awards are booked with U.S. flag air carriers."""
    chosen, reasons = economy_choice(trip, economy)[:2]
    everywhere = cheapest([offer for offer in timely if offer.seats_available and offer.cabin == Cabin.ECONOMY])
    if reasons != [ReasonCode.LOWEST_FARE] or ids(everywhere) & ids(chosen):
        raise ValueError("a federal award whose cheapest fare is already on a U.S. carrier is not modelled")
    return answer(Decision.BOOK, chosen, [ReasonCode.FLY_AMERICA_US_CARRIER_REQUIRED, ReasonCode.OPEN_SKIES_AGREEMENT,
                                              ReasonCode.NATIONAL_CARRIER_REQUIRED], approvers, [Clause.POLICY, Clause.DEFINITIONS],
                  "Lines 58-59: the Fly America Act/Open Skies Agreement requires all flights charged to federal "
                  "awards to be booked with U.S. flag air carriers; the trip is charged to a federal research "
                  "award, so the lowest economy fare on a U.S. carrier, not the cheaper foreign carrier.")


def declined(trip, economy, approvers, kind, why):
    """A better cabin that needs a business reason the traveller does not give: the lowest logical fare."""
    if kind not in ("none", "personal"):
        raise ValueError(f"a declined cabin with a {kind} reason is not modelled")
    chosen, reasons, clauses, note = economy_choice(trip, economy)
    if reasons != [ReasonCode.LOWEST_FARE]:
        raise ValueError("a declined cabin whose economy fare turns on the connection test is not modelled")
    # The reason names why the cabin is declined, so LOWEST_FARE (the economy fare's own reason) is not accepted.
    return answer(Decision.BOOK, chosen, DECLINED, approvers, [*CABIN_CLAUSES, *LOWEST_CLAUSES, *clauses],
                  f"{why}; {note}.")


def premium(trip, route, seated, economy, approvers, kind):
    """Lines 121, 126-127: premium economy for a flight under 4 hours needs an appropriate business reason."""
    verdicts = {over("premium-economy", offer) for offer in route}
    if len(verdicts) != 1:
        raise ValueError("offers on different sides of the 4-hour limit are not modelled (set background 0)")
    verdict = verdicts.pop()
    upgrade = cheapest([offer for offer in seated if offer.cabin == Cabin.PREMIUM_ECONOMY])
    low = cheapest(economy)
    if not upgrade or not low or upgrade[0].fare_cents - low[0].fare_cents > TOLERANCE_CENTS:
        raise ValueError("a premium economy request without a premium seat within $200 is not modelled")
    if verdict is True:
        return answer(Decision.BOOK, upgrade, [ReasonCode.PREMIUM_ECONOMY_ALLOWED, ReasonCode.UPGRADE_WITHIN_FARE_MARGIN,
                                              ReasonCode.FARE_WITHIN_TOLERANCE], approvers, CABIN_CLAUSES,
                      "Lines 121, 126-127: premium economy needs a business reason only for a flight under 4 hours; "
                      "this flight is not under 4 hours, and the cheapest premium economy fare is within $200 of the "
                      "lowest economy fare (lines 123, 128), so it is within policy and the traveller asks for it.")
    if verdict is False:
        return declined(trip, economy, approvers, kind,
                        "Lines 121, 126-127: premium economy for a flight under 4 hours needs an appropriate business "
                        "reason, and the traveller gives none")
    chosen, reasons = economy_choice(trip, economy)[:2]
    if reasons != [ReasonCode.LOWEST_FARE] or kind not in ("none", "personal"):
        raise ValueError("an unclear premium economy case beside other tests is not modelled")
    return answer(Decision.FLAG_FOR_APPROVAL, [*upgrade, *chosen], UNCLEAR_REASONS, UNCLEAR_ROLES, CABIN_CLAUSES,
                  "Line 121: premium economy for a 'flight under 4 hours' needs a business reason. Each flight of this "
                  "connection is under 4 hours, but the journey is not; the handbook does not say whether a "
                  "connection is one flight or several. On one reading premium economy is within policy, on the "
                  "other it needs a reason the traveller does not give. Hold the cheapest premium economy fare (or "
                  "the cheapest economy fare).", phrase=DURATION_PHRASE)


def business(trip, route, candidates, seated, economy, approvers, kind, abroad):
    """Lines 122, 126-127: business class for a flight under 8 hours needs an appropriate business reason."""
    verdicts = {over("business", offer) for offer in route}
    if len(verdicts) != 1 or None in verdicts:
        raise ValueError("offers on different sides of the 8-hour limit, or connections, are not modelled")
    verdict = verdicts.pop()
    upgrade = cheapest([offer for offer in seated if offer.cabin == Cabin.BUSINESS])
    if not upgrade:
        raise ValueError("a business request with no business seat is not modelled")
    if verdict is True:
        low = cheapest(economy)
        if kind != "none" or not low or upgrade[0].fare_cents - low[0].fare_cents > TOLERANCE_CENTS:
            raise ValueError("a long-flight business request outside $200 of economy is not modelled")
        reasons = [ReasonCode.LONG_FLIGHT_APPROVED, ReasonCode.UPGRADE_WITHIN_FARE_MARGIN,
                   ReasonCode.FARE_WITHIN_TOLERANCE]
        if abroad:
            reasons.append(ReasonCode.INTERNATIONAL_LONG_FLIGHT)
        return answer(Decision.BOOK, upgrade, reasons, approvers, CABIN_CLAUSES,
                      "Lines 122, 126-127: business class needs a business reason only for a flight under 8 hours; "
                      "this flight is not under 8 hours, and the cheapest business fare is within $200 of the lowest "
                      "economy fare (lines 123, 128), so it is within policy and the traveller asks for it.")
    if kind == "economy_sold_out":
        coach = [offer for offer in candidates if offer.cabin == Cabin.ECONOMY]
        if not coach or any(offer.seats_available for offer in coach) or trip.desired_departure:
            raise ValueError("a sold-out case needs every economy seat landing in time sold out")
        return answer(Decision.BOOK, upgrade, [ReasonCode.NO_ECONOMY_SEATS_URGENT, ReasonCode.BUSINESS_REASON_DOCUMENTED,
                                              ReasonCode.LOWEST_FARE], approvers, CABIN_CLAUSES,
                      "Lines 122, 126-127: business class for a flight under 8 hours needs an appropriate business "
                      "reason. Every economy seat on the flights that land before the work begins is sold out, which "
                      "is such a reason; the lowest available fare that lands in time (lines 115-118) is this "
                      "business fare.")
    if kind == "unclear":
        chosen, reasons = economy_choice(trip, economy)[:2]
        if reasons != [ReasonCode.LOWEST_FARE]:
            raise ValueError("an unclear business reason beside the connection test is not modelled")
        return answer(Decision.FLAG_FOR_APPROVAL, [*upgrade, *chosen], UNCLEAR_REASONS,
                      [*UNCLEAR_ROLES, Approver.SUPERVISOR], CABIN_CLAUSES,
                      "Lines 122, 126-127: business class for a flight under 8 hours needs 'an appropriate business "
                      "reason', which the handbook does not define. The traveller's reason is University work done "
                      "on board; one reader takes that as a business reason, another as a comfort wish. Hold the "
                      "cheapest business fare (or the cheapest economy fare).", phrase=REASON_PHRASE)
    return declined(trip, economy, approvers, kind,
                    "Lines 122, 126-127: business class for a flight under 8 hours needs an appropriate business reason, "
                    "and comfort is not one")


def personal(trip, offers, economy, approvers):
    """Lines 135-144: a trip extended for personal travel needs a comparison non-refundable coach quote on the
    business dates, and reimbursement is limited to the lesser airfare. Business trips normally commence one day
    before the conference or meeting."""
    if trip.requested_cabin != Cabin.ECONOMY or trip.requested_airline or trip.desired_departure:
        raise ValueError("a personal extension outside plain economy is not modelled")
    business_day = date_of(day_number(trip.business_starts[:10]) - 1)
    if business_day == trip.travel_date:
        raise ValueError("personal days on a trip leaving on its business day are not modelled")
    wanted = cheapest(economy)
    if not wanted or any(offer.stops for offer in wanted):
        raise ValueError("a personal-date fare that is not a nonstop is not modelled")
    quote = cheapest([offer for offer in on_route(trip, offers, business_day)
                      if offer.seats_available and offer.cabin == Cabin.ECONOMY and not offer.refundable])
    if not quote:
        raise ValueError("the comparison fare must be on a pinned search on the business day")
    lesser = min(wanted[0].fare_cents, quote[0].fare_cents)
    return answer(Decision.BOOK, wanted, [ReasonCode.PERSONAL_EXTENSION_COMPARISON, ReasonCode.LOWEST_FARE,
                                              ReasonCode.PERSONAL_TRAVEL_NOT_COVERED], approvers, CABIN_CLAUSES,
                  f"Lines 135-144: business trips normally commence one day before the conference ({business_day}); "
                  "the traveller extends the trip for personal days, so the flight they will take is booked at its "
                  f"lowest fare ({wanted[0].fare_cents} cents) with a comparison non-refundable coach quote for "
                  f"{business_day} ({quote[0].fare_cents} cents), and reimbursement is limited to the lesser "
                  f"({lesser} cents).")
