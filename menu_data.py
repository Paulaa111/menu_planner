MENU_DATA = {
    # ── PRZYSTAWKI ──────────────────────────────────────────────────────────
    "Przystawki": {
        "type": "single",          # wybór wielu dań z tej kategorii
        "description": "Eleganckie przystawki na start uczty weselnej",
        "dishes": [
            {"name": "Wiejski stół staropolski", "description": "Sery, wędliny, kiszonki, chleby wiejskie prosto z pieca", "allergens": ["gluten", "laktoza"], "price_per_person": 35},
            {"name": "Deska serów dojrzewających", "description": "Selekcja polskich serów z winogronami i orzechami włoskimi", "allergens": ["laktoza", "orzechy"], "price_per_person": 28},
            {"name": "Śledzie po polsku", "description": "Śledzie w trzech marynatach: z cebulką, w śmietanie i po kaszubsku", "allergens": ["ryby"], "price_per_person": 18},
            {"name": "Tatarski z polędwicy", "description": "Tradycyjny tatar z korniszonem, kaparami i żółtkiem", "allergens": ["jajka"], "price_per_person": 32},
        ],
    },

    # ── OBIAD I ──────────────────────────────────────────────────────────────
    "Obiad I – Zupa": {
        "type": "single",
        "description": "Wybierz jedną zupę do pierwszego obiadu",
        "meal_group": "Obiad I",
        "dishes": [
            {"name": "Żurek staropolski", "description": "Z białą kiełbasą, jajkiem i chrzanem, podawany w chlebie", "allergens": ["gluten", "jajka"], "price_per_person": 22},
            {"name": "Rosół z kury wiejskiej", "description": "Złocisty bulion gotowany 6 godzin, z makaronem lane ciasto", "allergens": ["gluten", "jajka"], "price_per_person": 18},
            {"name": "Barszcz czerwony z uszkami", "description": "Klasyczny barszcz z uszkami z grzybami leśnymi", "allergens": ["gluten"], "price_per_person": 20},
            {"name": "Krupnik z pęczaku", "description": "Sycąca zupa z pęczaku z warzywami i skwarkami", "allergens": ["gluten"], "price_per_person": 19},
        ],
    },
    "Obiad I – Danie Główne": {
        "type": "single",
        "description": "Wybierz główne danie mięsne lub rybne",
        "meal_group": "Obiad I",
        "dishes": [
            {"name": "Kaczka pieczona z jabłkami", "description": "Kaczka faszerowana jabłkami i majerankiem, pieczona przez 4 godziny", "allergens": [], "price_per_person": 89},
            {"name": "Schab po staropolsku", "description": "Schab duszony z suszonymi śliwkami i miodem, z naturalnym sosem", "allergens": [], "price_per_person": 65},
            {"name": "Pstrąg z polskich hodowli", "description": "Pstrąg pieczony z masłem ziołowym, cytryną i koperkiem", "allergens": ["ryby", "laktoza"], "price_per_person": 72},
            {"name": "Kurczak wiejski duszony", "description": "Kurczak duszony z grzybami leśnymi w śmietanie, z natką", "allergens": ["laktoza"], "price_per_person": 55},
        ],
    },
    "Obiad I – Dodatek": {
        "type": "single",
        "description": "Wybierz skrobiowy dodatek do dania głównego",
        "meal_group": "Obiad I",
        "dishes": [
            {"name": "Kopytka z boczkiem", "description": "Domowe kopytka z chrupiącym boczkiem i cebulką", "allergens": ["gluten", "jajka"], "price_per_person": 15},
            {"name": "Pierogi ruskie", "description": "Z serem twarogowym, ziemniakami i cebulką, okraszone masłem", "allergens": ["gluten", "laktoza", "jajka"], "price_per_person": 18},
            {"name": "Kluski śląskie", "description": "Tradycyjne kluski z okrągłym otworem, podawane ze skwarkami", "allergens": ["gluten", "jajka"], "price_per_person": 14},
            {"name": "Ziemniaki zapiekane z rozmarynem", "description": "Młode ziemniaki z rozmarynem, czosnkiem i masłem", "allergens": ["laktoza"], "price_per_person": 10},
        ],
    },
    "Obiad I – Sałatka": {
        "type": "single",
        "description": "Wybierz świeżą sałatkę do pierwszego obiadu",
        "meal_group": "Obiad I",
        "dishes": [
            {"name": "Sałatka z buraków z kozim serem", "description": "Pieczone buraki, kozi ser, orzechy, roszponka i vinaigrette z miodem", "allergens": ["laktoza", "orzechy"], "price_per_person": 16},
            {"name": "Sałatka Cezar po polsku", "description": "Sałata masłowa, grzanki żytnie, parmezan i sos Cezar z anchois", "allergens": ["gluten", "laktoza", "ryby", "jajka"], "price_per_person": 14},
            {"name": "Surówka z kapusty białej", "description": "Klasyczna surówka z marchewką, jabłkiem i kminkiem", "allergens": [], "price_per_person": 8},
            {"name": "Warzywa grillowane sezonowe", "description": "Cukinia, papryka, bakłażan z oliwą i ziołami prowansalskimi", "allergens": [], "price_per_person": 12},
        ],
    },

    # ── OBIAD II ─────────────────────────────────────────────────────────────
    "Obiad II – Danie Główne": {
        "type": "single",
        "description": "Drugie danie główne — bez zupy",
        "meal_group": "Obiad II",
        "dishes": [
            {"name": "Polędwiczki wieprzowe w sosie grzybowym", "description": "Delikatne polędwiczki z sosem z leśnych grzybów i śmietany", "allergens": ["laktoza"], "price_per_person": 78},
            {"name": "Łosoś pieczony na łóżku z warzyw", "description": "Filet z łososia z cytryną, koprem i sezonowymi warzywami", "allergens": ["ryby"], "price_per_person": 75},
            {"name": "Żeberka wołowe BBQ", "description": "Wołowe żeberka marynowane przez 48h, pieczone do miękkości", "allergens": [], "price_per_person": 95},
            {"name": "Pierś z indyka nadziewana szpinakiem", "description": "Soczysty indyk z farszem szpinakowym i serem feta", "allergens": ["laktoza"], "price_per_person": 62},
        ],
    },
    "Obiad II – Dodatek": {
        "type": "single",
        "description": "Wybierz skrobiowy dodatek do drugiego obiadu",
        "meal_group": "Obiad II",
        "dishes": [
            {"name": "Kasza gryczana ze skwarkami", "description": "Prażona kasza gryczana z cebulką i boczkiem", "allergens": [], "price_per_person": 11},
            {"name": "Ryż z warzywami", "description": "Sypki ryż długoziarnisty z marchewką, groszkiem i kukurydzą", "allergens": [], "price_per_person": 9},
            {"name": "Puree ziemniaczane z masłem", "description": "Kremowe puree z masłem i szczypiorkiem", "allergens": ["laktoza"], "price_per_person": 10},
            {"name": "Frytki z pieca z rozmarynem", "description": "Chrupiące frytki z pieca z rozmarynem i fleur de sel", "allergens": [], "price_per_person": 12},
        ],
    },
    "Obiad II – Sałatka": {
        "type": "single",
        "description": "Wybierz sałatkę do drugiego obiadu",
        "meal_group": "Obiad II",
        "dishes": [
            {"name": "Sałatka grecka", "description": "Pomidory, ogórek, oliwki, feta, cebula i oregano", "allergens": ["laktoza"], "price_per_person": 13},
            {"name": "Coleslaw domowy", "description": "Kapusta pekińska, marchew, majonez i musztarda", "allergens": ["jajka"], "price_per_person": 9},
            {"name": "Sałata mix z pomidorkami cherry", "description": "Mieszanka sałat, pomidorki, rzodkiewki, vinaigrette cytrynowe", "allergens": [], "price_per_person": 11},
            {"name": "Sałatka z quinoa i awokado", "description": "Quinoa, awokado, ogórek, mięta i sos tahini", "allergens": ["sezam"], "price_per_person": 17},
        ],
    },

    # ── KOLACJA ───────────────────────────────────────────────────────────────
    "Kolacja – Danie Główne": {
        "type": "single",
        "description": "Lżejsze danie wieczorne",
        "meal_group": "Kolacja",
        "dishes": [
            {"name": "Bigos staropolski", "description": "Bigos gotowany przez 3 dni z kapusty kiszonej, grzybów i mięs", "allergens": [], "price_per_person": 35},
            {"name": "Gołąbki w sosie pomidorowym", "description": "Klasyczne gołąbki z mięsem i ryżem w domowym sosie pomidorowym", "allergens": ["gluten"], "price_per_person": 32},
            {"name": "Leczo z kiełbasą", "description": "Papryka, cukinia, kiełbasa i pomidory duszone z ziołami", "allergens": [], "price_per_person": 28},
            {"name": "Risotto z grzybami leśnymi", "description": "Kremowe risotto z borowikami, parmezanem i truflowym olejem", "allergens": ["laktoza"], "price_per_person": 38},
        ],
    },
    "Kolacja – Dodatek": {
        "type": "single",
        "description": "Wybierz dodatek do kolacji",
        "meal_group": "Kolacja",
        "dishes": [
            {"name": "Chleb wiejski z masłem", "description": "Świeży chleb wiejski ze smalcem, masłem i szczypiorkiem", "allergens": ["gluten", "laktoza"], "price_per_person": 6},
            {"name": "Ziemniaki z koperkiem", "description": "Gotowane ziemniaki okraszone masłem i koperkiem", "allergens": ["laktoza"], "price_per_person": 7},
            {"name": "Kasza jaglana z masłem", "description": "Lekka kasza jaglana z masłem i prażonymi pestkami dyni", "allergens": ["laktoza"], "price_per_person": 9},
        ],
    },
    "Kolacja – Sałatka": {
        "type": "single",
        "description": "Wybierz sałatkę wieczorną",
        "meal_group": "Kolacja",
        "dishes": [
            {"name": "Sałatka z rukolą i parmezanem", "description": "Rukola, płatki parmezanu, suszone pomidory, balsamico", "allergens": ["laktoza"], "price_per_person": 14},
            {"name": "Sałatka jarzynowa", "description": "Klasyczna sałatka jarzynowa z majonezem, w stylu babcinym", "allergens": ["jajka"], "price_per_person": 10},
            {"name": "Pomidory z cebulą i bazylią", "description": "Sezonowe pomidory z czerwoną cebulą, świeżą bazylią i oliwą", "allergens": [], "price_per_person": 8},
        ],
    },

    # ── BARSZCZE ─────────────────────────────────────────────────────────────
    "Barszcze & Przekąski Nocne": {
        "type": "multi",
        "description": "Późnonocna uczta — tradycyjne barszcze i gorące przekąski",
        "dishes": [
            {"name": "Barszcz czerwony z pasztecikam", "description": "Klarowny barszcz z gorącymi pasztecikam z grzybami", "allergens": ["gluten", "jajka"], "price_per_person": 14},
            {"name": "Barszcz biały z jajkiem", "description": "Kremowy barszcz biały z jajkiem, kiełbasą i chrzanem", "allergens": ["gluten", "jajka"], "price_per_person": 16},
            {"name": "Flaczki wołowe", "description": "Tradycyjne flaczki w aromatycznym bulionie wołowym z majerankiem", "allergens": [], "price_per_person": 18},
            {"name": "Żurek z koszyczkiem", "description": "Żurek z ziemniakami, jajkiem i białą kiełbasą w chlebowym koszyczku", "allergens": ["gluten", "jajka"], "price_per_person": 20},
        ],
    },

    # ── ZIMNA PŁYTA ───────────────────────────────────────────────────────────
    "Zimna Płyta": {
        "type": "multi",
        "description": "Zimne przekąski dostępne przez całą imprezę — tortille, wrapy, finger food",
        "dishes": [
            {"name": "Wiejski stół z wędlinami", "description": "Selekcja polskich wędlin, serów wiejskich, ogórków i chlebów", "allergens": ["gluten", "laktoza"], "price_per_person": 30},
            {"name": "Tortille z kurczakiem i warzywami", "description": "Tortille z grillowanym kurczakiem, awokado, papryką i sosem jogurtowym", "allergens": ["gluten", "laktoza"], "price_per_person": 22},
            {"name": "Mini kanapki na ciemnym chlebie", "description": "Kanapki z różnymi nadzieniami: łosoś, szynka parmeńska, pastramii", "allergens": ["gluten", "ryby"], "price_per_person": 25},
            {"name": "Bruschetta z pomidorami", "description": "Grzanki z focacci, pomidorami, czosnkiem i świeżą bazylią", "allergens": ["gluten"], "price_per_person": 14},
            {"name": "Roladki z łososia z serkiem", "description": "Plasterki łososia wędzonego z twarogiem, kaparami i cytryną", "allergens": ["ryby", "laktoza"], "price_per_person": 28},
            {"name": "Mini tartaletki z pastą z wątróbki", "description": "Kruche tartaletki z domową pastą z wątróbki drobiowej i konfiturą", "allergens": ["gluten", "jajka"], "price_per_person": 18},
            {"name": "Warzywna deska z dipami", "description": "Marchew, seler, ogórek, rzodkiewka z hummusem, tzatziki i guacamole", "allergens": ["sezam", "laktoza"], "price_per_person": 15},
        ],
    },

    # ── DESERY ────────────────────────────────────────────────────────────────
    "Desery": {
        "type": "multi",
        "description": "Słodkie zakończenie wyjątkowego wieczoru",
        "dishes": [
            {"name": "Tort weselny wielopiętrowy", "description": "Tort na zamówienie wg projektu Pary Młodej, z masą maślaną", "allergens": ["gluten", "laktoza", "jajka"], "price_per_person": 45},
            {"name": "Sernik babci Zosi", "description": "Pieczony sernik na kruchym spodzie z konfiturą z czarnej porzeczki", "allergens": ["laktoza", "jajka", "gluten"], "price_per_person": 22},
            {"name": "Lody rzemieślnicze", "description": "Trzy smaki do wyboru z domowymi waflami i bitą śmietaną", "allergens": ["laktoza", "gluten"], "price_per_person": 20},
            {"name": "Jabłecznik z lodami", "description": "Ciepła szarlotka z cynamonem, podawana z gałką lodów waniliowych", "allergens": ["gluten", "laktoza", "jajka"], "price_per_person": 18},
        ],
    },
}

