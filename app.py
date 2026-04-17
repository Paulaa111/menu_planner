import streamlit as st
import pandas as pd
import json
from datetime import datetime
from openai import OpenAI
from menu_data import MENU_DATA, UPSELLS, DIET_OPTIONS
from utils import calculate_summary, export_to_csv

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Menu Weselne",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Grok client (klucz z .streamlit/secrets.toml) ────────────────────────────
grok_api_key = st.secrets.get("GROK_API_KEY", "")
grok_client  = OpenAI(api_key=grok_api_key, base_url="https://api.x.ai/v1") if grok_api_key else None

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');

html, body, [class*="css"] { font-family:'DM Sans',sans-serif; font-weight:300; color:#1B2A4A; }
h1,h2,h3 { font-family:'DM Serif Display',serif !important; font-weight:400 !important; color:#1B2A4A !important; }
.stApp { background:#FAF7F2; }
.block-container { padding-top:2rem !important; }

/* ─ Sidebar ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] { background:#1B2A4A !important; }

/* WSZYSTKIE teksty w sidebarze — wymuszamy jasny kolor na każdym elemencie */
[data-testid="stSidebar"] *:not(input):not(textarea):not(button) {
    color:#E8E4DC !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label { color:#E8E4DC !important; }

/* Małe etykiety (uppercase) */
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stTextInput  label,
[data-testid="stSidebar"] .stTextArea   label,
[data-testid="stSidebar"] .stDateInput  label { color:#A8B8CC !important; font-size:0.75rem !important; letter-spacing:0.08em !important; text-transform:uppercase !important; }

/* Pola formularza */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea { background:#243660 !important; border:1px solid #3A5080 !important; color:#E8E4DC !important; border-radius:10px !important; }
[data-testid="stSidebar"] input::placeholder,
[data-testid="stSidebar"] textarea::placeholder { color:#6A82A0 !important; }
[data-testid="stSidebar"] hr { border-color:#243660 !important; }

/* Przycisk expand (strzałka › gdy sidebar zwinięty) */
[data-testid="stSidebarCollapsedControl"] { background:#1B2A4A !important; border-radius:0 10px 10px 0 !important; }
[data-testid="stSidebarCollapsedControl"] svg { fill:#FAF7F2 !important; color:#FAF7F2 !important; }
[data-testid="stSidebarCollapseButton"] svg { fill:#A8B8CC !important; }

/* ─ Nagłówki grup posiłków ────────────────────────────────────────────────── */
.meal-group-header { background:#1B2A4A; border-radius:14px 14px 0 0; padding:1.1rem 2rem 1rem; margin-top:2.5rem; }
.meal-group-title  { font-family:'DM Serif Display',serif; font-size:1.6rem; color:#FAF7F2 !important; margin:0; line-height:1.2; }
.meal-group-subtitle { font-size:0.7rem; color:#A8B8CC !important; text-transform:uppercase; letter-spacing:0.1em; margin-top:3px; }

/* ─ Karty ─────────────────────────────────────────────────────────────────── */
.cat-card           { background:#FFFFFF; padding:1.5rem 2rem 1.25rem; border-left:3px solid #C4975A; border-bottom:1px solid #EDE8E0; }
.cat-card-last      { background:#FFFFFF; padding:1.5rem 2rem 1.25rem; border-left:3px solid #C4975A; border-radius:0 0 14px 14px; }
.cat-card-standalone{ background:#FFFFFF; border-radius:14px; padding:1.5rem 2rem 1.25rem; border-left:3px solid #C4975A; margin-top:2.5rem; box-shadow:0 2px 12px rgba(27,42,74,.06); }
.cat-title   { font-family:'DM Serif Display',serif; font-size:1.15rem; color:#1B2A4A !important; margin:0 0 .2rem; }
.cat-desc    { font-size:.75rem; color:#4A5E78 !important; letter-spacing:.05em; margin-bottom:.5rem; }
.select-hint { font-size:.68rem; color:#C4975A !important; text-transform:uppercase; letter-spacing:.1em; margin-bottom:.25rem; font-weight:500; }

/* ─ Kafelki dań ───────────────────────────────────────────────────────────── */
.dish-detail { border-left:3px solid #C4975A; background:#FAF7F2; border-radius:0 10px 10px 0; padding:.65rem .9rem; margin:.5rem 0; }
.dish-name   { font-weight:500; font-size:.9rem;  color:#1B2A4A !important; }
.dish-desc   { font-size:.78rem; color:#2D3E55 !important; margin-top:2px; }
.dish-price  { font-size:.8rem;  color:#C4975A !important; font-weight:500; margin-top:4px; }
.allergen-tag{ display:inline-block; background:#F0EBE3; border:1px solid #DDD5C8; border-radius:20px; padding:1px 8px; font-size:.68rem; color:#2D3E55 !important; margin-right:3px; margin-top:3px; }

/* ─ AI bubble ─────────────────────────────────────────────────────────────── */
.ai-bubble { background:#EEF1F7; border:1px solid #C8D4E8; border-left:3px solid #1B2A4A; border-radius:0 12px 12px 0; padding:.75rem 1rem; margin:.75rem 0; font-size:.85rem; color:#1B2A4A !important; font-style:italic; line-height:1.6; }

/* ─ Upsell ────────────────────────────────────────────────────────────────── */
.upsell-card  { background:#FFFFFF; border-radius:12px; padding:1rem; border-top:2px solid #C4975A; margin-bottom:.5rem; box-shadow:0 2px 8px rgba(27,42,74,.05); }
.upsell-name  { font-weight:500; font-size:.9rem;  color:#1B2A4A !important; }
.upsell-price { font-size:.8rem; color:#C4975A !important; margin-top:4px; font-weight:500; }
.upsell-desc  { font-size:.78rem; color:#2D3E55 !important; margin-top:3px; }

/* ─ Metryki ───────────────────────────────────────────────────────────────── */
.summary-metric { background:#FFFFFF; border-radius:14px; padding:1.25rem; border-top:3px solid #1B2A4A; text-align:center; box-shadow:0 2px 8px rgba(27,42,74,.06); }
.metric-value   { font-family:'DM Serif Display',serif; font-size:2rem; color:#1B2A4A !important; line-height:1; }
.metric-label   { font-size:.72rem; color:#4A5E78 !important; text-transform:uppercase; letter-spacing:.08em; margin-top:.5rem; }

/* ─ Koszt ─────────────────────────────────────────────────────────────────── */
.cost-box   { background:#1B2A4A; border-radius:14px; padding:1.75rem 2rem; margin:1.25rem 0; }
.cost-label { font-size:.72rem; color:#A8B8CC !important; text-transform:uppercase; letter-spacing:.1em; }
.cost-value { font-family:'DM Serif Display',serif; font-size:3.8rem; color:#FAF7F2 !important; line-height:1.1; margin-top:.25rem; }
.cost-note  { font-size:.78rem; color:#A8B8CC !important; margin-top:.5rem; }

/* ─ Taby ──────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] { background:transparent; border-bottom:1px solid #DDD5C8; gap:0; }
.stTabs [data-baseweb="tab"]      { font-family:'DM Sans',sans-serif !important; font-size:.75rem !important; letter-spacing:.08em !important; text-transform:uppercase !important; color:#4A5E78 !important; padding:.75rem 1.5rem !important; background:transparent !important; }
.stTabs [aria-selected="true"]    { color:#1B2A4A !important; border-bottom:2px solid #C4975A !important; }

/* ─ Przyciski ─────────────────────────────────────────────────────────────── */
.stButton>button { background:#1B2A4A !important; color:#FAF7F2 !important; border:none !important; border-radius:12px !important; font-family:'DM Sans',sans-serif !important; font-size:.8rem !important; letter-spacing:.08em !important; text-transform:uppercase !important; font-weight:500 !important; padding:.55rem 1.5rem !important; }
.stButton>button:hover { opacity:.85 !important; }
.stButton>button, .stButton>button *, .stButton>button p, .stButton>button span { color:#FAF7F2 !important; }

/* ─ Multiselect ───────────────────────────────────────────────────────────── */
[data-baseweb="tag"]      { background:#1B2A4A !important; border-radius:20px !important; }
[data-baseweb="tag"] span { color:#FAF7F2 !important; font-size:.78rem !important; }
[data-baseweb="select"]   { border-radius:10px !important; }

/* ─ Chat ──────────────────────────────────────────────────────────────────── */
[data-testid="stChatMessage"] { background:#FFFFFF !important; border-radius:12px !important; border:none !important; }

/* ─ Download ──────────────────────────────────────────────────────────────── */
.stDownloadButton>button { background:transparent !important; color:#1B2A4A !important; border:1.5px solid #1B2A4A !important; font-size:.72rem !important; border-radius:12px !important; }
.stDownloadButton>button:hover { background:#1B2A4A !important; color:#FAF7F2 !important; }

/* ─ Inne ──────────────────────────────────────────────────────────────────── */
hr { border-color:#DDD5C8 !important; margin:1.5rem 0 !important; }
.section-label { font-size:.68rem; letter-spacing:.12em; text-transform:uppercase; color:#4A5E78 !important; margin-bottom:1.25rem; padding-bottom:.5rem; border-bottom:1px solid #DDD5C8; }
.wedding-intro { background:#FFFFFF; border-radius:14px; padding:1.75rem 2rem; margin-bottom:2rem; border-left:4px solid #C4975A; box-shadow:0 2px 10px rgba(27,42,74,.05); }
.intro-title   { font-family:'DM Serif Display',serif; font-size:1.2rem; color:#1B2A4A !important; display:block; margin-bottom:.5rem; }
.intro-body    { color:#1B2A4A !important; font-size:.88rem; line-height:1.75; }
.tagline       { font-family:'DM Serif Display',serif; font-style:italic; font-size:1.05rem; color:#C4975A !important; margin-top:.4rem; }
.stCheckbox label, .stCheckbox span { color:#1B2A4A !important; font-size:.88rem !important; }
[data-testid="stDataFrame"] { border-radius:10px !important; overflow:hidden; }
#MainMenu{visibility:hidden;} footer{visibility:hidden;} header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "selections": {}, "guest_count": 100, "chat_history": [],
    "couple_name": "", "dietary_notes": {}, "show_summary_preview": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── AI helpers ────────────────────────────────────────────────────────────────
SYSTEM_CULINARY = (
    "Jesteś eleganckim asystentem kulinarnym polskiej restauracji weselnej. "
    "Odpowiadaj krótko (2 zdania), ciepło i po polsku, bez emoji. "
    "Doradzaj pasujące dodatki i kompozycje smakowe."
)
SYSTEM_CHAT = (
    "Jesteś Asystentem Smaku w ekskluzywnej polskiej restauracji weselnej. "
    "Pomagasz parze młodej skonfigurować idealne menu weselne. "
    "Odpowiadaj po polsku, bez emoji, ciepło i profesjonalnie. "
    "Sugeruj harmonijne kompozycje smakowe."
)


def grok_complete(system: str, messages: list, max_tokens: int = 300):
    if not grok_client:
        return None
    try:
        resp = grok_client.chat.completions.create(
            model="grok-3-latest",
            max_tokens=max_tokens,
            messages=[{"role": "system", "content": system}] + messages,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Błąd Grok: {e}"


def get_ai_suggestion(context: str):
    return grok_complete(SYSTEM_CULINARY, [{"role": "user", "content": context}], max_tokens=180)


def ai_chat(user_msg: str) -> str:
    history  = st.session_state.chat_history[-10:]
    messages = history + [{"role": "user", "content": user_msg}]
    return grok_complete(SYSTEM_CHAT, messages, max_tokens=500) or "Przepraszam, wystąpił chwilowy problem."


# ── Grupy posiłków ────────────────────────────────────────────────────────────
MEAL_GROUPS = {
    "Przystawki":                 ["Przystawki"],
    "Obiad I":                    ["Obiad I – Zupa","Obiad I – Danie Główne","Obiad I – Dodatek","Obiad I – Sałatka"],
    "Obiad II":                   ["Obiad II – Danie Główne","Obiad II – Dodatek","Obiad II – Sałatka"],
    "Kolacja":                    ["Kolacja – Danie Główne","Kolacja – Dodatek","Kolacja – Sałatka"],
    "Barszcze & Przekąski Nocne": ["Barszcze & Przekąski Nocne"],
    "Zimna Płyta":                ["Zimna Płyta"],
    "Desery":                     ["Desery"],
}

def sub_label(cat): return cat.split(" – ")[-1] if " – " in cat else cat


def render_dish_cards(chosen, items):
    if not chosen: return
    cols = st.columns(min(len(chosen), 3))
    for idx, dish_name in enumerate(chosen):
        dish = next((d for d in items["dishes"] if d["name"] == dish_name), None)
        if dish:
            with cols[idx % 3]:
                allergen_html = "".join(f'<span class="allergen-tag">{a}</span>' for a in dish.get("allergens",[]))
                price   = dish.get("price_per_person")
                total_p = price * st.session_state.guest_count if price else None
                st.markdown(
                    f'<div class="dish-detail">'
                    f'<p class="dish-name">{dish["name"]}</p>'
                    f'<p class="dish-desc">{dish.get("description","")}</p>'
                    f'{"<p class=\'dish-price\'>~"+str(price)+" zł / os. &nbsp;·&nbsp; "+str(total_p)+" zł łącznie</p>" if price else ""}'
                    f'<div style="margin-top:4px;">{allergen_html}</div>'
                    f'</div>', unsafe_allow_html=True)


def render_select(cat, items):
    prev   = st.session_state.selections.get(cat, [])
    st.markdown('<p class="select-hint">▸ Wybierz dania z listy poniżej</p>', unsafe_allow_html=True)
    chosen = st.multiselect(
        label=cat, options=[d["name"] for d in items["dishes"]],
        default=prev, key=f"select_{cat}", label_visibility="collapsed",
        placeholder="Kliknij, aby wybrać dania...",
    )
    st.session_state.selections[cat] = chosen
    if chosen and chosen != prev:
        with st.spinner(""):
            tip = get_ai_suggestion(f"Para wybrała do kategorii '{cat}': {', '.join(chosen)}. Zaproponuj krótko pasujące danie lub dodatek.")
        if tip:
            st.markdown(f'<div class="ai-bubble">{tip}</div>', unsafe_allow_html=True)
    render_dish_cards(chosen, items)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:DM Serif Display,serif;font-size:1.4rem;color:#FAF7F2;margin:0;'>Konfiguracja</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:.7rem;color:#A8B8CC;letter-spacing:.1em;text-transform:uppercase;margin-top:2px;'>Dane podstawowe</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#243660;margin:.75rem 0;'>", unsafe_allow_html=True)

    st.session_state.couple_name = st.text_input("Para Młoda", placeholder="Anna & Michał")
    wedding_date = st.date_input("Data uroczystości", min_value=datetime.today())
    st.session_state.guest_count = st.number_input("Liczba gości", min_value=10, max_value=1000, value=100, step=5)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:.7rem;color:#A8B8CC;letter-spacing:.1em;text-transform:uppercase;'>Diety specjalne</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#243660;margin:.5rem 0;'>", unsafe_allow_html=True)

    vege        = st.number_input("Wegetarianie",  min_value=0, max_value=st.session_state.guest_count, value=0)
    vegan       = st.number_input("Weganie",        min_value=0, max_value=st.session_state.guest_count, value=0)
    gluten_free = st.number_input("Bezglutenowi",   min_value=0, max_value=st.session_state.guest_count, value=0)
    allergy_notes = st.text_area("Pozostałe uwagi", placeholder="alergie, preferencje...")

    st.session_state.dietary_notes = {"vegetarian": vege, "vegan": vegan, "gluten_free": gluten_free, "other": allergy_notes}

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#243660;margin:.5rem 0;'>", unsafe_allow_html=True)
    total_sel = sum(len(v) for v in st.session_state.selections.values() if isinstance(v, list))
    st.markdown(f"<p style='font-size:.72rem;color:#A8B8CC;'>Wybrano dań: <strong style='color:#FAF7F2;'>{total_sel}</strong></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:.72rem;color:#A8B8CC;'>Liczba gości: <strong style='color:#FAF7F2;'>{st.session_state.guest_count}</strong></p>", unsafe_allow_html=True)

    if not grok_api_key:
        st.markdown("<hr style='border-color:#243660;margin:.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:.72rem;color:#E8A87C;'>⚠ Brak GROK_API_KEY w secrets — Asystent niedostępny.</p>", unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────────────
couple = st.session_state.couple_name or ""
col_h1, _ = st.columns([2, 1])
with col_h1:
    label = "Konfiguracja menu" if couple else "Konfigurator weselny"
    title = couple or "Menu Weselne"
    st.markdown(f"<p style='font-size:.72rem;color:#4A5E78;letter-spacing:.12em;text-transform:uppercase;margin:0 0 4px;'>{label}</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family:DM Serif Display,serif;font-size:2.8rem;color:#1B2A4A;margin:0;line-height:1.1;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Uzupełnij menu swojego wymarzonego wesela — krok po kroku, danie po daniu.</p>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
tabs = st.tabs(["Menu", "Asystent Smaku", "Podsumowanie"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – MENU
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
    <div class="wedding-intro">
        <span class="intro-title">Skomponuj swoje wesele</span>
        <span class="intro-body">
            Tworzymy menu weselne z sercem — korzystamy z produktów lokalnych dostawców
            i sprawdzonych polskich przepisów przekazywanych z pokolenia na pokolenie.
            Wybierz dania z każdej kategorii, a nasz Asystent Smaku podpowie, co do siebie pasuje.
            Każde danie możemy dostosować do potrzeb dietetycznych Twoich gości.
        </span>
    </div>""", unsafe_allow_html=True)

    for group_name, group_cats in MEAL_GROUPS.items():
        if len(group_cats) == 1:
            cat   = group_cats[0]
            items = MENU_DATA.get(cat, {})
            if not items: continue
            st.markdown(f'<div class="cat-card-standalone"><p class="cat-title">{cat}</p><p class="cat-desc">{items.get("description","")}</p></div>', unsafe_allow_html=True)
            render_select(cat, items)
        else:
            st.markdown(f'<div class="meal-group-header"><p class="meal-group-title">{group_name}</p><p class="meal-group-subtitle">Uzupełnij każdą sekcję, aby skomponować pełny posiłek</p></div>', unsafe_allow_html=True)
            for ci, cat in enumerate(group_cats):
                items = MENU_DATA.get(cat, {})
                if not items: continue
                cls = "cat-card-last" if ci == len(group_cats)-1 else "cat-card"
                st.markdown(f'<div class="{cls}"><p class="cat-title">{sub_label(cat)}</p><p class="cat-desc">{items.get("description","")}</p></div>', unsafe_allow_html=True)
                render_select(cat, items)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Dodatki Premium</p>', unsafe_allow_html=True)

    up_cols = st.columns(3)
    sel_ups  = st.session_state.selections.get("_upsells", [])
    new_ups  = []
    for i, u in enumerate(UPSELLS):
        with up_cols[i % 3]:
            if st.checkbox(u["name"], value=u["name"] in sel_ups, key=f"upsell_{u['name']}"):
                new_ups.append(u["name"])
            st.markdown(
                f'<div class="upsell-card"><p class="upsell-name">{u["name"]}</p>'
                f'<p class="upsell-desc">{u["description"]}</p>'
                f'{"<p class=\'upsell-price\'>od "+str(u["price"])+" zł</p>" if u.get("price") else ""}'
                f'</div>', unsafe_allow_html=True)
    st.session_state.selections["_upsells"] = new_ups

    total_dishes_now = sum(len(v) for k,v in st.session_state.selections.items() if isinstance(v,list) and k!="_upsells")
    st.markdown("<hr>", unsafe_allow_html=True)

    if total_dishes_now > 0:
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            if st.button("Podsumuj wybrane menu", use_container_width=True):
                st.session_state.show_summary_preview = not st.session_state.show_summary_preview

        if st.session_state.show_summary_preview:
            s = calculate_summary(st.session_state.selections, st.session_state.guest_count, MENU_DATA, UPSELLS)
            rows_html = ""
            for cat, dishes in s["breakdown"].items():
                for d in dishes:
                    dobj = next((di for di in MENU_DATA.get(cat,{}).get("dishes",[]) if di["name"]==d), None)
                    pt   = f"{dobj['price_per_person']} zł/os." if dobj and dobj.get("price_per_person") else "—"
                    rows_html += (f"<div style='display:flex;justify-content:space-between;border-bottom:1px solid #2C3F66;"
                                  f"padding:.35rem 0;font-size:.84rem;color:#C8D4E8;'>"
                                  f"<span><span style='color:#7A9AB8;font-size:.72rem;'>{cat}</span>&nbsp;·&nbsp;{d}</span>"
                                  f"<span style='color:#C4975A;white-space:nowrap;margin-left:1rem;'>{pt}</span></div>")
            for un in st.session_state.selections.get("_upsells",[]):
                uo  = next((x for x in UPSELLS if x["name"]==un), None)
                pt  = f"od {uo['price']} zł" if uo and uo.get("price") else "—"
                rows_html += (f"<div style='display:flex;justify-content:space-between;border-bottom:1px solid #2C3F66;"
                              f"padding:.35rem 0;font-size:.84rem;color:#C8D4E8;'>"
                              f"<span><span style='color:#7A9AB8;font-size:.72rem;'>Dodatek</span>&nbsp;·&nbsp;{un}</span>"
                              f"<span style='color:#C4975A;white-space:nowrap;margin-left:1rem;'>{pt}</span></div>")
            cost_html = (f"<p style='font-family:DM Serif Display,serif;font-size:1.5rem;color:#C4975A;margin-top:.9rem;margin-bottom:0;'>"
                         f"Szacunkowy koszt: {s['estimated_cost']:,} zł</p>") if s["estimated_cost"] > 0 else ""
            st.markdown(
                f"<div style='background:#1B2A4A;border-radius:14px;padding:1.4rem 2rem;margin:1rem 0;'>"
                f"<p style='font-family:DM Serif Display,serif;font-size:1.25rem;color:#FAF7F2;margin:0 0 .75rem;'>Twoje wybory</p>"
                f"{rows_html}{cost_html}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center;color:#4A5E78;font-size:.82rem;padding:1rem 0;'>Wybierz przynajmniej jedno danie, aby zobaczyć podsumowanie.</p>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – ASYSTENT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="section-label">Asystent Smaku — Grok</p>', unsafe_allow_html=True)

    if not grok_client:
        st.warning("Asystent Smaku wymaga klucza API Grok. Dodaj `GROK_API_KEY` do pliku `.streamlit/secrets.toml`:")
        st.code('[secrets]\nGROK_API_KEY = "xai-..."', language="toml")
    else:
        st.markdown("<p style='font-size:.85rem;color:#2D3E55;margin-bottom:1.5rem;'>Zapytaj o kompozycje smakowe, porcje, alergie lub sugestie dla szczególnych potrzeb gości.</p>", unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        st.markdown('<p style="font-size:.72rem;color:#4A5E78;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.5rem;">Sugerowane pytania</p>', unsafe_allow_html=True)
        qcols = st.columns(3)
        for i, qp in enumerate(["Co pasuje do kaczki?", "Ile porcji na 100 gości?", "Opcje dla wegan?"]):
            with qcols[i]:
                if st.button(qp, key=f"qp_{i}"):
                    st.session_state.chat_history.append({"role":"user","content":qp})
                    st.session_state.chat_history.append({"role":"assistant","content":ai_chat(qp)})
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if user_input := st.chat_input("Napisz pytanie..."):
            st.session_state.chat_history.append({"role":"user","content":user_input})
            with st.spinner(""):
                st.session_state.chat_history.append({"role":"assistant","content":ai_chat(user_input)})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("Wyczyść rozmowę"):
                st.session_state.chat_history = []
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – PODSUMOWANIE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="section-label">Podsumowanie zamówienia</p>', unsafe_allow_html=True)
    summary = calculate_summary(st.session_state.selections, st.session_state.guest_count, MENU_DATA, UPSELLS)

    m1,m2,m3,m4 = st.columns(4)
    for col,(val,label) in zip([m1,m2,m3,m4],[
        (str(st.session_state.guest_count),"Gości"),
        (str(summary["total_dishes"]),"Wybrane dania"),
        (str(sum([st.session_state.dietary_notes.get(k,0) for k in ["vegetarian","vegan","gluten_free"]])),"Diety specjalne"),
        (str(len(st.session_state.selections.get("_upsells",[]))),"Dodatki Premium"),
    ]):
        with col:
            st.markdown(f'<div class="summary-metric"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    if summary["estimated_cost"] > 0:
        st.markdown(
            f'<div class="cost-box"><p class="cost-label">Szacunkowy koszt całkowity</p>'
            f'<p class="cost-value">{summary["estimated_cost"]:,} zł</p>'
            f'<p class="cost-note">przy {st.session_state.guest_count} gościach — ceny orientacyjne, bez napojów</p></div>',
            unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    if any(dishes for dishes in summary["breakdown"].values()):
        st.markdown('<p class="section-label">Wybrane dania</p>', unsafe_allow_html=True)
        for cat, dishes in summary["breakdown"].items():
            if dishes:
                st.markdown(f"<p style='font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:#4A5E78;margin-bottom:.25rem;'>{cat}</p>", unsafe_allow_html=True)
                for d in dishes:
                    dobj = next((di for di in MENU_DATA.get(cat,{}).get("dishes",[]) if di["name"]==d), None)
                    pi   = f" — {dobj['price_per_person']} zł/os." if dobj and dobj.get("price_per_person") else ""
                    st.markdown(f"<p style='font-size:.9rem;color:#1B2A4A;margin:.15rem 0;padding-left:1rem;'>{d}{pi}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Diety specjalne</p>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([
        {"Dieta":"Wegetariańska","Liczba gości":st.session_state.dietary_notes.get("vegetarian",0)},
        {"Dieta":"Wegańska",     "Liczba gości":st.session_state.dietary_notes.get("vegan",0)},
        {"Dieta":"Bezglutenowa", "Liczba gości":st.session_state.dietary_notes.get("gluten_free",0)},
    ]), use_container_width=True, hide_index=True)

    if st.session_state.dietary_notes.get("other"):
        st.markdown(f"<p style='font-size:.82rem;color:#2D3E55;font-style:italic;'>Uwagi: {st.session_state.dietary_notes['other']}</p>", unsafe_allow_html=True)

    ups_ch = st.session_state.selections.get("_upsells",[])
    if ups_ch:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Dodatki Premium</p>', unsafe_allow_html=True)
        for u in ups_ch:
            uo = next((x for x in UPSELLS if x["name"]==u), None)
            pi = f" — od {uo['price']} zł" if uo and uo.get("price") else ""
            st.markdown(f"<p style='font-size:.9rem;color:#1B2A4A;'>{u}{pi}</p>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Eksport</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("Pobierz CSV",
            export_to_csv(st.session_state.selections, st.session_state.dietary_notes,
                          st.session_state.guest_count, st.session_state.couple_name, MENU_DATA, UPSELLS),
            file_name=f"menu_{st.session_state.couple_name or 'wesele'}_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv")
    with c2:
        st.download_button("Pobierz JSON",
            json.dumps({"para":st.session_state.couple_name,"goscie":st.session_state.guest_count,
                        "wybory":st.session_state.selections,"diety":st.session_state.dietary_notes,
                        "data_eksportu":datetime.now().isoformat()}, ensure_ascii=False, indent=2),
            file_name=f"menu_{st.session_state.couple_name or 'wesele'}_{datetime.today().strftime('%Y%m%d')}.json",
            mime="application/json")
