import streamlit as st
import math
import pandas as pd
from datetime import datetime
import plotly.express as px  # Plotly Express do interaktywnych wykresów

# Konfiguracja strony
st.set_page_config(
    page_title="Asystent Fitnessu",
    page_icon="🏋️",
    layout="wide"
)

# Style CSS
st.markdown("""
<style>
/* ... (cały Twój kod CSS pozostaje bez zmian) ... */
 html, body {
    height: 100%; /* Ustawienie wysokości na 100% dla html i body */
    margin: 0; /* Usunięcie domyślnego marginesu */
  }
  [data-testid="stAppViewContainer"] {
    position: relative; /* Pozycjonowanie relatywne dla kontenera głównego aplikacji */
    height: 100vh; /* Wysokość kontenera na 100% wysokości widocznego obszaru */
    background-image: url("https://wallpapercave.com/wp/wp2563942.jpg"); /* Ustawienie obrazu tła */
    background-size: cover; /* Pokrycie całego tła obrazem */
    background-position: center center; /* Wyśrodkowanie obrazu tła */
    background-attachment: fixed; /* Tło pozostaje nieruchome podczas przewijania */
    overflow: auto; /* ZMIANA: Umożliwia przewijanie, gdy treść jest dłuższa */
  }
  [data-testid="stAppViewContainer"]::before {
    content: ""; /* Tworzenie pseudoelementu do nałożenia warstwy na tło */
    position: absolute; /* Pozycjonowanie absolutne względem rodzica */
    top:0; left:0; right:0; bottom:0; /* Rozciągnięcie na cały obszar rodzica */
    background: rgba(0,0,0,0.4); /* Półprzezroczyste czarne tło */
    backdrop-filter: blur(3px); /* Rozmycie tła za elementem */
    -webkit-backdrop-filter: blur(3px); /* Wersja dla przeglądarek WebKit */
    z-index: 0; /* Ustawienie niskiego z-index, aby inne elementy były nad nim */
  }
  [data-testid="stAppViewContainer"] > .main {
    position: relative; /* Pozycjonowanie relatywne dla głównej zawartości aplikacji */
    z-index: 1; /* Ustawienie wyższego z-index, aby główna zawartość była nad tłem */
    background: transparent; /* Przezroczyste tło dla głównej zawartości */
  }
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0); /* Przezroczyste tło dla nagłówka Streamlit */
}
[data-testid="stToolbar"] {
    right: 2rem; /* Przesunięcie paska narzędzi Streamlit w prawo */
}
div.st-emotion-cache-16txtl3 {
    background-color: rgba(28, 30, 38, 0.8); /* Półprzezroczyste ciemne tło dla specyficznego komponentu */
    padding: 1rem; /* Wewnętrzny odstęp */
    border-radius: 0.5rem; /* Zaokrąglenie rogów */
}
.st-emotion-cache-1avcm0n {
    background-color: rgba(15, 17, 22, 0.9); /* Półprzezroczyste bardzo ciemne tło dla innego komponentu */
}
</style>
""", unsafe_allow_html=True)  # Pozwolenie na renderowanie HTML w Streamlit

