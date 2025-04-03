def calculate_ev(prob_over, odds_over, odds_under):
    """
    Calculate expected value (EV) for both Over and Under outcomes.
    Returns a dict with the EV and best suggested pick.
    """

    prob_under = 1 - prob_over

    # Convert American odds to implied decimal
    def implied_prob(odds):
        return 100 / (odds + 100) if odds > 0 else abs(odds) / (abs(odds) + 100)

    payout = lambda odds: odds / 100 if odds > 0 else 100 / abs(odds)

    ev_over = (prob_over * payout(odds_over)) - (prob_under * 1)
    ev_under = (prob_under * payout(odds_under)) - (prob_over * 1)

    return {
        "ev_over": round(ev_over, 3),
        "ev_under": round(ev_under, 3),
        "best_pick": "Over" if ev_over > ev_under else "Under"
    }
