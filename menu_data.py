MENU_DATA = {
    "Przystawki": {
        "icon": "",
        "description": "Eleganckie przystawki na rozpoczęcie uczty weselnej",
        "dishes": [
            {"name": "Wiejski stół staropolski", "description": "Sery, wędliny, kiszonki, chleby wiejskie", "allergens": ["gluten", "laktoza"], "price_per_person": 35},
            {"name": "Deska serów dojrzewających", "description": "Selekcja serów z winogronami i orzechami", "allergens": ["laktoza", "orzechy"], "price_per_person": 28},
            {"name": "Śledzie po polsku", "description": "Śledzie w trzech marynatach", "allergens": ["ryby"], "price_per_person": 18},
            {"name": "Carpaccio z polędwicy", "description": "Cienko krojona polędwica z rukolą i parmezanem", "allergens": ["laktoza"], "price_per_person": 32},
        ],
    },
    "Zupy": {
        "icon": "",
        "description": "Tradycyjne polskie zupy w nowoczesnym wydaniu",
        "dishes": [
            {"name": "Żurek staropolski", "description": "Z białą kiełbasą, jajkiem i chrzanem", "allergens": ["gluten", "jajka"], "price_per_person": 22},
            {"name": "Rosół z kury wiejskiej", "description": "Złocisty bulion z makaronem lane ciasto", "allergens": ["gluten", "jajka"], "price_per_person": 18},
            {"name": "Barszcz czerwony z uszkami", "description": "Klasyczny barszcz z uszkami z grzybami", "allergens": ["gluten"], "price_per_person": 20},
            {"name": "Krem z dyni z pestkami", "description": "Aksamitna zupa krem z pestkami dyni", "allergens": [], "price_per_person": 19},
        ],
    },
    "Dania Główne": {
        "icon": "",
        "description": "Serca naszego menu — starannie dobrane mięsa i ryby",
        "dishes": [
            {"name": "Kaczka w sosie pomarańczowym", "description": "Pieczona kaczka z pomarańczą i rozmarynem", "allergens": [], "price_per_person": 89},
            {"name": "Polędwica wołowa sous-vide", "description": "Polędwica z sosem truflowym i jus", "allergens": [], "price_per_person": 125},
            {"name": "Łosoś atlantycki pieczony", "description": "Filet z łososia z cytryną i koperkiem", "allergens": ["ryby"], "price_per_person": 75},
            {"name": "Kurczak w sosie śmietanowym", "description": "Pierś z kurczaka z grzybami leśnymi", "allergens": ["laktoza"], "price_per_person": 55},
        ],
    },
    "Dodatki": {
        "icon": "",
        "description": "Staranne dodatki dopełniające smak dań głównych",
        "dishes": [
            {"name": "Kopytka z boczkiem", "description": "Domowe kopytka z chrupiącym boczkiem", "allergens": ["gluten", "jajka"], "price_per_person": 15},
            {"name": "Pierogi ruskie", "description": "Z serem, ziemniakami i cebulką", "allergens": ["gluten", "laktoza", "jajka"], "price_per_person": 18},
            {"name": "Kluski śląskie", "description": "Tradycyjne kluski z okrągłym otworem", "allergens": ["gluten", "jajka"], "price_per_person": 14},
            {"name": "Ziemniaki zapiekane", "description": "Z rozmarynem i czosnkiem", "allergens": [], "price_per_person": 10},
            {"name": "Warzywa grillowane sezonowe", "description": "Cukinia, papryka, bakłażan z oliwą", "allergens": [], "price_per_person": 12},
        ],
    },
    "Desery": {
        "icon": "",
        "description": "Słodkie zakończenie wyjątkowego wieczoru",
        "dishes": [
            {"name": "Tort weselny wielopiętrowy", "description": "Tort na zamówienie wg projektu Pary Młodej", "allergens": ["gluten", "laktoza", "jajka"], "price_per_person": 45},
            {"name": "Fontanna czekoladowa", "description": "Z owocami i kąskami do maczania", "allergens": ["laktoza"], "price_per_person": 30},
            {"name": "Lody rzemieślnicze", "description": "Trzy smaki do wyboru z waflami", "allergens": ["laktoza", "gluten"], "price_per_person": 20},
            {"name": "Sernik na zimno", "description": "Klasyczny sernik z owocami leśnymi", "allergens": ["laktoza", "jajka", "gluten"], "price_per_person": 22},
        ],
    },
}

UPSELLS = [
    {
        "icon": "",
        "name": "Stacja Sushi",
        "description": "Żywe sushi na specjalnej wyspie — kucharz przygotowuje na oczach gości",
        "price": 3500,
    },
    {
        "icon": "",
        "name": "Bar Ostryg",
        "description": "Świeże ostrygi z cytryną i winegret — idealne z szampanem",
        "price": 2800,
    },
    {
        "icon": "",
        "name": "Stacja Makaronów",
        "description": "Włoskie makarony gotowane na żywo z wyborem sosów",
        "price": 1800,
    },
    {
        "icon": "",
        "name": "Candy Bar",
        "description": "Słodki stół z pralinkami, macarons, owocami w czekoladzie",
        "price": 2200,
    },
    {
        "icon": "",
        "name": "Degustacja Serów",
        "description": "Selekcja 12 serów europejskich z sommelierem",
        "price": 1500,
    },
    {
        "icon": "",
        "name": "Nocna Grochówka",
        "description": "Tradycyjna grochówka serwowana o północy",
        "price": 900,
    },
]

DIET_OPTIONS = ["wegetariańskie", "wegańskie", "bezglutenowe", "bezlaktozowe", "halal", "kosher"]
