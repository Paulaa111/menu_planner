import streamlit as st
import pandas as pd
import json
from datetime import datetime
from anthropic import Anthropic
from menu_data import MENU_DATA, UPSELLS, DIET_OPTIONS
from utils import calculate_summary, export_to_csv

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Konfigurator Menu Weselnego",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Jost:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Jost', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
    }
    .stApp {
        background: linear-gradient(135deg, #fdf8f4 0%, #fef3ec 100%);
    }
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(180,120,80,0.08);
        border-left: 4px solid #c9956a;
    }
    .ai-bubble {
        background: linear-gradient(135deg, #fff7f0, #ffeedd);
        border: 1px solid #f0cba8;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        font-style: italic;
        color: #7a4a2a;
    }
    .summary-box {
        background: linear-gradient(135deg, #3d2b1f, #5c3d26);
        color: white;
        border-radius: 16px;
        padding: 1.5rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #c9956a, #a0714a) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Jost', sans-serif !important;
        font-weight: 500 !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #a0714a, #7a5535) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(160,113,74,0.3) !important;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "selections" not in st.session_state:
    st.session_state.selections = {}
if "guest_count" not in st.session_state:
    st.session_state.guest_count = 100
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "couple_name" not in st.session_state:
    st.session_state.couple_name = ""
if "dietary_notes" not in st.session_state:
    st.session_state.dietary_notes = {}
if "ai_tip" not in st.session_state:
    st.session_state.ai_tip = None

client = Anthropic()

# ── AI helper ─────────────────────────────────────────────────────────────────
def get_ai_suggestion(context: str) -> str:
    """Get a short AI pairing/upsell suggestion."""
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            system=(
                "Jesteś eleganckim asystentem kulinarnym polskiej restauracji weselnej. "
                "Odpowiadaj krótko (2-3 zdania), ciepło i po polsku. "
                "Doradzaj pasujące dodatki i kompozycje smakowe."
            ),
            messages=[{"role": "user", "content": context}],
        )
        return resp.content[0].text
    except Exception:
        return None


def ai_chat(user_msg: str) -> str:
    """Full AI assistant chat."""
    history = st.session_state.chat_history[-10:]  # last 10 messages
    messages = history + [{"role": "user", "content": user_msg}]
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=(
                "Jesteś Asystentem Smaku w ekskluzywnej polskiej restauracji weselnej. "
                "Pomagasz parze młodej skonfigurować idealne menu weselne. "
                "Znasz całą ofertę: dania główne (kaczka, polędwica, łosoś, kurczak), "
                "dodatki (kopytka, pierogi, kluski śląskie, ziemniaki, warzywa), "
                "zupy (żurek, rosół, barszcz, krem z dyni), "
                "przekąski (wiejski stół, deska serów, śledzie), "
                "desery (fontanna czekoladowa, tort weselny, lody). "
                "Odpowiadaj po polsku, ciepło i profesjonalnie. Sugeruj harmonijne kompozycje."
            ),
            messages=messages,
        )
        return resp.content[0].text
    except Exception as e:
        return f"Przepraszam, wystąpił chwilowy problem z asystentem. Spróbuj ponownie za chwilę."


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌸 Informacje")
    st.session_state.couple_name = st.text_input("Para Młoda", placeholder="Anna & Michał")
    wedding_date = st.date_input("Data ślubu", min_value=datetime.today())
    st.session_state.guest_count = st.number_input("Liczba gości", min_value=10, max_value=1000, value=100, step=5)

    st.markdown("---")
    st.markdown("### 🥗 Diety specjalne")
    vege = st.number_input("Wegetarianie", min_value=0, max_value=st.session_state.guest_count, value=0)
    vegan = st.number_input("Weganie", min_value=0, max_value=st.session_state.guest_count, value=0)
    gluten_free = st.number_input("Bezglutenowi", min_value=0, max_value=st.session_state.guest_count, value=0)
    allergy_notes = st.text_area("Inne alergie / uwagi", placeholder="np. alergia na orzechy, laktozę...")

    st.session_state.dietary_notes = {
        "vegetarian": vege,
        "vegan": vegan,
        "gluten_free": gluten_free,
        "other": allergy_notes,
    }

    st.markdown("---")
    # Quick summary
    total_selected = sum(len(v) for v in st.session_state.selections.values())
    st.markdown(f"**Wybrano kategorii:** {total_selected}")
    st.markdown(f"**Gości:** {st.session_state.guest_count}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
couple = st.session_state.couple_name or "Droga Paro Młoda"
st.markdown(f"# 🌸 Konfigurator Menu Weselnego")
st.markdown(f"### Witaj, *{couple}*! Zbudujmy razem Wasze wymarzone menu.")
st.markdown("---")

tabs = st.tabs(["🍽️ Menu", "🤖 Asystent Smaku", "📊 Podsumowanie"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 – MENU SELECTOR
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    for category, items in MENU_DATA.items():
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        icon = items.get("icon", "🍴")
        st.markdown(f"### {icon} {category}")
        st.caption(items.get("description", ""))

        # Multiselect for dishes
        prev = st.session_state.selections.get(category, [])
        chosen = st.multiselect(
            f"Wybierz dania – {category}",
            options=[d["name"] for d in items["dishes"]],
            default=prev,
            key=f"select_{category}",
            label_visibility="collapsed",
        )
        st.session_state.selections[category] = chosen

        # AI pairing tip when selection changes
        if chosen and chosen != prev:
            with st.spinner("Asystent Smaku myśli..."):
                tip = get_ai_suggestion(
                    f"Para wybrała do kategorii '{category}': {', '.join(chosen)}. "
                    "Zaproponuj krótko pasujące danie lub dodatek z naszej oferty."
                )
            if tip:
                st.markdown(f'<div class="ai-bubble">💬 {tip}</div>', unsafe_allow_html=True)

        # Show dish details
        if chosen:
            detail_cols = st.columns(min(len(chosen), 3))
            for idx, dish_name in enumerate(chosen):
                dish = next((d for d in items["dishes"] if d["name"] == dish_name), None)
                if dish:
                    with detail_cols[idx % 3]:
                        st.markdown(f"**{dish['name']}**")
                        st.caption(dish.get("description", ""))
                        if dish.get("allergens"):
                            st.caption(f"⚠️ Alergeny: {', '.join(dish['allergens'])}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Upsells ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### ✨ Dodatki Premium")
    st.caption("Wzbogać swoje wesele o wyjątkowe atrakcje kulinarne")

    upsell_cols = st.columns(3)
    selected_upsells = st.session_state.selections.get("_upsells", [])
    new_upsells = []
    for i, upsell in enumerate(UPSELLS):
        with upsell_cols[i % 3]:
            checked = st.checkbox(
                f"{upsell['icon']} **{upsell['name']}**",
                value=upsell["name"] in selected_upsells,
                key=f"upsell_{upsell['name']}",
                help=upsell["description"],
            )
            st.caption(upsell["description"])
            if upsell.get("price"):
                st.caption(f"💰 od {upsell['price']} zł")
            if checked:
                new_upsells.append(upsell["name"])
    st.session_state.selections["_upsells"] = new_upsells


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 – AI ASSISTANT CHAT
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("### 🤖 Asystent Smaku")
    st.caption("Zapytaj o kompozycje smakowe, alergie, porcje – jestem tu, by pomóc!")

    # Display chat history
    for msg in st.session_state.chat_history:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])

    # Quick prompts
    st.markdown("**Szybkie pytania:**")
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

    # Chat input
    if user_input := st.chat_input("Napisz pytanie do Asystenta Smaku..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Asystent przygotowuje odpowiedź..."):
            reply = ai_chat(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("🗑️ Wyczyść rozmowę"):
        st.session_state.chat_history = []
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 – SUMMARY & EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("### 📊 Podsumowanie zamówienia")

    summary = calculate_summary(
        st.session_state.selections,
        st.session_state.guest_count,
        MENU_DATA,
        UPSELLS,
    )

    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("👥 Goście", st.session_state.guest_count)
    with m2:
        st.metric("🍽️ Wybrane dania", summary["total_dishes"])
    with m3:
        st.metric("🥗 Diety specjalne", sum([
            st.session_state.dietary_notes.get("vegetarian", 0),
            st.session_state.dietary_notes.get("vegan", 0),
            st.session_state.dietary_notes.get("gluten_free", 0),
        ]))
    with m4:
        st.metric("✨ Dodatki Premium", len(st.session_state.selections.get("_upsells", [])))

    st.markdown("---")

    # Per-category breakdown
    if summary["breakdown"]:
        st.markdown("#### Wybrane dania według kategorii")
        for cat, dishes in summary["breakdown"].items():
            if dishes:
                st.markdown(f"**{cat}**")
                for d in dishes:
                    st.markdown(f"  - {d} × {st.session_state.guest_count} porcji")

    # Dietary summary
    st.markdown("---")
    st.markdown("#### 🥗 Zestawienie dietetyczne")
    diet_df = pd.DataFrame([
        {"Dieta": "Wegetariańska", "Liczba gości": st.session_state.dietary_notes.get("vegetarian", 0)},
        {"Dieta": "Wegańska", "Liczba gości": st.session_state.dietary_notes.get("vegan", 0)},
        {"Dieta": "Bezglutenowa", "Liczba gości": st.session_state.dietary_notes.get("gluten_free", 0)},
        {"Dieta": "Inne wymagania", "Liczba gości": "patrz uwagi"},
    ])
    st.dataframe(diet_df, use_container_width=True, hide_index=True)

    if st.session_state.dietary_notes.get("other"):
        st.info(f"📝 Uwagi: {st.session_state.dietary_notes['other']}")

    # Upsells chosen
    upsells_chosen = st.session_state.selections.get("_upsells", [])
    if upsells_chosen:
        st.markdown("---")
        st.markdown("#### ✨ Zamówione dodatki Premium")
        for u in upsells_chosen:
            st.markdown(f"  - {u}")

    # Export
    st.markdown("---")
    st.markdown("#### 📥 Eksport")

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
            label="⬇️ Pobierz CSV (dla kuchni)",
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
            label="⬇️ Pobierz JSON (pełny)",
            data=json_export,
            file_name=f"menu_{st.session_state.couple_name or 'wesele'}_{datetime.today().strftime('%Y%m%d')}.json",
            mime="application/json",
        )
