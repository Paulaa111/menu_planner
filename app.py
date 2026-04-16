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
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        font-weight: 300;
    }
    h1, h2, h3, .serif {
        font-family: 'DM Serif Display', serif !important;
        font-weight: 400 !important;
    }
    .stApp {
        background: #F7F5F2;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1C1917 !important;
    }
    [data-testid="stSidebar"] * {
        color: #E8E0D5 !important;
    }
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stTextArea textarea {
        background: #2C2824 !important;
        border: 1px solid #3D3730 !important;
        color: #E8E0D5 !important;
        border-radius: 4px !important;
    }
    [data-testid="stSidebar"] label {
        color: #9C9087 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #2C2824 !important;
    }

    /* Category cards */
    .cat-card {
        background: #FFFFFF;
        border-radius: 2px;
        padding: 2rem 2rem 1.5rem;
        margin-bottom: 1.5rem;
        border-top: 2px solid #1C1917;
    }
    .cat-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #1C1917;
        margin: 0 0 0.25rem 0;
        letter-spacing: -0.01em;
    }
    .cat-desc {
        font-size: 0.8rem;
        color: #9C9087;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1.25rem;
    }

    /* Dish cards */
    .dish-detail {
        border-left: 2px solid #E8E0D5;
        padding: 0.5rem 0.75rem;
        margin: 0.5rem 0;
    }
    .dish-name {
        font-weight: 500;
        font-size: 0.9rem;
        color: #1C1917;
    }
    .dish-desc {
        font-size: 0.78rem;
        color: #9C9087;
        margin-top: 2px;
    }
    .dish-price {
        font-size: 0.78rem;
        color: #6B6059;
        font-weight: 500;
        margin-top: 3px;
    }
    .allergen-tag {
        display: inline-block;
        background: #F7F5F2;
        border: 1px solid #E8E0D5;
        border-radius: 2px;
        padding: 1px 6px;
        font-size: 0.68rem;
        color: #9C9087;
        margin-right: 3px;
        margin-top: 3px;
    }

    /* AI bubble */
    .ai-bubble {
        background: #FEFCFA;
        border: 1px solid #E8E0D5;
        border-left: 3px solid #1C1917;
        border-radius: 2px;
        padding: 0.75rem 1rem;
        margin: 0.75rem 0;
        font-size: 0.85rem;
        color: #4A4039;
        font-style: italic;
        line-height: 1.6;
    }

    /* Upsell cards */
    .upsell-card {
        background: #FFFFFF;
        border-radius: 2px;
        padding: 1rem;
        border-top: 2px solid #C9B99A;
        margin-bottom: 0.5rem;
    }
    .upsell-name {
        font-weight: 500;
        font-size: 0.9rem;
        color: #1C1917;
    }
    .upsell-price {
        font-size: 0.8rem;
        color: #6B6059;
        margin-top: 4px;
    }

    /* Summary */
    .summary-metric {
        background: #FFFFFF;
        border-radius: 2px;
        padding: 1.25rem;
        border-top: 2px solid #1C1917;
        text-align: center;
    }
    .metric-value {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: #1C1917;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #9C9087;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.5rem;
    }

    /* Cost highlight */
    .cost-box {
        background: #1C1917;
        color: #F7F5F2;
        border-radius: 2px;
        padding: 1.5rem 2rem;
        margin: 1rem 0;
    }
    .cost-label {
        font-size: 0.72rem;
        color: #9C9087;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .cost-value {
        font-family: 'DM Serif Display', serif;
        font-size: 2.5rem;
        color: #F7F5F2;
        line-height: 1.1;
        margin-top: 0.25rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1px solid #E8E0D5;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #9C9087 !important;
        padding: 0.75rem 1.5rem !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #1C1917 !important;
        border-bottom: 2px solid #1C1917 !important;
    }

    /* Buttons */
    .stButton>button {
        background: #1C1917 !important;
        color: #F7F5F2 !important;
        border: none !important;
        border-radius: 2px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        font-weight: 400 !important;
        padding: 0.5rem 1.5rem !important;
        transition: opacity 0.15s !important;
    }
    .stButton>button:hover {
        opacity: 0.8 !important;
        transform: none !important;
    }

    /* Multiselect tags */
    [data-baseweb="tag"] {
        background: #1C1917 !important;
        border-radius: 2px !important;
    }
    [data-baseweb="tag"] span {
        color: #F7F5F2 !important;
        font-size: 0.78rem !important;
    }

    /* Chat */
    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border-radius: 2px !important;
        border: none !important;
    }

    /* Download buttons */
    .stDownloadButton>button {
        background: transparent !important;
        color: #1C1917 !important;
        border: 1px solid #1C1917 !important;
        font-size: 0.72rem !important;
    }
    .stDownloadButton>button:hover {
        background: #1C1917 !important;
        color: #F7F5F2 !important;
    }

    /* Divider */
    hr {
        border-color: #E8E0D5 !important;
        margin: 1.5rem 0 !important;
    }

    /* Section label */
    .section-label {
        font-size: 0.68rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #9C9087;
        margin-bottom: 1.25rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E8E0D5;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "selections": {},
    "guest_count": 100,
    "chat_history": [],
    "couple_name": "",
    "dietary_notes": {},
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


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-family:DM Serif Display,serif; font-size:1.4rem; color:#E8E0D5; margin:0;'>Konfiguracja</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<p style='font-size:0.7rem; color:#6B6059; letter-spacing:0.1em; text-transform:uppercase; margin-top:2px;'>Dane podstawowe</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2C2824; margin:0.75rem 0;'>", unsafe_allow_html=True)

    st.session_state.couple_name = st.text_input("Para Młoda", placeholder="Anna & Michał")
    wedding_date = st.date_input("Data uroczystości", min_value=datetime.today())
    st.session_state.guest_count = st.number_input("Liczba gości", min_value=10, max_value=1000, value=100, step=5)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.7rem; color:#6B6059; letter-spacing:0.1em; text-transform:uppercase;'>Diety specjalne</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2C2824; margin:0.5rem 0;'>", unsafe_allow_html=True)

    vege = st.number_input("Wegetarianie", min_value=0, max_value=st.session_state.guest_count, value=0)
    vegan = st.number_input("Weganie", min_value=0, max_value=st.session_state.guest_count, value=0)
    gluten_free = st.number_input("Bezglutenowi", min_value=0, max_value=st.session_state.guest_count, value=0)
    allergy_notes = st.text_area("Pozostałe uwagi", placeholder="alergie, preferencje...")

    st.session_state.dietary_notes = {
        "vegetarian": vege,
        "vegan": vegan,
        "gluten_free": gluten_free,
        "other": allergy_notes,
    }

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2C2824; margin:0.5rem 0;'>", unsafe_allow_html=True)
    total_selected = sum(len(v) for v in st.session_state.selections.values() if isinstance(v, list))
    st.markdown(f"<p style='font-size:0.72rem; color:#6B6059;'>Wybrano dań: <strong style='color:#E8E0D5;'>{total_selected}</strong></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.72rem; color:#6B6059;'>Liczba gości: <strong style='color:#E8E0D5;'>{st.session_state.guest_count}</strong></p>", unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────────────
couple = st.session_state.couple_name or ""
st.markdown("<br>", unsafe_allow_html=True)

col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    if couple:
        st.markdown(f"<p style='font-size:0.72rem; color:#9C9087; letter-spacing:0.12em; text-transform:uppercase; margin:0;'>Konfiguracja menu</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-family:DM Serif Display,serif; font-size:2.8rem; color:#1C1917; margin:0; line-height:1.1;'>{couple}</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='font-size:0.72rem; color:#9C9087; letter-spacing:0.12em; text-transform:uppercase; margin:0;'>Konfigurator</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-family:DM Serif Display,serif; font-size:2.8rem; color:#1C1917; margin:0; line-height:1.1;'>Menu Weselne</h1>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["Menu", "Asystent Smaku", "Podsumowanie"])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 – MENU
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    for category, items in MENU_DATA.items():
        st.markdown(f'<div class="cat-card">', unsafe_allow_html=True)
        st.markdown(f'<p class="cat-title">{category}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="cat-desc">{items.get("description", "")}</p>', unsafe_allow_html=True)

        prev = st.session_state.selections.get(category, [])
        chosen = st.multiselect(
            f"Wybierz — {category}",
            options=[d["name"] for d in items["dishes"]],
            default=prev,
            key=f"select_{category}",
            label_visibility="collapsed",
        )
        st.session_state.selections[category] = chosen

        if chosen and chosen != prev:
            with st.spinner(""):
                tip = get_ai_suggestion(
                    f"Para wybrała do kategorii '{category}': {', '.join(chosen)}. "
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
                        total = price * st.session_state.guest_count if price else None
                        st.markdown(
                            f"""<div class="dish-detail">
                                <p class="dish-name">{dish['name']}</p>
                                <p class="dish-desc">{dish.get('description','')}</p>
                                {"<p class='dish-price'>~" + str(price) + " zł / os. &nbsp;·&nbsp; " + str(total) + " zł łącznie</p>" if price else ""}
                                <div style="margin-top:4px;">{allergen_html}</div>
                            </div>""",
                            unsafe_allow_html=True,
                        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Dodatki Premium ────────────────────────────────────────────────────────
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
                    <p class="dish-desc">{upsell['description']}</p>
                    {"<p class='upsell-price'>od " + str(upsell['price']) + " zł</p>" if upsell.get('price') else ""}
                </div>""",
                unsafe_allow_html=True,
            )
            if checked:
                new_upsells.append(upsell["name"])

    st.session_state.selections["_upsells"] = new_upsells


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 – ASYSTENT
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="section-label">Asystent Smaku</p>', unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem; color:#6B6059; margin-bottom:1.5rem;'>Zapytaj o kompozycje smakowe, porcje, alergie lub sugestie dla szczególnych potrzeb gości.</p>",
        unsafe_allow_html=True,
    )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.72rem; color:#9C9087; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.5rem;">Sugerowane pytania</p>', unsafe_allow_html=True)

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

    # Metrics
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

    # Estimated cost
    if summary["estimated_cost"] > 0:
        st.markdown(
            f"""<div class="cost-box">
                <p class="cost-label">Szacunkowy koszt</p>
                <p class="cost-value">{summary['estimated_cost']:,} zł</p>
                <p style="font-size:0.72rem; color:#6B6059; margin-top:0.5rem;">przy {st.session_state.guest_count} gościach — ceny orientacyjne, bez napojów</p>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Breakdown
    if any(dishes for dishes in summary["breakdown"].values()):
        st.markdown('<p class="section-label">Wybrane dania</p>', unsafe_allow_html=True)
        for cat, dishes in summary["breakdown"].items():
            if dishes:
                st.markdown(f"<p style='font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; color:#9C9087; margin-bottom:0.25rem;'>{cat}</p>", unsafe_allow_html=True)
                for d in dishes:
                    dish_obj = next((di for di in MENU_DATA.get(cat, {}).get("dishes", []) if di["name"] == d), None)
                    price_info = f" — {dish_obj['price_per_person']} zł/os." if dish_obj and dish_obj.get("price_per_person") else ""
                    st.markdown(f"<p style='font-size:0.85rem; color:#1C1917; margin:0.1rem 0; padding-left:1rem;'>{d}{price_info}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

    # Dietary
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Diety specjalne</p>', unsafe_allow_html=True)
    diet_df = pd.DataFrame([
        {"Dieta": "Wegetariańska", "Liczba gości": st.session_state.dietary_notes.get("vegetarian", 0)},
        {"Dieta": "Wegańska",      "Liczba gości": st.session_state.dietary_notes.get("vegan", 0)},
        {"Dieta": "Bezglutenowa",  "Liczba gości": st.session_state.dietary_notes.get("gluten_free", 0)},
    ])
    st.dataframe(diet_df, use_container_width=True, hide_index=True)

    if st.session_state.dietary_notes.get("other"):
        st.markdown(f"<p style='font-size:0.82rem; color:#6B6059; font-style:italic;'>Uwagi: {st.session_state.dietary_notes['other']}</p>", unsafe_allow_html=True)

    # Premium
    upsells_chosen = st.session_state.selections.get("_upsells", [])
    if upsells_chosen:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Dodatki Premium</p>', unsafe_allow_html=True)
        for u in upsells_chosen:
            upsell_obj = next((x for x in UPSELLS if x["name"] == u), None)
            price_info = f" — od {upsell_obj['price']} zł" if upsell_obj and upsell_obj.get("price") else ""
            st.markdown(f"<p style='font-size:0.85rem; color:#1C1917;'>{u}{price_info}</p>", unsafe_allow_html=True)

    # Export
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
