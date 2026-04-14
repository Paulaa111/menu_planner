"""
menu_data.py – Dane menu weselnego.
Edytuj ten plik, aby dostosować ofertę do konkretnej restauracji.
"""

MENU_DATA = {
    "Przystawki & Wiejski Stół": {
        "icon": "🧀",
        "description": "Pierwsze wrażenie na przyjęciu – eleganckie i apetyczne",
        "dishes": [
            {
                "name": "Deska serów z konfiturami",
                "description": "Selekcja polskich i europejskich serów z owocowymi konfiturami i orzechami",
                "allergens": ["mleko", "orzechy"],
            },
            {
                "name": "Śledzie w 3 marynatach",
                "description": "Klasyczne śledzie w oleju, po kaszubsku i w sosie śmietanowym z jabłkiem",
                "allergens": ["ryby", "mleko"],
            },
            {
                "name": "Roladki z łososia z twarożkiem",
                "description": "Wędzone plastry łososia z kremowym twarożkiem ziołowym",
                "allergens": ["ryby", "mleko"],
            },
            {
                "name": "Bruschetta z pomidorami i bazylią",
                "description": "Chrupiące grzanki z dojrzałymi pomidorami, czosnkiem i świeżą bazylią",
                "allergens": ["gluten"],
            },
            {
                "name": "Tartinki z pasztetem domowym",
                "description": "Mini kanapeczki z pasztetem z dziczyzny i żurawiną",
                "allergens": ["gluten", "seler"],
            },
        ],
    },
    "Zupy": {
        "icon": "🍲",
        "description": "Rozgrzewające i aromatyczne – serce polskiego przyjęcia weselnego",
        "dishes": [
            {
                "name": "Żurek staropolski z jajkiem i kiełbasą",
                "description": "Tradycyjny żurek na zakwasie z ugotowanym jajkiem, białą kiełbasą i chrzanem",
                "allergens": ["gluten", "jaja"],
            },
            {
                "name": "Rosół z kury z makaronem",
                "description": "Złocisty rosół gotowany 6 godzin, podawany z domowym makaronem i zieleniną",
                "allergens": ["gluten", "seler"],
            },
            {
                "name": "Barszcz czerwony z uszkami",
                "description": "Klasyczny barszcz z buraków z malutkimi uszkami z kapustą i grzybami",
                "allergens": ["gluten"],
            },
            {
                "name": "Krem z dyni z pestkami",
                "description": "Aksamitny krem z dyni hokkaido z prażonymi pestkami i olejem z pestek dyni",
                "allergens": [],
            },
            {
                "name": "Chłodnik litewski",
                "description": "Orzeźwiający różowy chłodnik z buraków, ogórkiem i jajkiem (sezonowo)",
                "allergens": ["mleko", "jaja"],
            },
        ],
    },
    "Dania Główne – Mięso": {
        "icon": "🥩",
        "description": "Serce menu weselnego – wybierz 1-2 dania główne",
        "dishes": [
            {
                "name": "Pierś z kaczki z sosem wiśniowym",
                "description": "Różowa pierś z kaczki confitowana, z redukcją wiśniową i anyżem",
                "allergens": ["seler"],
            },
            {
                "name": "Polędwica wołowa medium-rare",
                "description": "Polędwica wołowa z grilla, podawana z sosem bordelaise i masłem ziołowym",
                "allergens": ["mleko", "seler"],
            },
            {
                "name": "Kurczak faszerowany ricottą i szpinakiem",
                "description": "Rolada z piersi kurczaka z nadzieniem z ricotty, szpinaku i suszonych pomidorów",
                "allergens": ["mleko"],
            },
            {
                "name": "Żeberka wieprzone w miodzie i piwie",
                "description": "Długo pieczone żeberka wieprzowe w glazurze miodowo-piwnej z jabłkiem",
                "allergens": ["gluten", "seler"],
            },
            {
                "name": "Pieczeń cielęca z warzywami",
                "description": "Delikatna pieczeń cielęca duszona z warzywami korzeniowymi i tymiankiem",
                "allergens": ["seler"],
            },
        ],
    },
    "Dania Główne – Ryby & Wegetariańskie": {
        "icon": "🐟",
        "description": "Lżejsze alternatywy i opcje bezmięsne dla Waszych gości",
        "dishes": [
            {
                "name": "Łosoś pieczony z cytryną i koperkiem",
                "description": "Filet z łososia atlantyckiego pieczony w pergaminie z cytryną i świeżym koperkiem",
                "allergens": ["ryby"],
            },
            {
                "name": "Dorsz w panierce ziołowej",
                "description": "Filet z dorsza w chrupiącej panierce z ziołami, podawany z remoulade",
                "allergens": ["ryby", "gluten", "jaja", "mleko"],
            },
            {
                "name": "Risotto z grzybami leśnymi",
                "description": "Kremowe risotto z mieszanką grzybów leśnych, parmezanem i truflowym olejkiem",
                "allergens": ["mleko"],
            },
            {
                "name": "Tagine warzywne z ciecierzycą",
                "description": "Aromatyczna potrawka w stylu marokańskim z warzywami, ciecierzycą i kuskusem (vegan)",
                "allergens": ["gluten"],
            },
            {
                "name": "Quiche szpinakowy z kozim serem",
                "description": "Kruche ciasto z nadzieniem szpinakowym, kozim serem i karmelizowaną cebulą",
                "allergens": ["gluten", "jaja", "mleko"],
            },
        ],
    },
    "Dodatki & Garnitury": {
        "icon": "🥔",
        "description": "Wybierz 2-3 dodatki – pasujące zestawy podpowie Asystent Smaku",
        "dishes": [
            {
                "name": "Kopytka z boczkiem i cebulką",
                "description": "Domowe kopytka z ziemniaków, podsmażane na maśle z chrupiącym boczkiem",
                "allergens": ["gluten", "jaja"],
            },
            {
                "name": "Pierogi ruskie",
                "description": "Ręcznie lepione pierogi z farszem ziemniaczano-twarogowym ze śmietaną",
                "allergens": ["gluten", "jaja", "mleko"],
            },
            {
                "name": "Kluski śląskie",
                "description": "Tradycyjne kluski z dziurką, podawane z zasmażaną kapustą",
                "allergens": ["gluten", "jaja"],
            },
            {
                "name": "Ziemniaki pieczone z rozmarynem",
                "description": "Złociste ćwiartki ziemniaków pieczone z rozmarynem, czosnkiem i oliwą",
                "allergens": [],
            },
            {
                "name": "Bukiet warzyw sezonowych",
                "description": "Gotowane i glazurowane warzywa sezonowe z masłem ziołowym",
                "allergens": ["mleko"],
            },
            {
                "name": "Sałata z grillowaną brzoskwinią",
                "description": "Mix sałat z grillowaną brzoskwinią, orzechami włoskimi i vinaigrette balsamicznym",
                "allergens": ["orzechy"],
            },
        ],
    },
    "Desery": {
        "icon": "🍰",
        "description": "Słodkie zakończenie niezapomnianego wieczoru",
        "dishes": [
            {
                "name": "Tort weselny (do wyceny)",
                "description": "Indywidualnie projektowany tort weselny – skontaktuj się z nami po detale",
                "allergens": ["gluten", "jaja", "mleko"],
            },
            {
                "name": "Makaroniki francuskie",
                "description": "Kolorowe makaroniki w 4 smakach: wanilia, malina, pistacja, czekolada",
                "allergens": ["jaja", "orzechy", "mleko"],
            },
            {
                "name": "Sernik nowojorski",
                "description": "Kremowy sernik na kruchym spodzie z kulisem malinowym",
                "allergens": ["gluten", "jaja", "mleko"],
            },
            {
                "name": "Tiramisu klasyczne",
                "description": "Tradycyjne tiramisu z mascarpone, espresso i biszkoptami savoiardi",
                "allergens": ["gluten", "jaja", "mleko"],
            },
            {
                "name": "Sorbet owocowy (vegan)",
                "description": "Rzemieślniczy sorbet: mango-marakuja lub truskawka-bazylia",
                "allergens": [],
            },
        ],
    },
}

