import streamlit as st
import math
import pandas as pd
from datetime import datetime
import plotly.express as px  # NOWY IMPORT

# --- Konfiguracja strony ---
st.set_page_config(page_title="Asystent Fitnessu", page_icon="🏋️", layout="wide")

# --- Style CSS ---
st.markdown("""
<style>
/* ... (cały Twój kod CSS pozostaje bez zmian) ... */
 html, body {
    height: 100%;
    margin: 0;
  }
  [data-testid="stAppViewContainer"] {
    position: relative;
    height: 100vh;
    background-image: url("https://wallpapercave.com/wp/wp2563942.jpg");
    background-size: cover;
    background-position: center center;
    background-attachment: fixed;
    overflow: auto; /* ZMIANA: Umożliwia przewijanie, gdy treść jest dłuższa */
  }
  [data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top:0; left:0; right:0; bottom:0;
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(3px);
    -webkit-backdrop-filter: blur(3px);
    z-index: 0;
  }
  [data-testid="stAppViewContainer"] > .main {
    position: relative;
    z-index: 1;
    background: transparent;
  }
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
    right: 2rem;
}
div.st-emotion-cache-16txtl3 {
    background-color: rgba(28, 30, 38, 0.8);
    padding: 1rem;
    border-radius: 0.5rem;
}
.st-emotion-cache-1avcm0n {
    background-color: rgba(15, 17, 22, 0.9);
}
</style>
""", unsafe_allow_html=True)

# --- Struktura danych ---
CWICZENIA_KATEGORIE = {
    "Wybierz kategorię...": {},
    "Klatka piersiowa": {
        "Wyciskanie sztangi leżąc": "https://static.fabrykasily.pl/atlas/wyciskanie_sztangi_na_lawce_plaskiej.mp4",
        "Pompki na poręczach (dipy)": "https://static.fabrykasily.pl/atlas/pompki_na_poreczach.mp4"
    },
    "Plecy": {
        "Martwy ciąg": "https://static.fabrykasily.pl/atlas/klasyczny_martwy_ciag_fabryka.mp4",
        "Podciąganie na drążku": "https://static.fabrykasily.pl/atlas/podciaganie_na_drazku_trzymanym_nachwytem.mp4",
        "Wiosłowanie sztangą": "https://static.fabrykasily.pl/atlas/wioslowanie_sztanaga_trzymana_nachwytem_do_klatki_w_opadzie_tulowia.mp4"
    },
    "Nogi": {
        "Przysiad ze sztangą": "https://static.fabrykasily.pl/atlas/video-poprawka-przysiadu.mp4",
        "Wykroki z hantlami": "https://static.fabrykasily.pl/atlas/wykroki_w_miejscu_z_hantelkami.mp4"
    },
    "Barki": {
        "Wyciskanie żołnierskie (OHP)": "https://static.fabrykasily.pl/atlas/wyciskanie_sztangi_nad_glowe.mp4"
    }
}

# --- Inicjalizacja Session State ---
if 'historia_pomiarow' not in st.session_state:
    st.session_state.historia_pomiarow = []
if 'historia_treningow' not in st.session_state:
    st.session_state.historia_treningow = []
if 'historia_zdjec' not in st.session_state:  # NOWOŚĆ
    st.session_state.historia_zdjec = []

# --- PASEK BOCZNY ---
with st.sidebar:
    st.title("🏋️ Asystent Siłowni")
    st.write("---")
    strona = st.radio(
        "Wybierz stronę:",
        ("Strona główna", "Kalkulatory", "Biblioteka Ćwiczeń", "Dziennik Postępów", "Dziennik Treningowy", "Dziennik Zdjęć"), # <-- DODANA NOWA POZYCJA
        label_visibility="collapsed"
    )
    st.write("---")
    st.info("Aplikacja stworzona w ramach projektu na studia.")

# --- GŁÓWNA CZĘŚĆ APLIKACJI ---
# --- GŁÓWNA CZĘŚĆ APLIKACJI ---

