import streamlit as st
import math
import pandas as pd
from datetime import datetime
import io

# --- POPRAWIONA KOLEJNOŚĆ ---

# 1. Konfiguracja strony MUSI BYĆ PIERWSZĄ komendą Streamlit w skrypcie.
st.set_page_config(page_title="Asystent Siłowni", page_icon="🏋️", layout="wide")

# 2. Dodatkowy CSS i inne komendy Streamlit mogą iść DOPIERO PO konfiguracji strony.
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://sdmntprukwest.oaiusercontent.com/files/00000000-3974-6243-850f-d898216b4a22/raw?se=2025-06-12T23%3A26%3A08Z&sp=r&sv=2024-08-04&sr=b&scid=8708d40a-d7cf-5e55-91d5-7ae32dd8e264&skoid=b32d65cd-c8f1-46fb-90df-c208671889d4&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-06-12T06%3A50%3A26Z&ske=2025-06-13T06%3A50%3A26Z&sks=b&skv=2024-08-04&sig=MoXxxXryXzHUSrLexIq%2Bkaf8G777R5osHTCJ7PYmPE4%3D");
    background-size: cover;
    background-position: fixed;
    background-repeat: no-repeat;
    background-attachment: fixed;r
}

[data-testid="stHeader"] {{
    background-color: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
    right: 2rem;
}}

