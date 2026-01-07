MODEL_SUMMARY = {
    ("shorten", "none"): {
        "gpt-4.1": {"rating": 4.757142857142857, "faithfulness_rating": 4.771428571428571, "completeness_rating": 4.828571428571428},
        "gpt-4o-mini": {"rating": 4.771428571428571, "faithfulness_rating": 4.771428571428571, "completeness_rating": 4.9},
    },
    ("lengthen", "none"): {
        "gpt-4.1": {"rating": 4.666666666666667, "faithfulness_rating": 4.666666666666667, "completeness_rating": 4.958333333333333},
        "gpt-4o-mini": {"rating": 4.583333333333333, "faithfulness_rating": 4.583333333333333, "completeness_rating": 4.916666666666667},
    },
    ("tone", "friendly"): {
        "gpt-4.1": {"rating": 4.816901408450704, "faithfulness_rating": 4.823943661971831, "completeness_rating": 4.915492957746479},
        "gpt-4o-mini": {"rating": 4.591549295774648, "faithfulness_rating": 4.591549295774648, "completeness_rating": 4.908450704225352},
    },
    ("tone", "sympathetic"): {
        "gpt-4.1": {"rating": 4.295774647887324, "faithfulness_rating": 4.302816901408451, "completeness_rating": 4.887323943661972},
        "gpt-4o-mini": {"rating": 4.436619718309859, "faithfulness_rating": 4.443661971830986, "completeness_rating": 4.908450704225352},
    },
    ("tone", "professional"): {
        "gpt-4.1": {"rating": 4.845070422535211, "faithfulness_rating": 4.845070422535211, "completeness_rating": 4.943661971830986},
        "gpt-4o-mini": {"rating": 4.725352112676056, "faithfulness_rating": 4.732394366197183, "completeness_rating": 4.838028169014085},
    },
}

def pick_action_tone_keys(action: str, tone):
    a = (action or "").strip().lower()
    if a == "tone":
        return "tone", (tone or "none").strip().lower()
    return a, "none"

def summarize_winners(metrics: dict, models=("gpt-4.1", "gpt-4o-mini")):
    m1, m2 = models
    def winner(metric):
        v1 = metrics[m1].get(metric, 0)
        v2 = metrics[m2].get(metric, 0)
        if v1 == v2:
            return "tie"
        return m1 if v1 > v2 else m2

    wins = {
        "rating": winner("rating"),
        "faithfulness_rating": winner("faithfulness_rating"),
        "completeness_rating": winner("completeness_rating"),
    }

    overall = wins["rating"]
    return wins, overall
