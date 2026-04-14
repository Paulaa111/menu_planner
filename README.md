# 🌸 Konfigurator Menu Weselnego

Interaktywna aplikacja Streamlit z AI Asystentem Smaku, stworzona jako demo dla restauracji weselnych.

## ✨ Funkcje

- **Konfigurator menu** – wybór dań z podziałem na kategorie (zupy, dania główne, dodatki, desery)
- **Asystent Smaku AI** – podpowiedzi kompozycji smakowych oparte na Claude API
- **Upselling** – sekcja dodatków premium (fontanna czekoladowa, wiejski stół, pakiet napojów...)
- **Diety pod kontrolą** – zbieranie info o wegetarianach, weganach, alergiach
- **Eksport** – gotowy CSV dla kuchni i JSON dla systemu restauracji
- **Podsumowanie** – automatyczne liczenie porcji per gość

---

## 🚀 Uruchomienie lokalne

### 1. Klonowanie repozytorium
```bash
git clone https://github.com/TWOJ_USERNAME/wedding-menu-configurator.git
cd wedding-menu-configurator
```

### 2. Środowisko wirtualne
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Instalacja zależności
```bash
pip install -r requirements.txt
```

### 4. Klucz API Anthropic

Skopiuj plik przykładowy i uzupełnij kluczem:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Edytuj `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-TWÓJ_KLUCZ"
```

> Klucz API uzyskasz na: https://console.anthropic.com

### 5. Uruchomienie
```bash
streamlit run app.py
```

---

## ☁️ Deploy na Streamlit Cloud

1. Wrzuć kod na GitHub (`.gitignore` pilnuje, żeby `secrets.toml` nie trafił do repo).
2. Wejdź na [share.streamlit.io](https://share.streamlit.io) → **New app** → wybierz repo.
3. W zakładce **Secrets** dodaj:
   ```
   ANTHROPIC_API_KEY = "sk-ant-TWÓJ_KLUCZ"
   ```
4. Kliknij **Deploy** – gotowe! 🎉

---

## 📁 Struktura projektu

```
wedding-menu-configurator/
├── app.py              # Główna aplikacja Streamlit
├── menu_data.py        # Dane menu (edytuj wg oferty restauracji)
├── utils.py            # Helpers: podsumowanie, eksport CSV
├── requirements.txt    # Zależności Python
├── .gitignore
└── .streamlit/
    └── secrets.toml.example   # Szablon konfiguracji (nie commituj secrets.toml!)
```

---

## 🛠️ Dostosowanie

Cała oferta restauracji jest w pliku `menu_data.py`. Możesz tam:
- dodawać/usuwać kategorie i dania,
- edytować opisy i alergeny,
- modyfikować listę dodatków premium (UPSELLS) z cenami.

---

## 📄 Licencja

MIT – używaj swobodnie jako demo lub baza do rozbudowy.