# Struktura danych
# Słownik przechowujący kategorie ćwiczeń i przypisane do nich linki do filmów instruktażowych
CWICZENIA_KATEGORIE = {
    "Wybierz kategorię...": {},
    "Klatka piersiowa": {
        "Wyciskanie sztangi leżąc": "https://static.fabrykasily.pl/atlas/wyciskanie_sztangi_na_lawce_plaskiej.mp4",
        "Pompki na poręczach (dipy)": "https://static.fabrykasily.pl/atlas/pompki_na_poreczach.mp4"
    },
    "Plecy": {
        "Martwy ciąg": "https://static.fabrykasily.pl/atlas/klasyczny_martwy_ciag_fabryka.mp4",
        "Podciąganie na drążku": "https://static.rykasily.pl/atlas/podciaganie_na_drazku_trzymanym_nachwytem.mp4",
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

# Inicjalizacja Session State
# Session_state do przechowywania danych między ponownymi uruchomieniami skryptu.
if 'historia_pomiarow' not in st.session_state:
    st.session_state.historia_pomiarow = []  # Listy do przechowywania histori
if 'historia_treningow' not in st.session_state:
    st.session_state.historia_treningow = []  # Listy do przechowywania histori
if 'historia_zdjec' not in st.session_state:
    st.session_state.historia_zdjec = []  # Listy do przechowywania histori

# PASEK BOCZNY
with st.sidebar:
    st.title("🏋️ Asystent Siłowni")
    st.write("---")  # Linia podziałki
    strona = st.radio(  # Widget radio button żeby sobie wybrać która stronę aktualnie chcemy przeglądać
        "Wybierz stronę:",
        ("Strona główna", "Kalkulatory", "Biblioteka Ćwiczeń", "Dziennik Postępów", "Dziennik Treningowy",
         "Dziennik Zdjęć"),
        label_visibility="collapsed"  # Ukrycie etykiety, aby było czyściej
    )
    st.write("---")

# GŁÓWNA CZĘŚĆ APLIKACJI

# Podzieliłem strone na bloki w zależności co wybrał użytwkownik w nawigacji strony na pasku bocznym
if strona == "Strona główna":  # Warunek do sprawdzenia czy kliknięto stronę główną
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
    """)  # Lista stworzona za pomocą markdowna

# Sekcja kalkulatorów
elif strona == "Kalkulatory":
    st.header("Kalkulatory Fitness")
    st.info("Wybierz kalkulator z poniższych zakładek, aby oszacować swoje wskaźniki.")
    # Aby wyglądało to estetyczniej użyłem zakładek dla każdego kalkulatora
    tab1, tab2, tab3 = st.tabs(["📊 Kalkulator BMI", "🔥 Kalkulator TDEE", "💪 Kalkulator Body Fat"])

    with tab1:  # Pierwsza zakładka - Kalkulator BMI
        st.subheader("Kalkulator Wskaźnika Masy Ciała (BMI)")
        waga_bmi = st.number_input("Twoja waga (kg)", 30.0, 250.0, 70.0, 0.5)
        wzrost_bmi = st.number_input("Twój wzrost (cm)", 100.0, 250.0, 175.0, 1.0)

        if st.button("Oblicz moje BMI"):
            if wzrost_bmi > 0:  # czy wzrost jest większy od zera
                wzrost_m = wzrost_bmi / 100  # wzrost z cm na m
                bmi = waga_bmi / (wzrost_m ** 2)  # Wzór na bmi
                st.metric("Twoje BMI wynosi", f"{bmi:.2f}")

                # Jakaś interpretacja wyniku z googla
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
                st.error("Wzrost musi być większy od zera.")  # Error jeśli wzrost jest nieprawidłowo podany

        st.write("---")  # Linia podziałki

        # Tabela z wartościami bmi z googla zrobiona w markdown
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

    with tab2:  # Druga zakładka - Kalkulator TDEE
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
        # Słownik mapujący poziom aktywności na mnożnik
        mnozniki = {"Siedzący tryb życia (brak lub minimalna aktywność)": 1.2,
                    "Lekka aktywność (1-3 dni/tydzień)": 1.375, "Umiarkowana aktywność (3-5 dni/tydzień)": 1.55,
                    "Wysoka aktywność (6-7 dni/tydzień)": 1.725,
                    "Bardzo wysoka aktywność (ciężkie ćwiczenia codziennie)": 1.9}
        if st.button("Oblicz moje zapotrzebowanie kaloryczne"):  # Button do obliczania TDEE
            # Obliczenie BMR (Basal Metabolic Rate - Podstawowa Przemiana Materii) wzięte z google
            bmr = (10 * waga_tdee) + (6.25 * wzrost_tdee) - (5 * wiek_tdee) + (5 if plec_tdee == "Mężczyzna" else -161)
            tdee = bmr * mnozniki[poziom_aktywnosci]  # Obliczenie TDEE
            st.success(f"Twoje BMR: **{bmr:.0f} kcal** | Twoje TDEE: **{tdee:.0f} kcal**")  # Wyświetlenie wyników

    with tab3:  # Trzecia zakładka - Kalkulator Body Fat
        st.subheader("Kalkulator Procentowej Zawartości Tkanki Tłuszczowej")
        st.warning("Pamiętaj, że jest to szacunek (metoda US Navy) i nie zastąpi profesjonalnego pomiaru.")  # Warning

        plec_bf = st.radio("Wybierz płeć", ("Mężczyzna", "Kobieta"), key="plec_bf", horizontal=True)

        c1, c2 = st.columns(2)  # Tworzenie dwóch kolumn
        with c1:  # Pierwsza kolumna
            wzrost_bf = st.number_input("Wzrost (cm)", 100.0, 250.0, 175.0, 1.0, key="wzrost_bf")  # Pole wzrostu
            obwod_szyi = st.number_input("Obwód szyi (cm)", 20.0, 60.0, 40.0, 0.5)  # Pole obwodu szyi
        with c2:  # Druga kolumna
            obwod_talii = st.number_input("Obwód talii (cm)", 50.0, 150.0, 80.0, 0.5)  # Pole obwodu talii
            if plec_bf == "Kobieta":  # Warunek dla kobiet
                obwod_bioder = st.number_input("Obwód bioder (cm)", 60.0, 150.0, 95.0,
                                               0.5)  # Pole obwodu bioder dla kobiet

        if st.button("Oblicz poziom tłuszczu"):  # bUTTON do obliczania poziomu tłuszczu
            try:
                if plec_bf == "Mężczyzna":  # dla m
                    body_fat = 495 / (1.0324 - 0.19077 * math.log10(obwod_talii - obwod_szyi) + 0.15456 * math.log10(
                        wzrost_bf)) - 450
                    st.metric("Szacowany poziom tkanki tłuszczowej", f"{body_fat:.1f}%")
                    # interpretacja dla m
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
                else:  # dla k
                    body_fat = 495 / (1.29579 - 0.35004 * math.log10(
                        obwod_talii + obwod_bioder - obwod_szyi) + 0.22100 * math.log10(wzrost_bf)) - 450
                    st.metric("Szacowany poziom tkanki tłuszczowej", f"{body_fat:.1f}%")
                    # interpretacja dla k
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
            except (ValueError, ZeroDivisionError):  # Obsługa błędów
                st.error("Wprowadzone wymiary są nieprawidłowe lub niemożliwe do obliczenia.")

        st.write("---")  # Linia podziałki

        # Tabela body fatu z googla zrobiona w markdown
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

    # Sekcja biblioteki ćwiczeń
elif strona == "Biblioteka Ćwiczeń":
    st.header("🎬 Biblioteka Ćwiczeń")
    st.info("Wybierz partię mięśniową, a następnie ćwiczenie, aby zobaczyć instruktaż wideo.")
    lista_kategorii = list(CWICZENIA_KATEGORIE.keys())  # Pobranie listy kategorii z słownika
    wybrana_kategoria = st.selectbox("1. Wybierz partię mięśniową:", lista_kategorii)  # Wybór kategorii
    if wybrana_kategoria != "Wybierz kategorię...":  # Sprawdzenie, czy wybrano konkretną kategorię
        lista_cwiczen = list(
            CWICZENIA_KATEGORIE[wybrana_kategoria].keys())  # Pobranie listy ćwiczeń dla wybranej kategorii
        wybrane_cwiczenie = st.selectbox("2. Wybierz ćwiczenie:", lista_cwiczen)  # Wybór ćwiczenia
        if wybrane_cwiczenie:  # Jeśli wybrano ćwiczenie
            st.video(CWICZENIA_KATEGORIE[wybrana_kategoria][wybrane_cwiczenie])  # Wyświetlenie filmu instruktażowego

# Sekcja dziennika postępów
elif strona == "Dziennik Postępów":
    st.header("📈 Dziennik Postępów Sylwetkowych")
    st.info("Regularnie zapisuj swoje pomiary, aby śledzić zmiany w czasie i wizualizować postępy.")
    with st.form("pomiar_form", clear_on_submit=True):  # Formularz do dodawania nowego pomiaru
        st.subheader("➕ Dodaj nowy pomiar")  # Podnagłówek
        c1, c2 = st.columns(2)  # Tworzenie dwóch kolumn
        data_pomiaru = c1.date_input("Data pomiaru", datetime.now())  # Pole do wyboru daty pomiaru
        waga_pomiaru = c2.number_input("Waga (kg)", 30.0, 250.0, 70.0, 0.1)  # Pole do wprowadzenia wagi
        st.write("Wprowadź obwody (cm):")  # Tekst informacyjny
        c3, c4, c5 = st.columns(3)  # Tworzenie trzech kolumn dla obwodów
        talia_pomiaru = c3.number_input("Talia", 40, 150, 80, 1)  # Pole obwodu talii
        klatka_pomiaru = c4.number_input("Klatka piersiowa", 50, 200, 100, 1)  # Pole obwodu klatki
        biceps_pomiaru = c5.number_input("Biceps", 15, 60, 35, 1)  # Pole obwodu bicepsa
        if st.form_submit_button("Zapisz pomiar"):  # Button do zapisywania pomiaru
            st.session_state.historia_pomiarow.append(  # Dodanie pomiaru do listy w session_state
                {"Data": data_pomiaru, "Waga (kg)": waga_pomiaru, "Talia (cm)": talia_pomiaru,
                 "Klatka (cm)": klatka_pomiaru, "Biceps (cm)": biceps_pomiaru})
            st.success("Pomiar został pomyślnie zapisany!")  # Komunikat jeśli sie udało

    if st.session_state.historia_pomiarow:  # Jeśli istnieją zapisane pomiary
        st.write("---")  # Linia podziałki
        st.subheader("📊 Historia i Wizualizacja")

        if st.session_state.historia_pomiarow:  # Ponowne sprawdzenie
            df = pd.DataFrame(st.session_state.historia_pomiarow)  # Utworzenie DataFrame z historii pomiarów
            df["Data"] = pd.to_datetime(df["Data"])  # Konwersja kolumny 'Data' na typ datetime
            df = df.sort_values("Data").set_index("Data")  # Sortowanie po dacie i ustawienie jej jako indeks

            wybrany_pomiar = st.selectbox("Pokaż wykres dla:",  # Wybór pomiaru do wizualizacji na wykresie
                                          ["Waga (kg)", "Talia (cm)", "Klatka (cm)", "Biceps (cm)"],
                                          key="progress_chart_select")

            # Wykres Plotly
            fig = px.line(df, x=df.index, y=wybrany_pomiar, title=f"Postępy - {wybrany_pomiar}",
                          markers=True)  # Stworzenie wykresu
            # Konfiguracja wyglądu wykresu
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)  # Wyświetlenie wykresu

            st.dataframe(df)  # Wyświetlenie danych w formie tabeli

            # ZARZĄDZANIE DANYMI: EKSPORT I USUWANIE
            st.write("---")  # Linia podziałki
            col1, col2 = st.columns(2)  # Tworzenie dwóch kolumn
            with col1:  # Pierwsza eksport
                csv = df.reset_index().to_csv(index=False).encode("utf-8")  # Konwersja DataFrame do CSV
                st.download_button("📥 Eksportuj Pomiary do CSV", csv, "historia_pomiarow.csv",
                                   "text/csv")  # Przycisk do pobierania CSV
            with col2:  # Druga usuwanie
                if st.button("🗑️ Wyczyść Historię Pomiarów"):  # Przycisk do czyszczenia historii
                    st.session_state.historia_pomiarow = []  # Usunięcie danych z session_state
                    st.rerun()  # Odświeżenie strony, aby pokazać zmiany

        else:
            st.warning(
                "Brak zapisanych pomiarów. Dodaj swój pierwszy wpis, aby zobaczyć historię.")  # Komunikat o braku danych

        # ZARZĄDZANIE DANYMI: IMPORT ---
        with st.expander("⬆️ Importuj historię pomiarów z pliku CSV"):  # Rozwijany panel do importu danych
            uploaded_file_pomiar = st.file_uploader("Wybierz plik CSV z pomiarami", type="csv",
                                                    key="uploader_pomiary")  # Przycisk do przesyłania pliku CSV
            if uploaded_file_pomiar:  # Jeśli plik został przesłany
                try:
                    df_imported = pd.read_csv(uploaded_file_pomiar)  # Wczytanie pliku CSV do DataFrame
                    REQUIRED_COLS = {'Data', 'Waga (kg)', 'Talia (cm)', 'Klatka (cm)',
                                     'Biceps (cm)'}  # Wymagane kolumny
                    if REQUIRED_COLS.issubset(df_imported.columns):  # Sprawdzenie, czy plik zawiera wymagane kolumny
                        st.session_state.historia_pomiarow = df_imported.to_dict(
                            'records')  # Zapisanie danych do session_state
                        st.success("Dane pomiarów zostały pomyślnie zaimportowane!")  # Komunikat sukcesu
                        st.rerun()  # Odświeżenie strony
                    else:
                        st.error(
                            f"Plik CSV musi zawierać wymagane kolumny: {REQUIRED_COLS}")  # Komunikat błędu o brakujących kolumnach
                except Exception as e:  # Obsługa innych błędów
                    st.error(f"Wystąpił błąd podczas przetwarzania pliku: {e}")

# Sekcja dziennika treningowego
elif strona == "Dziennik Treningowy":
    st.header("📓 Dziennik Treningowy")
    st.info("Zapisuj swoje treningi, aby śledzić postępy w sile i wytrzymałości.")

    # Formularz do dodawania wpisów
    with st.form("trening_form", clear_on_submit=True):  # Formularz do dodawania nowego treningu
        st.subheader("➕ Dodaj nowy wpis treningowy")
        data_treningu = st.date_input("Data treningu", datetime.now())  # Pole wyboru daty treningu
        wszystkie_cwiczenia = sorted(list(
            set(ex for cat in CWICZENIA_KATEGORIE.values() for ex in cat.keys())))  # Pobranie listy wszystkich ćwiczeń
        wybrane_cwiczenie = st.selectbox("Wybierz ćwiczenie", wszystkie_cwiczenia)  # Wybór ćwiczenia

        c1, c2, c3 = st.columns(3)  # Tworzenie trzech kolumn
        ciezar = c1.number_input("Ciężar (kg)", 0.0, 500.0, 20.0, 0.5)  # Pole wprowadzenia ciężaru
        serie = c2.number_input("Serie", 1, 10, 3, 1)  # Pole wprowadzenia liczby serii
        powtorzenia = c3.number_input("Powtórzenia", 1, 50, 10, 1)  # Pole wprowadzenia liczby powtórzeń

        if st.form_submit_button("Zapisz trening"):  # Przycisk do zapisywania treningu
            st.session_state.historia_treningow.append({  # Dodanie treningu do listy w session_state
                "Data": data_treningu, "Ćwiczenie": wybrane_cwiczenie, "Ciężar (kg)": ciezar,
                "Serie": serie, "Powtórzenia": powtorzenia
            })
            st.success("Trening został zapisany!")  # Komunikat jeśli sie udało

    # Wyświetlanie historii i opcje zarządzania danymi
    if st.session_state.historia_treningow:  # Jeśli istnieją zapisane treningi
        st.write("---")  # Linia podziałki
        st.subheader("Historia Treningów")
        df_treningi = pd.DataFrame(st.session_state.historia_treningow)  # Utworzenie DataFrame z historii treningów
        df_treningi["Data"] = pd.to_datetime(df_treningi["Data"])  # Konwersja kolumny 'Data' na typ datetime
        st.dataframe(df_treningi.sort_values("Data", ascending=False).set_index(
            "Data"))  # Wyświetlenie tabeli z danymi treningów

        # ZARZĄDZANIE DANYMI TRENINGOWYMI
        st.write("---")
        col1, col2 = st.columns(2)  # Dwie kolumny
        with col1:  # Pierwsza eksport
            csv_treningi = df_treningi.to_csv(index=False).encode("utf-8")  # Konwersja DataFrame do CSV
            st.download_button("📥 Eksportuj Treningi do CSV", csv_treningi, "historia_treningow.csv",
                               "text/csv")  # Przycisk do pobierania CSV
        with col2:  # Druga uisuwanie
            if st.button("🗑️ Wyczyść Historię Treningów"):  # Przycisk do czyszczenia historii treningów
                st.session_state.historia_treningow = []  # Usunięcie danych z session_state
                st.rerun()  # Odświeżenie strony

    else:
        st.warning("Brak zapisanych treningów.")  # Komunikat jęsli brakuje danych

    # IMPORT DANYCH TRENINGOWYCH
    with st.expander("⬆️ Importuj historię treningów z pliku CSV"):  # Rozwijany panel do importu danych
        uploaded_file_trening = st.file_uploader("Wybierz plik CSV z treningami", type="csv",
                                                 key="uploader_treningi")  # Przycisk do przesyłania pliku CSV
        if uploaded_file_trening:  # Jeśli plik został przesłany
            try:
                df_imported_t = pd.read_csv(uploaded_file_trening)  # Wczytanie pliku CSV do DataFrame
                REQUIRED_COLS_T = {'Data', 'Ćwiczenie', 'Ciężar (kg)', 'Serie', 'Powtórzenia'}  # Wymagane kolumny
                if REQUIRED_COLS_T.issubset(df_imported_t.columns):  # Sprawdzenie, czy plik zawiera wymagane kolumny
                    st.session_state.historia_treningow = df_imported_t.to_dict(
                        'records')  # Zapisanie danych do session_state
                    st.success("Dane treningów zostały pomyślnie zaimportowane!")  # Komunikat jeśli sie udało
                    st.rerun()  # Odświeżenie strony
                else:
                    st.error(
                        f"Plik CSV musi zawierać wymagane kolumny: {REQUIRED_COLS_T}")  # Komunikat błędu jesli brakuje kolumn
            except Exception as e:  # Obsługa innych błędów
                st.error(f"Wystąpił błąd podczas przetwarzania pliku: {e}")

# Sekcja Dziennika Zdjęć
elif strona == "Dziennik Zdjęć":
    st.header("📸 Dziennik Zdjęć Sylwetki")
    st.info("Dodawaj zdjęcia, aby wizualnie śledzić swoje postępy. To świetna motywacja!")

    with st.form("zdjecie_form", clear_on_submit=True):  # Formularz do dodawania nowego zdjęcia
        st.subheader("➕ Dodaj nowe zdjęcie")
        data_zdjecia = st.date_input("Data zrobienia zdjęcia")  # Pole wyboru daty zdjęcia
        notatka = st.text_input(
            "Krótka notatka (np. 'Koniec redukcji', 'Początek masy')")  # Pole do wprowadzenia notatki
        plik_zdjecia = st.file_uploader("Wybierz plik ze zdjęciem",
                                        type=['png', 'jpg', 'jpeg'])  # Przycisk do przesyłania pliku graficznego

        if st.form_submit_button("Zapisz zdjęcie"):  # Przycisk do zapisywania zdjęcia
            if plik_zdjecia is not None:  # Jeśli plik został przesłany
                # Wczytuje obraz jako bajty i zapisuje w pamięci sesji
                st.session_state.historia_zdjec.append({  # Dodanie zdjęcia do listy w session_state
                    "data": data_zdjecia,
                    "notatka": notatka,
                    "obraz": plik_zdjecia.getvalue()  # Zapisanie zawartości pliku
                })
                st.success("Zdjęcie zostało zapisane!")  # Komunikat jesli sie udało
            else:
                st.warning("Nie wybrano żadnego pliku ze zdjęciem.")  # Komunikat ostrzegawczy

    st.write("---")
    st.subheader("Galeria Twoich Postępów")

    if st.session_state.historia_zdjec:  # Jeśli istnieją zapisane zdjęcia
        # Sortowanie zdjęć od najnowszych do najstarszych
        posortowane_zdjecia = sorted(st.session_state.historia_zdjec, key=lambda x: x['data'],
                                     reverse=True)  # Sortowanie zdjęć po dacie

        # Tworzymy galerię w 3 kolumnach
        for i in range(0, len(posortowane_zdjecia), 3):  # Iteracja co 3 zdjęcia
            cols = st.columns(3)  # Tworzenie 3 kolumn
            for j in range(3):  # Iteracja przez kolumny
                if i + j < len(posortowane_zdjecia):  # Sprawdzenie, czy indeks nie wykracza poza listę
                    with cols[j]:  # Umieszczenie zdjęcia w bieżącej kolumnie
                        zdjecie = posortowane_zdjecia[i + j]  # Pobranie zdjęcia
                        st.image(zdjecie["obraz"],  # Wyświetlenie obrazu
                                 caption=f"{zdjecie['data'].strftime('%Y-%m-%d')} - {zdjecie['notatka']}")  # Dodanie podpisu

        if st.button("🗑️ Wyczyść całą historię zdjęć"):  # Przycisk do czyszczenia historii zdjęć
            st.session_state.historia_zdjec = []  # Usunięcie wszystkich zdjęć z session_state
            st.rerun()  # Odświeżenie strony
    else:
        st.warning(
            "Brak zapisanych zdjęć. Dodaj swoje pierwsze zdjęcie, aby rozpocząć!")  # Komunikat jeśli brakuje zdjęć