# NOWY BLOK KODU DLA STRONY GŁÓWNEJ
if strona == "Strona główna":
    st.title("Witaj w Twoim Osobistym Asystencie Fitness! 🏋️")
    st.info(
        "Ta aplikacja została stworzona, aby pomóc Ci w monitorowaniu i planowaniu Twojej drogi do lepszej formy. "
        "Wybierz interesujący Cię moduł z menu po lewej stronie."
    )

    st.header("Co znajdziesz w tej aplikacji?")

    st.markdown("""
    - **📊 Kalkulatory:** Zestaw narzędzi do obliczania kluczowych wskaźników, takich jak BMI, dzienne zapotrzebowanie kaloryczne (TDEE) oraz szacunkowy poziom tkanki tłuszczowej.

    - **🎬 Biblioteka Ćwiczeń:** Wizualny atlas ćwiczeń z podziałem na partie mięśniowe. Każde ćwiczenie posiada instruktaż wideo, aby zapewnić poprawną technikę.

    - **📈 Dziennik Postępów:** Twoje centrum monitorowania zmian sylwetkowych. Zapisuj regularnie wagę i wymiary, a aplikacja wygeneruje interaktywne wykresy, abyś mógł śledzić swoje postępy.

    - **📓 Dziennik Treningowy:** Szczegółowo notuj swoje sesje treningowe – wykonane ćwiczenia, ciężar, serie i powtórzenia. Buduj historię swojej siły!

    - **📸 Dziennik Zdjęć:** Nic tak nie motywuje, jak wizualne dowody ciężkiej pracy. Dodawaj zdjęcia sylwetki, aby porównywać zmiany w czasie i utrzymać motywację na najwyższym poziomie.
    """)


