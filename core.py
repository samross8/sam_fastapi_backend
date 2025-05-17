from models import CheatSheetResponse, Pick

def generate_cheatsheet(day: str):
    # Static mock data for now — this will be replaced with scraped + scored inputs
    picks = {
        "Moneyline": [
            Pick(label="Guardians ML", confidence=9.2),
            Pick(label="Padres ML", confidence=8.8),
            Pick(label="Rays ML", confidence=8.4),
        ],
        "RunLine": [
            Pick(label="Phillies +1.5", confidence=9.4),
            Pick(label="Twins +1.5", confidence=8.85),
            Pick(label="Cubs +1.5", confidence=8.5),
        ],
        "NRFI": [
            Pick(label="Tigers vs Blue Jays", confidence=9.1),
            Pick(label="Reds vs Marlins", confidence=8.6),
        ],
        "Hits": [
            Pick(label="Luis Arraez 1+ Hit", confidence=9.3),
            Pick(label="Juan Soto 1+ Hit", confidence=8.95),
        ],
        "HR": [
            Pick(label="Yordan Alvarez HR", confidence=8.6),
            Pick(label="Matt Olson HR", confidence=8.25),
        ]
    }

    # Construct parlay suite tiers
    sorted_all = sorted(
        [(cat, p) for cat in picks for p in picks[cat]],
        key=lambda x: x[1].confidence,
        reverse=True
    )

    def slice_confidence(start, end):
        return [p for _, p in sorted_all if start <= p.confidence < end]

    parlay_suite = {
        "best_bet": [sorted_all[0][1]],
        "doubloon_doubler_1": slice_confidence(9.0, 9.3),
        "doubloon_doubler_2": slice_confidence(8.7, 9.0),
        "mini_lotto": slice_confidence(8.4, 8.7),
        "lotto_play": slice_confidence(0, 8.4)
    }

    return {
        "cheatsheet": picks,
        "parlay_suite": parlay_suite
    }