# ── Kolejność grup posiłków ───────────────────────────────────────────────────
MEAL_GROUPS_ORDER = ["Przystawki", "Obiad I", "Obiad II", "Kolacja", "Barszcze & Przekąski Nocne", "Zimna Płyta", "Desery"]

UPSELLS = [
    {
        "name": "Stacja Sushi",
        "description": "Żywe sushi na specjalnej wyspie — kucharz przygotowuje na oczach gości",
        "price": 3500,
    },
    {
        "name": "Stacja Makaronów",
        "description": "Włoskie makarony gotowane na żywo z wyborem sosów i dodatków",
        "price": 1800,
    },
    {
        "name": "Candy Bar",
        "description": "Słodki stół z pralinkami, macarons, owocami i domowymi ciasteczkami",
        "price": 2200,
    },
    {
        "name": "Degustacja Serów",
        "description": "Selekcja 12 polskich i europejskich serów z sommelierem i konfiturami",
        "price": 1500,
    },
    {
        "name": "Nocna Grochówka",
        "description": "Tradycyjna grochówka z wędzonym boczkiem, serwowana o północy",
        "price": 900,
    },
    {
        "name": "Stacja Pierogów",
        "description": "Pierogi lepione i gotowane na żywo — kilka rodzajów nadzienia do wyboru",
        "price": 1600,
    },
]

DIET_OPTIONS = ["wegetariańskie", "wegańskie", "bezglutenowe", "bezlaktozowe", "halal", "kosher"]