if strona == "Kalkulatory":
    # ... (kod tej sekcji pozostaje bez zmian) ...
    st.header("Kalkulatory Fitness")
    st.info("Wybierz kalkulator z poniższych zakładek, aby oszacować swoje wskaźniki.")
    tab1, tab2, tab3 = st.tabs(["📊 Kalkulator BMI", "🔥 Kalkulator TDEE", "💪 Kalkulator Body Fat"])
    with tab1:
        st.subheader("Kalkulator Wskaźnika Masy Ciała (BMI)")
        waga_bmi = st.number_input("Twoja waga (kg)", 30.0, 250.0, 70.0, 0.5)
        wzrost_bmi = st.number_input("Twój wzrost (cm)", 100.0, 250.0, 175.0, 1.0)

        if st.button("Oblicz moje BMI"):
            if wzrost_bmi > 0:
                wzrost_m = wzrost_bmi / 100
                bmi = waga_bmi / (wzrost_m ** 2)
                st.metric("Twoje BMI wynosi", f"{bmi:.2f}")

                # ZAKTUALIZOWANA LOGIKA INTERPRETACJI WYNIKU
                if bmi < 18.5:
                    st.warning("Interpretacja: Niedowaga.")
                elif bmi < 25:
                    st.success("Interpretacja: Waga prawidłowa.")
                elif bmi < 30:
                    st.warning("Interpretacja: Nadwaga.")
                elif bmi < 35:
                    st.error("Interpretacja: Otyłość I stopnia.")
                elif bmi < 40:
                    st.error("Interpretacja: Otyłość II stopnia.")
                else:
                    st.error("Interpretacja: Otyłość III stopnia (otyłość olbrzymia).")
            else:
                st.error("Wzrost musi być większy od zera.")

        st.write("---")  # Linia oddzielająca

        # NOWA TABELA Z KLASYFIKACJĄ BMI
        st.subheader("Klasyfikacja wartości BMI")
        st.markdown("""
        | Wartość BMI     | Interpretacja       |
        |-----------------|---------------------|
        | < 18,5          | Niedowaga           |
        | 18,5 – 24,9     | Waga prawidłowa     |
        | 25,0 – 29,9     | Nadwaga             |
        | 30,0 – 34,9     | Otyłość I stopnia   |
        | 35,0 – 39,9     | Otyłość II stopnia  |
        | ≥ 40,0          | Otyłość III stopnia |
        """)
    with tab2:
        st.subheader("Kalkulator Całkowitego Dziennego Zapotrzebowania Kalorycznego (TDEE)")
        plec_tdee = st.radio("Wybierz płeć", ("Mężczyzna", "Kobieta"))
        waga_tdee = st.number_input("Waga (kg)", 30.0, 250.0, 70.0, 0.5, key="waga_tdee")
        wzrost_tdee = st.number_input("Wzrost (cm)", 100.0, 250.0, 175.0, 1.0, key="wzrost_tdee")
        wiek_tdee = st.number_input("Wiek (lata)", 15, 100, 30, 1)
        poziom_aktywnosci = st.selectbox("Poziom aktywności fizycznej",
                                         ("Siedzący tryb życia (brak lub minimalna aktywność)",
                                          "Lekka aktywność (1-3 dni/tydzień)",
                                          "Umiarkowana aktywność (3-5 dni/tydzień)",
                                          "Wysoka aktywność (6-7 dni/tydzień)",
                                          "Bardzo wysoka aktywność (ciężkie ćwiczenia codziennie)"))
        mnozniki = {"Siedzący tryb życia (brak lub minimalna aktywność)": 1.2,
                    "Lekka aktywność (1-3 dni/tydzień)": 1.375, "Umiarkowana aktywność (3-5 dni/tydzień)": 1.55,
                    "Wysoka aktywność (6-7 dni/tydzień)": 1.725,
                    "Bardzo wysoka aktywność (ciężkie ćwiczenia codziennie)": 1.9}
        if st.button("Oblicz moje zapotrzebowanie kaloryczne"):
            bmr = (10 * waga_tdee) + (6.25 * wzrost_tdee) - (5 * wiek_tdee) + (5 if plec_tdee == "Mężczyzna" else -161)
            tdee = bmr * mnozniki[poziom_aktywnosci]
            st.success(f"Twoje BMR: **{bmr:.0f} kcal** | Twoje TDEE: **{tdee:.0f} kcal**")
    with tab3:
        st.subheader("Kalkulator Procentowej Zawartości Tkanki Tłuszczowej")
        st.warning("Pamiętaj, że jest to szacunek (metoda US Navy) i nie zastąpi profesjonalnego pomiaru.")

        plec_bf = st.radio("Wybierz płeć", ("Mężczyzna", "Kobieta"), key="plec_bf", horizontal=True)

        c1, c2 = st.columns(2)
        with c1:
            wzrost_bf = st.number_input("Wzrost (cm)", 100.0, 250.0, 175.0, 1.0, key="wzrost_bf")
            obwod_szyi = st.number_input("Obwód szyi (cm)", 20.0, 60.0, 40.0, 0.5)
        with c2:
            obwod_talii = st.number_input("Obwód talii (cm)", 50.0, 150.0, 80.0, 0.5)
            if plec_bf == "Kobieta":
                obwod_bioder = st.number_input("Obwód bioder (cm)", 60.0, 150.0, 95.0, 0.5)

        if st.button("Oblicz poziom tłuszczu"):
            try:
                if plec_bf == "Mężczyzna":
                    body_fat = 495 / (1.0324 - 0.19077 * math.log10(obwod_talii - obwod_szyi) + 0.15456 * math.log10(
                        wzrost_bf)) - 450
                    st.metric("Szacowany poziom tkanki tłuszczowej", f"{body_fat:.1f}%")
                    # NOWOŚĆ: Interpretacja wyniku dla mężczyzn
                    if body_fat <= 4:
                        st.success("Interpretacja: Niezbędna tkanka tłuszczowa")
                    elif body_fat <= 13:
                        st.success("Interpretacja: Poziom atletyczny")
                    elif body_fat <= 17:
                        st.success("Interpretacja: Poziom fitness")
                    elif body_fat <= 25:
                        st.warning("Interpretacja: Poziom akceptowalny")
                    else:
                        st.error("Interpretacja: Otyłość")
                else:  # Kobieta
                    body_fat = 495 / (1.29579 - 0.35004 * math.log10(
                        obwod_talii + obwod_bioder - obwod_szyi) + 0.22100 * math.log10(wzrost_bf)) - 450
                    st.metric("Szacowany poziom tkanki tłuszczowej", f"{body_fat:.1f}%")
                    # NOWOŚĆ: Interpretacja wyniku dla kobiet
                    if body_fat <= 12:
                        st.success("Interpretacja: Niezbędna tkanka tłuszczowa")
                    elif body_fat <= 20:
                        st.success("Interpretacja: Poziom atletyczny")
                    elif body_fat <= 24:
                        st.success("Interpretacja: Poziom fitness")
                    elif body_fat <= 31:
                        st.warning("Interpretacja: Poziom akceptowalny")
                    else:
                        st.error("Interpretacja: Otyłość")
            except (ValueError, ZeroDivisionError):
                st.error("Wprowadzone wymiary są nieprawidłowe lub niemożliwe do obliczenia.")

        st.write("---")

        # NOWA TABELA Z KLASYFIKACJĄ
        st.subheader("Kategorie ze względu na poziom tłuszczu w ciele")
        st.markdown("""
        | Klasyfikacja                  | Kobiety (% tkanki tłuszczowej) | Mężczyźni (% tkanki tłuszczowej) |
        |-------------------------------|--------------------------------|----------------------------------|
        | **Niezbędna tkanka tłuszczowa** | 10-12%                         | 2-4%                             |
        | **Atletyczna** | 14-20%                         | 6-13%                            |
        | **Fitness** | 21-24%                         | 14-17%                           |
        | **Akceptowalna** | 25-31%                         | 18-25%                           |
        | **Otyłość** | ≥ 32%                          | ≥ 25%                            |
        """)

