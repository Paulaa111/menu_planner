import streamlit as st
import pandas as pd
import json
from datetime import datetime
from anthropic import Anthropic
from menu_data import MENU_DATA, UPSELLS, DIET_OPTIONS
from utils import calculate_summary, export_to_csv

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Menu Weselne",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        font-weight: 300;
        color: #1B2A4A;
    }
    h1, h2, h3, .serif {
        font-family: 'DM Serif Display', serif !important;
        font-weight: 400 !important;
    }

    /* ── Paleta ──────────────────────────────────────────────────────────────
       Granat:        #1B2A4A
       Granat jasny:  #2C3F66
       Krem:          #FAF7F2
       Krem ciemny:   #F0EBE3
       Akcent złoty:  #C4975A
       Tekst ciemny:  #1B2A4A
       Tekst medium:  #3D4F6A
       Tekst jasny:   #6A7D96
    ───────────────────────────────────────────────────────────────────────── */

    .stApp {
        background: #FAF7F2;
    }

    /* ── Sidebar ─────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #1B2A4A !important;
    }
    [data-testid="stSidebar"] * {
        color: #E8E4DC !important;
    }
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stTextArea textarea {
        background: #243660 !important;
        border: 1px solid #3A5080 !important;
        color: #E8E4DC !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] label {
        color: #8A9AB0 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #243660 !important;
    }

    /* ── Grupowe nagłówki posiłków ───────────────────────────────────────── */
    .meal-group-header {
        background: #1B2A4A;
        border-radius: 14px 14px 0 0;
        padding: 1.1rem 2rem 1rem;
        margin-top: 2.5rem;
        margin-bottom: 0;
    }
    .meal-group-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem;
        color: #FAF7F2;
        margin: 0;
        line-height: 1.2;
    }
    .meal-group-subtitle {
        font-size: 0.7rem;
        color: #8A9AB0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 3px;
    }

    /* ── Karty kategorii ─────────────────────────────────────────────────── */
    .cat-card {
        background: #FFFFFF;
        border-radius: 0 0 0 0;
        padding: 1.5rem 2rem 1.25rem;
        border-left: 3px solid #C4975A;
        border-bottom: 1px solid #EDE8E0;
    }
    .cat-card:last-of-type,
    .cat-card-last {
        border-radius: 0 0 14px 14px;
        border-bottom: none;
    }
    .cat-card-standalone {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.5rem 2rem 1.25rem;
        border-left: 3px solid #C4975A;
        margin-top: 2.5rem;
        margin-bottom: 0;
        box-shadow: 0 2px 12px rgba(27,42,74,0.06);
    }
    .cat-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.15rem;
        color: #1B2A4A;
        margin: 0 0 0.2rem 0;
    }
    .cat-desc {
        font-size: 0.75rem;
        color: #6A7D96;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }

    /* ── Kafelki dań ─────────────────────────────────────────────────────── */
    .dish-detail {
        border-left: 3px solid #C4975A;
        background: #FAF7F2;
        border-radius: 0 10px 10px 0;
        padding: 0.65rem 0.9rem;
        margin: 0.5rem 0;
    }
    .dish-name {
        font-weight: 500;
        font-size: 0.9rem;
        color: #1B2A4A;
    }
    .dish-desc {
        font-size: 0.78rem;
        color: #3D4F6A;
        margin-top: 2px;
    }
    .dish-price {
        font-size: 0.8rem;
        color: #C4975A;
        font-weight: 500;
        margin-top: 4px;
    }
    .allergen-tag {
        display: inline-block;
        background: #F0EBE3;
        border: 1px solid #DDD5C8;
        border-radius: 20px;
        padding: 1px 8px;
        font-size: 0.68rem;
        color: #3D4F6A;
        margin-right: 3px;
        margin-top: 3px;
    }

    /* ── AI bubble ───────────────────────────────────────────────────────── */
    .ai-bubble {
        background: #EEF1F7;
        border: 1px solid #C8D4E8;
        border-left: 3px solid #1B2A4A;
        border-radius: 0 12px 12px 0;
        padding: 0.75rem 1rem;
        margin: 0.75rem 0;
        font-size: 0.85rem;
        color: #1B2A4A;
        font-style: italic;
        line-height: 1.6;
    }

    /* ── Upsell karty ────────────────────────────────────────────────────── */
    .upsell-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1rem;
        border-top: 2px solid #C4975A;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(27,42,74,0.05);
    }
    .upsell-name {
        font-weight: 500;
        font-size: 0.9rem;
        color: #1B2A4A;
    }
    .upsell-price {
        font-size: 0.8rem;
        color: #C4975A;
        margin-top: 4px;
        font-weight: 500;
    }
    .upsell-desc {
        font-size: 0.78rem;
        color: #3D4F6A;
        margin-top: 3px;
    }

    /* ── Metryki podsumowania ────────────────────────────────────────────── */
    .summary-metric {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.25rem;
        border-top: 3px solid #1B2A4A;
        text-align: center;
        box-shadow: 0 2px 8px rgba(27,42,74,0.06);
    }
    .metric-value {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: #1B2A4A;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #6A7D96;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.5rem;
    }

    /* ── Pole kosztów ────────────────────────────────────────────────────── */
    .cost-box {
        background: #1B2A4A;
        color: #FAF7F2;
        border-radius: 14px;
        padding: 1.75rem 2rem;
        margin: 1.25rem 0;
    }
    .cost-label {
        font-size: 0.72rem;
        color: #8A9AB0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .cost-value {
        font-family: 'DM Serif Display', serif;
        font-size: 3rem;
        color: #FAF7F2;
        line-height: 1.1;
        margin-top: 0.25rem;
    }
    .cost-note {
        font-size: 0.78rem;
        color: #8A9AB0;
        margin-top: 0.5rem;
    }

    /* ── Podgląd podsumowania ────────────────────────────────────────────── */
    .summary-preview {
        background: #1B2A4A;
        border-radius: 14px;
        padding: 1.4rem 2rem;
        margin: 1.5rem 0 0.5rem 0;
        color: #FAF7F2;
    }
    .summary-preview-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.25rem;
        color: #FAF7F2;
        margin-bottom: 0.75rem;
    }
    .summary-preview-row {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #2C3F66;
        padding: 0.35rem 0;
        font-size: 0.84rem;
        color: #C8D4E8;
    }
    .summary-preview-row:last-child { border-bottom: none; }
    .summary-preview-total {
        font-size: 1.35rem;
        color: #C4975A;
        font-weight: 500;
        margin-top: 0.9rem;
        font-family: 'DM Serif Display', serif;
    }

    /* ── Taby ────────────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1px solid #DDD5C8;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #6A7D96 !important;
        padding: 0.75rem 1.5rem !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1B2A4A !important;
        border-bottom: 2px solid #C4975A !important;
    }

    /* ── Przyciski ───────────────────────────────────────────────────────── */
    .stButton>button {
        background: #1B2A4A !important;
        color: #FAF7F2 !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        font-weight: 400 !important;
        padding: 0.5rem 1.5rem !important;
        transition: opacity 0.15s !important;
    }
    .stButton>button:hover {
        opacity: 0.85 !important;
    }

    /* ── Multiselect ─────────────────────────────────────────────────────── */
    [data-baseweb="tag"] {
        background: #1B2A4A !important;
        border-radius: 20px !important;
    }
    [data-baseweb="tag"] span {
        color: #FAF7F2 !important;
        font-size: 0.78rem !important;
    }
    [data-baseweb="select"] {
        border-radius: 10px !important;
    }

    /* ── Chat ────────────────────────────────────────────────────────────── */
    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border-radius: 12px !important;
        border: none !important;
    }

    /* ── Przyciski pobierania ────────────────────────────────────────────── */
    .stDownloadButton>button {
        background: transparent !important;
        color: #1B2A4A !important;
        border: 1.5px solid #1B2A4A !important;
        font-size: 0.72rem !important;
        border-radius: 12px !important;
    }
    .stDownloadButton>button:hover {
        background: #1B2A4A !important;
        color: #FAF7F2 !important;
    }

    /* ── Divider ─────────────────────────────────────────────────────────── */
    hr {
        border-color: #DDD5C8 !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Etykieta sekcji ─────────────────────────────────────────────────── */
    .section-label {
        font-size: 0.68rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6A7D96;
        margin-bottom: 1.25rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #DDD5C8;
    }

    /* ── Intro box ───────────────────────────────────────────────────────── */
    .wedding-intro {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        border-left: 4px solid #C4975A;
        box-shadow: 0 2px 10px rgba(27,42,74,0.05);
    }
    .wedding-intro p {
        color: #1B2A4A !important;
        font-size: 0.88rem;
        line-height: 1.7;
        margin: 0;
    }
    .wedding-intro .intro-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.1rem;
        color: #1B2A4A !important;
        margin-bottom: 0.5rem;
    }

    /* ── Checkbox ────────────────────────────────────────────────────────── */
    .stCheckbox label {
        color: #1B2A4A !important;
        font-size: 0.88rem !important;
    }

    /* ── Dataframe ───────────────────────────────────────────────────────── */
    [data-testid="stDataFrame"] {
        border-radius: 10px !important;
        overflow: hidden;
    }

    /* ── Tekst na jasnym tle ─────────────────────────────────────────────── */
    p, span, div, label {
        color: #1B2A4A;
    }

    /* ── Ukryj branding ──────────────────────────────────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Usuń domyślne marginesy Streamlit nad widgetami ─────────────────── */
    .block-container {
        padding-top: 2rem !important;
    }
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "selections": {},
    "guest_count": 100,
    "chat_history": [],
    "couple_name": "",
    "dietary_notes": {},
    "show_summary_preview": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