UPSELLS = [
    {
        "icon": "🍫",
        "name": "Fontanna czekoladowa",
        "description": "Belgijska czekolada z owocami, piankami i preclem. Atrakcja dla gości!",
        "price": 800,
    },
    {
        "icon": "🧀",
        "name": "Wiejski stół przekąskowy",
        "description": "Bogaty bufet zimnych przekąsek: sery, wędliny, przetwory, pieczywo",
        "price": 1200,
    },
    {
        "icon": "🥂",
        "name": "Pakiet napojów Premium",
        "description": "Nieograniczone wino, piwo kraftowe, wody mineralne i soki przez całą noc",
        "price": 2500,
    },
    {
        "icon": "🍾",
        "name": "Toast szampański",
        "description": "Kieliszek Prosecco lub szampana dla każdego gościa na toast",
        "price": 600,
    },
    {
        "icon": "🍕",
        "name": "Pizza o północy",
        "description": "Świeże pizze z pieca opalanego drewnem podawane późno w nocy",
        "price": 900,
    },
    {
        "icon": "☕",
        "name": "Stacja kawowa Barista",
        "description": "Profesjonalny barista przygotowujący espresso, cappuccino i latte art",
        "price": 1100,
    },
]

DIET_OPTIONS = ["Standardowa", "Wegetariańska", "Wegańska", "Bezglutenowa", "Bez laktozy", "Inne"]
