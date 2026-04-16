MENU_DATA = {
    "Przystawki": {
        "icon": "",
        "description": "Eleganckie przystawki na rozpoczęcie uczty weselnej",
        "dishes": [
            {"name": "Wiejski stół staropolski", "description": "Sery, wędliny, kiszonki, chleby wiejskie prosto z pieca", "allergens": ["gluten", "laktoza"], "price_per_person": 35},
            {"name": "Deska serów dojrzewających", "description": "Selekcja polskich serów z winogronami i orzechami włoskimi", "allergens": ["laktoza", "orzechy"], "price_per_person": 28},
            {"name": "Śledzie po polsku", "description": "Śledzie w trzech marynatach: z cebulką, w śmietanie i po kaszubsku", "allergens": ["ryby"], "price_per_person": 18},
            {"name": "Tatarski z polędwicy", "description": "Tradycyjny tatar z korniszonem, kaparami i żółtkiem", "allergens": ["jajka"], "price_per_person": 32},
        ],
    },
    "Zupy": {
        "icon": "",
        "description": "Tradycyjne polskie zupy w nowoczesnym wydaniu",
        "dishes": [
            {"name": "Żurek staropolski", "description": "Z białą kiełbasą, jajkiem i chrzanem, podawany w chlebie", "allergens": ["gluten", "jajka"], "price_per_person": 22},
            {"name": "Rosół z kury wiejskiej", "description": "Złocisty bulion gotowany 6 godzin, z makaronem lane ciasto", "allergens": ["gluten", "jajka"], "price_per_person": 18},
            {"name": "Barszcz czerwony z uszkami", "description": "Klasyczny barszcz z uszkami z grzybami leśnymi", "allergens": ["gluten"], "price_per_person": 20},
            {"name": "Krupnik z pęczaku", "description": "Sycąca zupa z pęczaku z warzywami i skwarkami", "allergens": ["gluten"], "price_per_person": 19},
        ],
    },
    "Dania Główne": {
        "icon": "",
        "description": "Serca naszego menu — starannie dobrane mięsa i ryby",
        "dishes": [
            {"name": "Kaczka pieczona z jabłkami", "description": "Kaczka faszerowana jabłkami i majerankiem, pieczona przez 4 godziny", "allergens": [], "price_per_person": 89},
            {"name": "Schab po staropolsku", "description": "Schab duszony z suszonymi śliwkami i miodem, z naturalnym sosem", "allergens": [], "price_per_person": 65},
            {"name": "Pstrąg z polskich hodowli", "description": "Pstrąg pieczony z masłem ziołowym, cytryną i koperkiem", "allergens": ["ryby", "laktoza"], "price_per_person": 72},
            {"name": "Kurczak wiejski duszony", "description": "Kurczak duszony z grzybami leśnymi w śmietanie, z natką", "allergens": ["laktoza"], "price_per_person": 55},
        ],
    },
    "Dodatki": {
        "icon": "",
        "description": "Staranne dodatki dopełniające smak dań głównych",
        "dishes": [
            {"name": "Kopytka z boczkiem", "description": "Domowe kopytka z chrupiącym boczkiem i cebulką", "allergens": ["gluten", "jajka"], "price_per_person": 15},
            {"name": "Pierogi ruskie", "description": "Z serem twarogowym, ziemniakami i cebulką, okraszone masłem", "allergens": ["gluten", "laktoza", "jajka"], "price_per_person": 18},
            {"name": "Kluski śląskie", "description": "Tradycyjne kluski z okrągłym otworem, podawane ze skwarkami", "allergens": ["gluten", "jajka"], "price_per_person": 14},
            {"name": "Ziemniaki zapiekane z rozmarynem", "description": "Młode ziemniaki z rozmarynem, czosnkiem i masłem", "allergens": ["laktoza"], "price_per_person": 10},
            {"name": "Warzywa grillowane sezonowe", "description": "Cukinia, papryka, bakłażan z oliwą i ziołami prowansalskimi", "allergens": [], "price_per_person": 12},
        ],
    },
    "Desery": {
        "icon": "",
        "description": "Słodkie zakończenie wyjątkowego wieczoru",
        "dishes": [
            {"name": "Tort weselny wielopiętrowy", "description": "Tort na zamówienie wg projektu Pary Młodej, z masą maślaną", "allergens": ["gluten", "laktoza", "jajka"], "price_per_person": 45},
            {"name": "Sernik babci Zosi", "description": "Pieczony sernik na kruchym spodzie z konfiturą z czarnej porzeczki", "allergens": ["laktoza", "jajka", "gluten"], "price_per_person": 22},
            {"name": "Lody rzemieślnicze", "description": "Trzy smaki do wyboru z domowymi waflami i bitą śmietaną", "allergens": ["laktoza", "gluten"], "price_per_person": 20},
            {"name": "Jabłecznik z lodami", "description": "Ciepły szarlotka z cynamonem, podawana z gałką lodów waniliowych", "allergens": ["gluten", "laktoza", "jajka"], "price_per_person": 18},
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
        "name": "Stacja Makaronów",
        "description": "Włoskie makarony gotowane na żywo z wyborem sosów i dodatków",
        "price": 1800,
    },
    {
        "icon": "",
        "name": "Candy Bar",
        "description": "Słodki stół z pralinkami, macarons, owocami i domowymi ciasteczkami",
        "price": 2200,
    },
    {
        "icon": "",
        "name": "Degustacja Serów",
        "description": "Selekcja 12 polskich i europejskich serów z sommelierem i konfiturami",
        "price": 1500,
    },
    {
        "icon": "",
        "name": "Nocna Grochówka",
        "description": "Tradycyjna grochówka z wędzonym boczkiem, serwowana o północy",
        "price": 900,
    },
    {
        "icon": "",
        "name": "Stacja Pierogów",
        "description": "Pierogi lepione i gotowane na żywo — kilka rodzajów nadzienia do wyboru",
        "price": 1600,
    },
]

DIET_OPTIONS = ["wegetariańskie", "wegańskie", "bezglutenowe", "bezlaktozowe", "halal", "kosher"]