elif strona == "Biblioteka Ćwiczeń":
    # ... (kod tej sekcji pozostaje bez zmian) ...
    st.header("🎬 Biblioteka Ćwiczeń")
    st.info("Wybierz partię mięśniową, a następnie ćwiczenie, aby zobaczyć instruktaż wideo.")
    lista_kategorii = list(CWICZENIA_KATEGORIE.keys())
    wybrana_kategoria = st.selectbox("1. Wybierz partię mięśniową:", lista_kategorii)
    if wybrana_kategoria != "Wybierz kategorię...":
        lista_cwiczen = list(CWICZENIA_KATEGORIE[wybrana_kategoria].keys())
        wybrane_cwiczenie = st.selectbox("2. Wybierz ćwiczenie:", lista_cwiczen)
        if wybrane_cwiczenie: st.video(CWICZENIA_KATEGORIE[wybrana_kategoria][wybrane_cwiczenie])

elif strona == "Dziennik Postępów":
    st.header("📈 Dziennik Postępów Sylwetkowych")
    st.info("Regularnie zapisuj swoje pomiary, aby śledzić zmiany w czasie i wizualizować postępy.")
    with st.form("pomiar_form", clear_on_submit=True):
        st.subheader("➕ Dodaj nowy pomiar")
        c1, c2 = st.columns(2)
        data_pomiaru = c1.date_input("Data pomiaru", datetime.now())
        waga_pomiaru = c2.number_input("Waga (kg)", 30.0, 250.0, 70.0, 0.1)
        st.write("Wprowadź obwody (cm):")
        c3, c4, c5 = st.columns(3)
        talia_pomiaru = c3.number_input("Talia", 40, 150, 80, 1)
        klatka_pomiaru = c4.number_input("Klatka piersiowa", 50, 200, 100, 1)
        biceps_pomiaru = c5.number_input("Biceps", 15, 60, 35, 1)
        if st.form_submit_button("Zapisz pomiar"):
            st.session_state.historia_pomiarow.append(
                {"Data": data_pomiaru, "Waga (kg)": waga_pomiaru, "Talia (cm)": talia_pomiaru,
                 "Klatka (cm)": klatka_pomiaru, "Biceps (cm)": biceps_pomiaru})
            st.success("Pomiar został pomyślnie zapisany!")

    if st.session_state.historia_pomiarow:
        st.write("---")
        st.subheader("📊 Historia i Wizualizacja")

        if st.session_state.historia_pomiarow:
            df = pd.DataFrame(st.session_state.historia_pomiarow)
            df["Data"] = pd.to_datetime(df["Data"])
            df = df.sort_values("Data").set_index("Data")

            wybrany_pomiar = st.selectbox("Pokaż wykres dla:",
                                          ["Waga (kg)", "Talia (cm)", "Klatka (cm)", "Biceps (cm)"],
                                          key="progress_chart_select")

            # Wykres Plotly (zakładam, że ta wersja jest już u Ciebie)
            fig = px.line(df, x=df.index, y=wybrany_pomiar, title=f"Postępy - {wybrany_pomiar}", markers=True)
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df)

            # --- ZARZĄDZANIE DANYMI: EKSPORT I USUWANIE ---
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                # Eksport
                csv = df.reset_index().to_csv(index=False).encode("utf-8")
                st.download_button("📥 Eksportuj Pomiary do CSV", csv, "historia_pomiarow.csv", "text/csv")
            with col2:
                # Usuwanie
                if st.button("🗑️ Wyczyść Historię Pomiarów"):
                    st.session_state.historia_pomiarow = []
                    st.rerun()  # Odświeża stronę, aby pokazać zmiany

        else:
            st.warning("Brak zapisanych pomiarów. Dodaj swój pierwszy wpis, aby zobaczyć historię.")

        # --- ZARZĄDZANIE DANYMI: IMPORT ---
        with st.expander("⬆️ Importuj historię pomiarów z pliku CSV"):
            uploaded_file_pomiar = st.file_uploader("Wybierz plik CSV z pomiarami", type="csv", key="uploader_pomiary")
            if uploaded_file_pomiar:
                try:
                    df_imported = pd.read_csv(uploaded_file_pomiar)
                    REQUIRED_COLS = {'Data', 'Waga (kg)', 'Talia (cm)', 'Klatka (cm)', 'Biceps (cm)'}
                    if REQUIRED_COLS.issubset(df_imported.columns):
                        st.session_state.historia_pomiarow = df_imported.to_dict('records')
                        st.success("Dane pomiarów zostały pomyślnie zaimportowane!")
                        st.rerun()
                    else:
                        st.error(f"Plik CSV musi zawierać wymagane kolumny: {REQUIRED_COLS}")
                except Exception as e:
                    st.error(f"Wystąpił błąd podczas przetwarzania pliku: {e}")

