from models import CheatSheetResponse, Pick

def generate_cheatsheet(day: str) -> CheatSheetResponse:
    if day == "today":
        return CheatSheetResponse(
            Moneyline=[
                Pick(label="Phillies ML", confidence=9.25),
                Pick(label="Guardians ML", confidence=8.80),
            ],
            RunLine=[
                Pick(label="Padres +1.5", confidence=9.10),
                Pick(label="Twins +1.5", confidence=8.75),
            ],
            NRFI=[
                Pick(label="Marlins vs Braves", confidence=9.00),
                Pick(label="Astros vs Yankees", confidence=8.65),
            ],
            Hits=[
                Pick(label="Luis Arraez 1+ Hit", confidence=9.30),
                Pick(label="Juan Soto 1+ Hit", confidence=8.90),
            ],
            HR=[
                Pick(label="Aaron Judge HR", confidence=8.40),
                Pick(label="Kyle Schwarber HR", confidence=8.15),
            ]
        )
    else:  # "tomorrow"
        return CheatSheetResponse(
            Moneyline=[
                Pick(label="Mets ML", confidence=9.10),
                Pick(label="Cubs ML", confidence=8.60),
            ],
            RunLine=[
                Pick(label="Rays +1.5", confidence=9.00),
                Pick(label="Reds +1.5", confidence=8.55),
            ],
            NRFI=[
                Pick(label="Blue Jays vs Tigers", confidence=9.20),
                Pick(label="Dodgers vs Giants", confidence=8.90),
            ],
            Hits=[
                Pick(label="Trea Turner 1+ Hit", confidence=9.35),
                Pick(label="J.D. Martinez 1+ Hit", confidence=8.85),
            ],
            HR=[
                Pick(label="Pete Alonso HR", confidence=8.50),
                Pick(label="Yordan Alvarez HR", confidence=8.30),
            ]
        )