/* Poprawa czytelności na tle obrazka */
div.st-emotion-cache-16txtl3 {{
    background-color: rgba(28, 30, 38, 0.8); /* Półprzezroczyste tło dla kontenerów */
    padding: 1rem;
    border-radius: 0.5rem;
}}
.st-emotion-cache-1avcm0n{{
    background-color: rgba(15, 17, 22, 0.9);
}}
</style>
""", unsafe_allow_html=True)

# --- Struktura danych (można ją przenieść do osobnego pliku w przyszłości) ---
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

# --- Inicjalizacja Session State (pamięci aplikacji) ---
# Uwaga: w twoim kodzie były duplikaty, zostawiłem jedną, poprawną wersję
if 'historia_pomiarow' not in st.session_state:
    st.session_state.historia_pomiarow = []
if 'historia_treningow' not in st.session_state:
    st.session_state.historia_treningow = []

# --- PASEK BOCZNY (SIDEBAR) - GŁÓWNA NAWIGACJA ---
with st.sidebar:
    st.title("🏋️ Asystent Siłowni")
    st.write("---")

    strona = st.radio(
        "Wybierz stronę:",
        ("Kalkulatory", "Biblioteka Ćwiczeń", "Dziennik Postępów", "Dziennik Treningowy")
    )
    st.write("---")
    st.info("Aplikacja stworzona w ramach projektu na studia. Wykorzystuje bibliotekę Streamlit.")

# --- GŁÓWNA CZĘŚĆ APLIKACJI (RENDEROWANIE WYBRANEJ STRONY) ---

# Strona 1: Kalkulatory
if strona == "Kalkulatory":
    st.header("Kalkulatory Fitness")
    st.info("Wybierz kalkulator z poniższych zakładek, aby oszacować swoje wskaźniki.")

    tab1, tab2, tab3 = st.tabs(["📊 Kalkulator BMI", "🔥 Kalkulator TDEE", "💪 Kalkulator Body Fat"])

    with tab1:
        st.subheader("Kalkulator Wskaźnika Masy Ciała (BMI)")
        waga_bmi = st.number_input("Twoja waga (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5)
        wzrost_bmi = st.number_input("Twój wzrost (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0)
        if st.button("Oblicz moje BMI"):
            if wzrost_bmi > 0:
                wzrost_m = wzrost_bmi / 100
                bmi = waga_bmi / (wzrost_m ** 2)
                st.metric(label="Twoje BMI wynosi", value=f"{bmi:.2f}")
                if bmi < 18.5:
                    st.warning("Masz niedowagę.")
                elif 18.5 <= bmi < 25:
                    st.success("Twoja waga jest w normie.")
                else:
                    st.warning("Masz nadwagę lub otyłość.")

    with tab2:
        st.subheader("Kalkulator Całkowitego Dziennego Zapotrzebowania Kalorycznego (TDEE)")
        plec_tdee = st.radio("Wybierz płeć", ("Mężczyzna", "Kobieta"))
        waga_tdee = st.number_input("Waga (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5, key="waga_tdee")
        wzrost_tdee = st.number_input("Wzrost (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0,
                                      key="wzrost_tdee")
        wiek_tdee = st.number_input("Wiek (lata)", min_value=15, max_value=100, value=30, step=1)
        poziom_aktywnosci = st.selectbox("Poziom aktywności fizycznej",
                                         ("Siedzący tryb życia (brak lub minimalna aktywność)",
                                          "Lekka aktywność (ćwiczenia 1-3 dni w tygodniu)",
                                          "Umiarkowana aktywność (ćwiczenia 3-5 dni w tygodniu)",
                                          "Wysoka aktywność (ćwiczenia 6-7 dni w tygodniu)",
                                          "Bardzo wysoka aktywność (ciężka praca fizyczna lub intensywne ćwiczenia codziennie)"))
        mnozniki = {"Siedzący tryb życia (brak lub minimalna aktywność)": 1.2,
                    "Lekka aktywność (ćwiczenia 1-3 dni w tygodniu)": 1.375,
                    "Umiarkowana aktywność (ćwiczenia 3-5 dni w tygodniu)": 1.55,
                    "Wysoka aktywność (ćwiczenia 6-7 dni w tygodniu)": 1.725,
                    "Bardzo wysoka aktywność (ciężka praca fizyczna lub intensywne ćwiczenia codziennie)": 1.9}
        if st.button("Oblicz moje zapotrzebowanie kaloryczne"):
            if plec_tdee == "Mężczyzna":
                bmr = (10 * waga_tdee) + (6.25 * wzrost_tdee) - (5 * wiek_tdee) + 5
            else:
                bmr = (10 * waga_tdee) + (6.25 * wzrost_tdee) - (5 * wiek_tdee) - 161
            tdee = bmr * mnozniki[poziom_aktywnosci]
            st.success(f"Twoje BMR: **{bmr:.0f} kcal** | Twoje TDEE: **{tdee:.0f} kcal**")

    with tab3:
        st.subheader("Kalkulator Procentowej Zawartości Tkanki Tłuszczowej")
        plec_bf = st.radio("Wybierz płeć", ("Mężczyzna", "Kobieta"), key="plec_bf")
        wzrost_bf = st.number_input("Wzrost (cm)", min_value=100.0, value=175.0, step=1.0, key="wzrost_bf")
        obwod_szyi = st.number_input("Obwód szyi (cm)", min_value=20.0, value=40.0, step=0.5)
        obwod_talii = st.number_input("Obwód talii (cm)", min_value=50.0, value=80.0, step=0.5)
        if plec_bf == "Kobieta": obwod_bioder = st.number_input("Obwód bioder (cm)", min_value=60.0, value=95.0,
                                                                step=0.5)
        if st.button("Oblicz poziom tłuszczu"):
            try:
                if plec_bf == "Mężczyzna":
                    body_fat = 495 / (1.0324 - 0.19077 * math.log10(obwod_talii - obwod_szyi) + 0.15456 * math.log10(
                        wzrost_bf)) - 450
                else:
                    body_fat = 495 / (1.29579 - 0.35004 * math.log10(
                        obwod_talii + obwod_bioder - obwod_szyi) + 0.22100 * math.log10(wzrost_bf)) - 450
                st.metric(label="Szacowany poziom tkanki tłuszczowej", value=f"{body_fat:.1f}%")
            except (ValueError, ZeroDivisionError):
                st.error("Wprowadzone wymiary są nieprawidłowe.")

# Strona 2: Biblioteka Ćwiczeń
elif strona == "Biblioteka Ćwiczeń":
    st.header("🎬 Biblioteka Ćwiczeń")
    st.info("Wybierz partię mięśniową, a następnie ćwiczenie, aby zobaczyć instruktaż wideo.")
    lista_kategorii = list(CWICZENIA_KATEGORIE.keys())
    wybrana_kategoria = st.selectbox("1. Wybierz partię mięśniową:", options=lista_kategorii)
    if wybrana_kategoria != "Wybierz kategorię...":
        lista_cwiczen_w_kategorii = list(CWICZENIA_KATEGORIE[wybrana_kategoria].keys())
        wybrane_cwiczenie = st.selectbox("2. Wybierz ćwiczenie:", options=lista_cwiczen_w_kategorii)
        if wybrane_cwiczenie:
            video_url = CWICZENIA_KATEGORIE[wybrana_kategoria][wybrane_cwiczenie]
            st.video(video_url)

# Strona 3: Dziennik Postępów
# Zmieniłem logikę na tę bardziej rozbudowaną, którą robiliśmy
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
        talia = c3.number_input("Talia", 40, 150, 80, 1)
        klatka = c4.number_input("Klatka piersiowa", 50, 200, 100, 1)
        biceps = c5.number_input("Biceps", 15, 60, 35, 1)

        submitted = st.form_submit_button("Zapisz pomiar")
        if submitted:
            nowy_pomiar = {
                "Data": data_pomiaru, "Waga (kg)": waga_pomiaru, "Talia (cm)": talia,
                "Klatka (cm)": klatka, "Biceps (cm)": biceps
            }
            st.session_state.historia_pomiarow.append(nowy_pomiar)
            st.success("Pomiar został pomyślnie zapisany!")

    st.write("---")
    st.subheader("📊 Historia i Wizualizacja")
    if st.session_state.historia_pomiarow:
        df = pd.DataFrame(st.session_state.historia_pomiarow)
        df['Data'] = pd.to_datetime(df['Data'])
        df = df.sort_values(by="Data").set_index('Data')

        st.write("**Wybierz pomiar do wizualizacji na wykresie:**")
        lista_pomiarow = ["Waga (kg)", "Talia (cm)", "Klatka (cm)", "Biceps (cm)"]
        wybrany_pomiar = st.selectbox("Pokaż wykres dla:", lista_pomiarow)

        st.line_chart(df[wybrany_pomiar])
        st.dataframe(df)

    # Starałem się zachować spójność z bardziej rozbudowaną wersją, którą omawialiśmy.
    # W Twoim kodzie było odwołanie do `historia_wagi`, które tu nie istnieje.
    # Zostawiam fragment do importu/eksportu, ale dostosowany do `historia_pomiarow`

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.historia_pomiarow:
            csv = pd.DataFrame(st.session_state.historia_pomiarow).to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Eksportuj do CSV", data=csv, file_name='moje_pomiary.csv', mime='text/csv')
    with col2:
        with st.expander("⬆️ Importuj dane z pliku CSV"):
            uploaded_file = st.file_uploader("Wybierz plik CSV", type="csv")
            if uploaded_file:
                # Logika importu...
                pass

# Strona 4: Dziennik Treningowy
elif strona == "Dziennik Treningowy":
    st.header("📓 Dziennik Treningowy")
    st.info("Zapisuj swoje treningi, aby śledzić postępy w sile i wytrzymałości.")

    with st.form("trening_form", clear_on_submit=True):
        st.subheader("Dodaj nowy wpis treningowy")
        data_treningu = st.date_input("Data treningu", datetime.now())
        lista_wszystkich_cwiczen = []
        for kat in CWICZENIA_KATEGORIE:
            if kat != "Wybierz kategorię...":
                lista_wszystkich_cwiczen.extend(list(CWICZENIA_KATEGORIE[kat].keys()))

        wybrane_cwiczenie_trening = st.selectbox("Wybierz ćwiczenie", sorted(lista_wszystkich_cwiczen))

        c1, c2, c3 = st.columns(3)
        ciezar = c1.number_input("Ciężar (kg)", min_value=0.0, step=0.5)
        serie = c2.number_input("Liczba serii", min_value=1, step=1)
        powtorzenia = c3.number_input("Liczba powtórzeń", min_value=1, step=1)

        submitted = st.form_submit_button("Zapisz trening")
        if submitted:
            st.session_state.historia_treningow.append({
                "Data": data_treningu,
                "Ćwiczenie": wybrane_cwiczenie_trening,
                "Ciężar (kg)": ciezar,
                "Serie": serie,
                "Powtórzenia": powtorzenia
            })
            st.success("Trening został zapisany!")

    st.write("---")
    st.subheader("Historia Twoich treningów")
    if st.session_state.historia_treningow:
        df_treningi = pd.DataFrame(st.session_state.historia_treningow)
        df_treningi["Data"] = pd.to_datetime(df_treningi["Data"])
        st.dataframe(df_treningi.sort_values(by="Data", ascending=False).set_index("Data"))
    else:
        st.warning("Brak zapisanych treningów.")