elif strona == "Dziennik Treningowy":
    st.header("📓 Dziennik Treningowy")
    st.info("Zapisuj swoje treningi, aby śledzić postępy w sile i wytrzymałości.")

    # Formularz do dodawania wpisów (pozostaje bez zmian)
    with st.form("trening_form", clear_on_submit=True):
        st.subheader("➕ Dodaj nowy wpis treningowy")
        data_treningu = st.date_input("Data treningu", datetime.now())
        wszystkie_cwiczenia = sorted(list(set(ex for cat in CWICZENIA_KATEGORIE.values() for ex in cat.keys())))
        wybrane_cwiczenie = st.selectbox("Wybierz ćwiczenie", wszystkie_cwiczenia)

        c1, c2, c3 = st.columns(3)
        ciezar = c1.number_input("Ciężar (kg)", 0.0, 500.0, 20.0, 0.5)
        serie = c2.number_input("Serie", 1, 10, 3, 1)
        powtorzenia = c3.number_input("Powtórzenia", 1, 50, 10, 1)

        if st.form_submit_button("Zapisz trening"):
            st.session_state.historia_treningow.append({
                "Data": data_treningu, "Ćwiczenie": wybrane_cwiczenie, "Ciężar (kg)": ciezar,
                "Serie": serie, "Powtórzenia": powtorzenia
            })
            st.success("Trening został zapisany!")

    # Wyświetlanie historii i NOWE opcje zarządzania danymi
    if st.session_state.historia_treningow:
        st.write("---")
        st.subheader("Historia Treningów")
        df_treningi = pd.DataFrame(st.session_state.historia_treningow)
        df_treningi["Data"] = pd.to_datetime(df_treningi["Data"])
        st.dataframe(df_treningi.sort_values("Data", ascending=False).set_index("Data"))

        # --- NOWOŚĆ: ZARZĄDZANIE DANYMI TRENINGOWYMI ---
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            # Eksport
            csv_treningi = df_treningi.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Eksportuj Treningi do CSV", csv_treningi, "historia_treningow.csv", "text/csv")
        with col2:
            # Usuwanie
            if st.button("🗑️ Wyczyść Historię Treningów"):
                st.session_state.historia_treningow = []
                st.rerun()

    else:
        st.warning("Brak zapisanych treningów.")

    # --- NOWOŚĆ: IMPORT DANYCH TRENINGOWYCH ---
    with st.expander("⬆️ Importuj historię treningów z pliku CSV"):
        uploaded_file_trening = st.file_uploader("Wybierz plik CSV z treningami", type="csv", key="uploader_treningi")
        if uploaded_file_trening:
            try:
                df_imported_t = pd.read_csv(uploaded_file_trening)
                REQUIRED_COLS_T = {'Data', 'Ćwiczenie', 'Ciężar (kg)', 'Serie', 'Powtórzenia'}
                if REQUIRED_COLS_T.issubset(df_imported_t.columns):
                    st.session_state.historia_treningow = df_imported_t.to_dict('records')
                    st.success("Dane treningów zostały pomyślnie zaimportowane!")
                    st.rerun()
                else:
                    st.error(f"Plik CSV musi zawierać wymagane kolumny: {REQUIRED_COLS_T}")
            except Exception as e:
                st.error(f"Wystąpił błąd podczas przetwarzania pliku: {e}")