client = Anthropic()

# ── AI helpers ────────────────────────────────────────────────────────────────
def get_ai_suggestion(context: str) -> str:
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=180,
            system=(
                "Jesteś eleganckim asystentem kulinarnym polskiej restauracji weselnej. "
                "Odpowiadaj krótko (2 zdania), ciepło i po polsku, bez emoji. "
                "Doradzaj pasujące dodatki i kompozycje smakowe."
            ),
            messages=[{"role": "user", "content": context}],
        )
        return resp.content[0].text
    except Exception:
        return None


def ai_chat(user_msg: str) -> str:
    history = st.session_state.chat_history[-10:]
    messages = history + [{"role": "user", "content": user_msg}]
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=(
                "Jesteś Asystentem Smaku w ekskluzywnej polskiej restauracji weselnej. "
                "Pomagasz parze młodej skonfigurować idealne menu weselne. "
                "Znasz całą ofertę restauracji. "
                "Odpowiadaj po polsku, bez emoji, ciepło i profesjonalnie. "
                "Sugeruj harmonijne kompozycje smakowe."
            ),
            messages=messages,
        )
        return resp.content[0].text
    except Exception:
        return "Przepraszam, wystąpił chwilowy problem. Spróbuj ponownie za chwilę."


# ── Pomocnicze: grupy posiłków ────────────────────────────────────────────────
# Kategorie pogrupowane wg posiłku
MEAL_GROUPS = {
    "Przystawki":                ["Przystawki"],
    "Obiad I":                   ["Obiad I – Zupa", "Obiad I – Danie Główne", "Obiad I – Dodatek", "Obiad I – Sałatka"],
    "Obiad II":                  ["Obiad II – Danie Główne", "Obiad II – Dodatek", "Obiad II – Sałatka"],
    "Kolacja":                   ["Kolacja – Danie Główne", "Kolacja – Dodatek", "Kolacja – Sałatka"],
    "Barszcze & Przekąski Nocne":["Barszcze & Przekąski Nocne"],
    "Zimna Płyta":               ["Zimna Płyta"],
    "Desery":                    ["Desery"],
}