# --- NOWOŚĆ: Całkowicie nowa strona "Dziennik Zdjęć" ---
elif strona == "Dziennik Zdjęć":
    st.header("📸 Dziennik Zdjęć Sylwetki")
    st.info("Dodawaj zdjęcia, aby wizualnie śledzić swoje postępy. To świetna motywacja!")

    with st.form("zdjecie_form", clear_on_submit=True):
        st.subheader("➕ Dodaj nowe zdjęcie")
        data_zdjecia = st.date_input("Data zrobienia zdjęcia")
        notatka = st.text_input("Krótka notatka (np. 'Koniec redukcji', 'Początek masy')")
        plik_zdjecia = st.file_uploader("Wybierz plik ze zdjęciem", type=['png', 'jpg', 'jpeg'])

        if st.form_submit_button("Zapisz zdjęcie"):
            if plik_zdjecia is not None:
                # Wczytujemy obraz jako bajty i zapisujemy w pamięci sesji
                st.session_state.historia_zdjec.append({
                    "data": data_zdjecia,
                    "notatka": notatka,
                    "obraz": plik_zdjecia.getvalue()
                })
                st.success("Zdjęcie zostało zapisane!")
            else:
                st.warning("Nie wybrano żadnego pliku ze zdjęciem.")

    st.write("---")
    st.subheader("Galeria Twoich Postępów")

    if st.session_state.historia_zdjec:
        # Sortujemy zdjęcia od najnowszych do najstarszych
        posortowane_zdjecia = sorted(st.session_state.historia_zdjec, key=lambda x: x['data'], reverse=True)

        # Tworzymy galerię w 3 kolumnach
        for i in range(0, len(posortowane_zdjecia), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(posortowane_zdjecia):
                    with cols[j]:
                        zdjecie = posortowane_zdjecia[i + j]
                        st.image(zdjecie["obraz"],
                                 caption=f"{zdjecie['data'].strftime('%Y-%m-%d')} - {zdjecie['notatka']}")

        if st.button("🗑️ Wyczyść całą historię zdjęć"):
            st.session_state.historia_zdjec = []
            st.rerun()
    else:
        st.warning("Brak zapisanych zdjęć. Dodaj swoje pierwsze zdjęcie, aby rozpocząć!")