# Etykieta podkategorii (część po " – ")
def sub_label(cat: str) -> str:
    return cat.split(" – ")[-1] if " – " in cat else cat

# Czy kategoria jest pierwszą w grupie?
def is_first_in_group(cat: str, group_cats: list) -> bool:
    return group_cats[0] == cat

# Czy kategoria jest ostatnią w grupie?
def is_last_in_group(cat: str, group_cats: list) -> bool:
    return group_cats[-1] == cat


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-family:DM Serif Display,serif; font-size:1.4rem; color:#E8E4DC; margin:0;'>Konfiguracja</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size:0.7rem; color:#8A9AB0; letter-spacing:0.1em; text-transform:uppercase; margin-top:2px;'>Dane podstawowe</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#243660; margin:0.75rem 0;'>", unsafe_allow_html=True)

    st.session_state.couple_name = st.text_input("Para Młoda", placeholder="Anna & Michał")
    wedding_date = st.date_input("Data uroczystości", min_value=datetime.today())
    st.session_state.guest_count = st.number_input(
        "Liczba gości", min_value=10, max_value=1000, value=100, step=5
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.7rem; color:#8A9AB0; letter-spacing:0.1em; text-transform:uppercase;'>Diety specjalne</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#243660; margin:0.5rem 0;'>", unsafe_allow_html=True)

    vege       = st.number_input("Wegetarianie",  min_value=0, max_value=st.session_state.guest_count, value=0)
    vegan      = st.number_input("Weganie",        min_value=0, max_value=st.session_state.guest_count, value=0)
    gluten_free= st.number_input("Bezglutenowi",   min_value=0, max_value=st.session_state.guest_count, value=0)
    allergy_notes = st.text_area("Pozostałe uwagi", placeholder="alergie, preferencje...")

    st.session_state.dietary_notes = {
        "vegetarian": vege,
        "vegan": vegan,
        "gluten_free": gluten_free,
        "other": allergy_notes,
    }

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#243660; margin:0.5rem 0;'>", unsafe_allow_html=True)
    total_selected = sum(len(v) for v in st.session_state.selections.values() if isinstance(v, list))
    st.markdown(
        f"<p style='font-size:0.72rem; color:#8A9AB0;'>Wybrano dań: <strong style='color:#E8E4DC;'>{total_selected}</strong></p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='font-size:0.72rem; color:#8A9AB0;'>Liczba gości: <strong style='color:#E8E4DC;'>{st.session_state.guest_count}</strong></p>",
        unsafe_allow_html=True,
    )


# ── HEADER ────────────────────────────────────────────────────────────────────
couple = st.session_state.couple_name or ""

col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    if couple:
        st.markdown(
            "<p style='font-size:0.72rem; color:#6A7D96; letter-spacing:0.12em; text-transform:uppercase; margin:0 0 4px;'>Konfiguracja menu</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h1 style='font-family:DM Serif Display,serif; font-size:2.8rem; color:#1B2A4A; margin:0; line-height:1.1;'>{couple}</h1>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<p style='font-size:0.72rem; color:#6A7D96; letter-spacing:0.12em; text-transform:uppercase; margin:0 0 4px;'>Konfigurator</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h1 style='font-family:DM Serif Display,serif; font-size:2.8rem; color:#1B2A4A; margin:0; line-height:1.1;'>Menu Weselne</h1>",
            unsafe_allow_html=True,
        )

st.markdown("<hr>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["Menu", "Asystent Smaku", "Podsumowanie"])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 – MENU
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:

    # Intro
    st.markdown("""
    <div class="wedding-intro">
        <p class="intro-title">Skomponuj swoje wesele</p>
        <p>
            Tworzymy menu weselne z sercem — korzystamy z produktów lokalnych dostawców
            i sprawdzonych polskich przepisów przekazywanych z pokolenia na pokolenie.
            Wybierz dania z każdej kategorii, a nasz Asystent Smaku podpowie,
            co do siebie pasuje.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Iteruj po grupach posiłków
    for group_name, group_cats in MEAL_GROUPS.items():
        is_single_cat = len(group_cats) == 1

        if is_single_cat:
            # Pojedyncza kategoria — standalone card
            cat = group_cats[0]
            items = MENU_DATA.get(cat, {})
            if not items:
                continue

            st.markdown(
                f"""<div class="cat-card-standalone">
                    <p class="cat-title">{cat}</p>
                    <p class="cat-desc">{items.get('description', '')}</p>
                </div>""",
                unsafe_allow_html=True,
            )

            # multiselect BEZ pustej etykiety
            prev = st.session_state.selections.get(cat, [])
            chosen = st.multiselect(
                label=cat,
                options=[d["name"] for d in items["dishes"]],
                default=prev,
                key=f"select_{cat}",
                label_visibility="collapsed",
            )
            st.session_state.selections[cat] = chosen

            if chosen and chosen != prev:
                with st.spinner(""):
                    tip = get_ai_suggestion(
                        f"Para wybrała do kategorii '{cat}': {', '.join(chosen)}. "
                        "Zaproponuj krótko pasujące danie lub dodatek z naszej oferty."
                    )
                if tip:
                    st.markdown(f'<div class="ai-bubble">{tip}</div>', unsafe_allow_html=True)

            if chosen:
                cols = st.columns(min(len(chosen), 3))
                for idx, dish_name in enumerate(chosen):
                    dish = next((d for d in items["dishes"] if d["name"] == dish_name), None)
                    if dish:
                        with cols[idx % 3]:
                            allergen_html = "".join(
                                f'<span class="allergen-tag">{a}</span>'
                                for a in dish.get("allergens", [])
                            )
                            price = dish.get("price_per_person")
                            total_p = price * st.session_state.guest_count if price else None
                            st.markdown(
                                f"""<div class="dish-detail">
                                    <p class="dish-name">{dish['name']}</p>
                                    <p class="dish-desc">{dish.get('description','')}</p>
                                    {"<p class='dish-price'>~" + str(price) + " zł / os. &nbsp;·&nbsp; " + str(total_p) + " zł łącznie</p>" if price else ""}
                                    <div style="margin-top:4px;">{allergen_html}</div>
                                </div>""",
                                unsafe_allow_html=True,
                            )

        else:
            # Grupa z kilkoma kategoriami (Obiad I, II, Kolacja)
            # Nagłówek grupy
            st.markdown(
                f"""<div class="meal-group-header">
                    <p class="meal-group-title">{group_name}</p>
                    <p class="meal-group-subtitle">Wybierz po jednym daniu z każdej sekcji</p>
                </div>""",
                unsafe_allow_html=True,
            )

            for ci, cat in enumerate(group_cats):
                items = MENU_DATA.get(cat, {})
                if not items:
                    continue

                is_last = (ci == len(group_cats) - 1)
                card_extra = "cat-card-last" if is_last else ""

                st.markdown(
                    f"""<div class="cat-card {card_extra}">
                        <p class="cat-title">{sub_label(cat)}</p>
                        <p class="cat-desc">{items.get('description', '')}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )

                prev = st.session_state.selections.get(cat, [])
                chosen = st.multiselect(
                    label=cat,
                    options=[d["name"] for d in items["dishes"]],
                    default=prev,
                    key=f"select_{cat}",
                    label_visibility="collapsed",
                )
                st.session_state.selections[cat] = chosen

                if chosen and chosen != prev:
                    with st.spinner(""):
                        tip = get_ai_suggestion(
                            f"Para wybrała do kategorii '{cat}': {', '.join(chosen)}. "
                            "Zaproponuj krótko pasujące danie lub dodatek z naszej oferty."
                        )
                    if tip:
                        st.markdown(f'<div class="ai-bubble">{tip}</div>', unsafe_allow_html=True)

                if chosen:
                    cols = st.columns(min(len(chosen), 3))
                    for idx, dish_name in enumerate(chosen):
                        dish = next((d for d in items["dishes"] if d["name"] == dish_name), None)
                        if dish:
                            with cols[idx % 3]:
                                allergen_html = "".join(
                                    f'<span class="allergen-tag">{a}</span>'
                                    for a in dish.get("allergens", [])
                                )
                                price = dish.get("price_per_person")
                                total_p = price * st.session_state.guest_count if price else None
                                st.markdown(
                                    f"""<div class="dish-detail">
                                        <p class="dish-name">{dish['name']}</p>
                                        <p class="dish-desc">{dish.get('description','')}</p>
                                        {"<p class='dish-price'>~" + str(price) + " zł / os. &nbsp;·&nbsp; " + str(total_p) + " zł łącznie</p>" if price else ""}
                                        <div style="margin-top:4px;">{allergen_html}</div>
                                    </div>""",
                                    unsafe_allow_html=True,
                                )

    # ── Dodatki Premium ───────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Dodatki Premium</p>', unsafe_allow_html=True)

    up_cols = st.columns(3)
    selected_upsells = st.session_state.selections.get("_upsells", [])
    new_upsells = []

    for i, upsell in enumerate(UPSELLS):
        with up_cols[i % 3]:
            checked = st.checkbox(
                upsell["name"],
                value=upsell["name"] in selected_upsells,
                key=f"upsell_{upsell['name']}",
            )
            st.markdown(
                f"""<div class="upsell-card">
                    <p class="upsell-name">{upsell['name']}</p>
                    <p class="upsell-desc">{upsell['description']}</p>
                    {"<p class='upsell-price'>od " + str(upsell['price']) + " zł</p>" if upsell.get('price') else ""}
                </div>""",
                unsafe_allow_html=True,
            )
            if checked:
                new_upsells.append(upsell["name"])

    st.session_state.selections["_upsells"] = new_upsells

    # ── Przycisk Podsumowania ─────────────────────────────────────────────────
    total_dishes_now = sum(
        len(v) for k, v in st.session_state.selections.items()
        if isinstance(v, list) and k != "_upsells"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    if total_dishes_now > 0:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("Podsumuj wybrane menu", use_container_width=True):
                st.session_state.show_summary_preview = not st.session_state.show_summary_preview

        if st.session_state.show_summary_preview:
            summary_now = calculate_summary(
                st.session_state.selections,
                st.session_state.guest_count,
                MENU_DATA,
                UPSELLS,
            )
            rows_html = ""
            for cat, dishes in summary_now["breakdown"].items():
                if dishes:
                    for d in dishes:
                        dish_obj = next(
                            (di for di in MENU_DATA.get(cat, {}).get("dishes", []) if di["name"] == d), None
                        )
                        price_txt = f"{dish_obj['price_per_person']} zł/os." if dish_obj and dish_obj.get("price_per_person") else "—"
                        rows_html += f"""
                        <div class="summary-preview-row">
                            <span><span style="color:#6A9AB0; font-size:0.72rem;">{cat}</span> &nbsp;·&nbsp; {d}</span>
                            <span style="color:#C4975A;">{price_txt}</span>
                        </div>"""

            for u_name in st.session_state.selections.get("_upsells", []):
                u_obj = next((x for x in UPSELLS if x["name"] == u_name), None)
                price_txt = f"od {u_obj['price']} zł" if u_obj and u_obj.get("price") else "—"
                rows_html += f"""
                <div class="summary-preview-row">
                    <span><span style="color:#6A9AB0; font-size:0.72rem;">Dodatek</span> &nbsp;·&nbsp; {u_name}</span>
                    <span style="color:#C4975A;">{price_txt}</span>
                </div>"""

            cost_txt = (
                f"Szacunkowy koszt: {summary_now['estimated_cost']:,} zł"
                if summary_now["estimated_cost"] > 0
                else ""
            )

            st.markdown(
                f"""<div class="summary-preview">
                    <p class="summary-preview-title">Twoje wybory</p>
                    {rows_html}
                    {"<p class='summary-preview-total'>" + cost_txt + "</p>" if cost_txt else ""}
                </div>""",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<p style='text-align:center; color:#6A7D96; font-size:0.82rem; padding:1rem 0;'>Wybierz przynajmniej jedno danie, aby zobaczyć podsumowanie.</p>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 – ASYSTENT
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="section-label">Asystent Smaku</p>', unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem; color:#3D4F6A; margin-bottom:1.5rem;'>Zapytaj o kompozycje smakowe, porcje, alergie lub sugestie dla szczególnych potrzeb gości.</p>",
        unsafe_allow_html=True,
    )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.72rem; color:#6A7D96; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.5rem;">Sugerowane pytania</p>',
        unsafe_allow_html=True,
    )

    qcols = st.columns(3)
    quick_prompts = [
        "Co pasuje do kaczki?",
        "Ile porcji na 100 gości?",
        "Opcje dla wegan?",
    ]
    for i, qp in enumerate(quick_prompts):
        with qcols[i]:
            if st.button(qp, key=f"qp_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": qp})
                reply = ai_chat(qp)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if user_input := st.chat_input("Napisz pytanie..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner(""):
            reply = ai_chat(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Wyczyść rozmowę"):
            st.session_state.chat_history = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 – PODSUMOWANIE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="section-label">Podsumowanie zamówienia</p>', unsafe_allow_html=True)

    summary = calculate_summary(
        st.session_state.selections,
        st.session_state.guest_count,
        MENU_DATA,
        UPSELLS,
    )

    # Metryki
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        (str(st.session_state.guest_count), "Gości"),
        (str(summary["total_dishes"]), "Wybrane dania"),
        (str(sum([
            st.session_state.dietary_notes.get("vegetarian", 0),
            st.session_state.dietary_notes.get("vegan", 0),
            st.session_state.dietary_notes.get("gluten_free", 0),
        ])), "Diety specjalne"),
        (str(len(st.session_state.selections.get("_upsells", []))), "Dodatki Premium"),
    ]
    for col, (val, label) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(
                f'<div class="summary-metric"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>',
                unsafe_allow_html=True,
            )

    # Koszt — większa czcionka
    if summary["estimated_cost"] > 0:
        st.markdown(
            f"""<div class="cost-box">
                <p class="cost-label">Szacunkowy koszt</p>
                <p class="cost-value">{summary['estimated_cost']:,} zł</p>
                <p class="cost-note">przy {st.session_state.guest_count} gościach — ceny orientacyjne, bez napojów</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Rozpisane dania
    if any(dishes for dishes in summary["breakdown"].values()):
        st.markdown('<p class="section-label">Wybrane dania</p>', unsafe_allow_html=True)
        for cat, dishes in summary["breakdown"].items():
            if dishes:
                st.markdown(
                    f"<p style='font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; color:#6A7D96; margin-bottom:0.25rem;'>{cat}</p>",
                    unsafe_allow_html=True,
                )
                for d in dishes:
                    dish_obj = next(
                        (di for di in MENU_DATA.get(cat, {}).get("dishes", []) if di["name"] == d), None
                    )
                    price_info = f" — {dish_obj['price_per_person']} zł/os." if dish_obj and dish_obj.get("price_per_person") else ""
                    st.markdown(
                        f"<p style='font-size:0.9rem; color:#1B2A4A; margin:0.15rem 0; padding-left:1rem;'>{d}{price_info}</p>",
                        unsafe_allow_html=True,
                    )
                st.markdown("<br>", unsafe_allow_html=True)

    # Diety
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Diety specjalne</p>', unsafe_allow_html=True)
    diet_df = pd.DataFrame([
        {"Dieta": "Wegetariańska", "Liczba gości": st.session_state.dietary_notes.get("vegetarian", 0)},
        {"Dieta": "Wegańska",      "Liczba gości": st.session_state.dietary_notes.get("vegan", 0)},
        {"Dieta": "Bezglutenowa",  "Liczba gości": st.session_state.dietary_notes.get("gluten_free", 0)},
    ])
    st.dataframe(diet_df, use_container_width=True, hide_index=True)

    if st.session_state.dietary_notes.get("other"):
        st.markdown(
            f"<p style='font-size:0.82rem; color:#3D4F6A; font-style:italic;'>Uwagi: {st.session_state.dietary_notes['other']}</p>",
            unsafe_allow_html=True,
        )

    # Premium
    upsells_chosen = st.session_state.selections.get("_upsells", [])
    if upsells_chosen:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Dodatki Premium</p>', unsafe_allow_html=True)
        for u in upsells_chosen:
            upsell_obj = next((x for x in UPSELLS if x["name"] == u), None)
            price_info = f" — od {upsell_obj['price']} zł" if upsell_obj and upsell_obj.get("price") else ""
            st.markdown(
                f"<p style='font-size:0.9rem; color:#1B2A4A;'>{u}{price_info}</p>",
                unsafe_allow_html=True,
            )

    # Eksport
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Eksport</p>', unsafe_allow_html=True)
    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        csv_data = export_to_csv(
            st.session_state.selections,
            st.session_state.dietary_notes,
            st.session_state.guest_count,
            st.session_state.couple_name,
            MENU_DATA,
            UPSELLS,
        )
        st.download_button(
            label="Pobierz CSV",
            data=csv_data,
            file_name=f"menu_{st.session_state.couple_name or 'wesele'}_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    with col_exp2:
        json_export = json.dumps(
            {
                "para": st.session_state.couple_name,
                "goscie": st.session_state.guest_count,
                "wybory": st.session_state.selections,
                "diety": st.session_state.dietary_notes,
                "data_eksportu": datetime.now().isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        )
        st.download_button(
            label="Pobierz JSON",
            data=json_export,
            file_name=f"menu_{st.session_state.couple_name or 'wesele'}_{datetime.today().strftime('%Y%m%d')}.json",
            mime="application/json",
        )
