import streamlit as st
import math
import pandas as pd
from datetime import datetime

# Konfiguracja strony (tytuł w zakładce przeglądarki i ikona)
st.set_page_config(page_title="Asystent Siłowni", page_icon="🏋️", layout="wide")

# --- GŁÓWNY TYTUŁ APLIKACJI ---
st.title("🏋️ Twój Osobisty Asystent Siłowni")
st.write("Wszystkie narzędzia, których potrzebujesz, w jednym miejscu!")

# --- TWORZENIE ZAKŁADEK ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Kalkulator BMI",
    "🔥 Kalkulator Kalorii (TDEE)",
    "💪 Kalkulator Poziomu Tłuszczu",
    "🎬 Biblioteka Ćwiczeń",
    "📈 Dziennik Postępów"
])


# --- ZAKŁADKA 1: KALKULATOR BMI (bez zmian) ---
with tab1:
    st.header("Kalkulator Wskaźnika Masy Ciała (BMI)")
    st.write("Wprowadź swoje dane, aby obliczyć wskaźnik BMI.")
    waga_bmi = st.number_input("Twoja waga (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5)
    wzrost_bmi = st.number_input("Twój wzrost (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0)
    if st.button("Oblicz moje BMI"):
        if wzrost_bmi > 0:
            wzrost_m = wzrost_bmi / 100
            bmi = waga_bmi / (wzrost_m ** 2)
            st.metric(label="Twoje BMI wynosi", value=f"{bmi:.2f}")
            if bmi < 18.5: st.warning("Masz niedowagę.")
            elif 18.5 <= bmi < 25: st.success("Twoja waga jest w normie.")
            elif 25 <= bmi < 30: st.warning("Masz nadwagę.")
            else: st.error("Jesteś w grupie ryzyka otyłości.")
        else: st.error("Wzrost musi być większy od zera.")


# --- ZAKŁADKA 2: KALKULATOR KALORII (TDEE) (bez zmian) ---
with tab2:
    st.header("Kalkulator Całkowitego Dziennego Zapotrzebowania Kalorycznego (TDEE)")
    st.info("TDEE to szacunkowa liczba kalorii, jaką spalasz w ciągu dnia, uwzględniając aktywność fizyczną.")
    plec_tdee = st.radio("Wybierz płeć", ("Mężczyzna", "Kobieta"))
    waga_tdee = st.number_input("Waga (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5, key="waga_tdee")
    wzrost_tdee = st.number_input("Wzrost (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0, key="wzrost_tdee")
    wiek_tdee = st.number_input("Wiek (lata)", min_value=15, max_value=100, value=30, step=1)
    poziom_aktywnosci = st.selectbox(
        "Poziom aktywności fizycznej",
        ("Siedzący tryb życia (brak lub minimalna aktywność)", "Lekka aktywność (ćwiczenia 1-3 dni w tygodniu)", "Umiarkowana aktywność (ćwiczenia 3-5 dni w tygodniu)", "Wysoka aktywność (ćwiczenia 6-7 dni w tygodniu)", "Bardzo wysoka aktywność (ciężka praca fizyczna lub intensywne ćwiczenia codziennie)")
    )
    mnozniki = {"Siedzący tryb życia (brak lub minimalna aktywność)": 1.2, "Lekka aktywność (ćwiczenia 1-3 dni w tygodniu)": 1.375, "Umiarkowana aktywność (ćwiczenia 3-5 dni w tygodniu)": 1.55, "Wysoka aktywność (ćwiczenia 6-7 dni w tygodniu)": 1.725, "Bardzo wysoka aktywność (ciężka praca fizyczna lub intensywne ćwiczenia codziennie)": 1.9}
    if st.button("Oblicz moje zapotrzebowanie kaloryczne"):
        if plec_tdee == "Mężczyzna": bmr = (10 * waga_tdee) + (6.25 * wzrost_tdee) - (5 * wiek_tdee) + 5
        else: bmr = (10 * waga_tdee) + (6.25 * wzrost_tdee) - (5 * wiek_tdee) - 161
        tdee = bmr * mnozniki[poziom_aktywnosci]
        st.success(f"Twoja podstawowa przemiana materii (BMR) wynosi: **{bmr:.0f} kcal**")
        st.success(f"Twoje całkowite dzienne zapotrzebowanie (TDEE) wynosi: **{tdee:.0f} kcal**")
        st.markdown(f"""---
* **Aby utrzymać wagę:** spożywaj ok. **{tdee:.0f} kcal**.
* **Aby schudnąć (deficyt):** spożywaj ok. **{tdee - 400:.0f} kcal**.
* **Aby przytyć (nadwyżka):** spożywaj ok. **{tdee + 400:.0f} kcal**.""")


# --- ZAKŁADKA 3: KALKULATOR POZIOMU TŁUSZCZU (bez zmian) ---
with tab3:
    st.header("Kalkulator Procentowej Zawartości Tkanki Tłuszczowej")
    st.warning("To jest szacunkowe obliczenie oparte na formule US Navy. Nie zastąpi profesjonalnego pomiaru.")
    plec_bf = st.radio("Wybierz płeć", ("Mężczyzna", "Kobieta"), key="plec_bf")
    wzrost_bf = st.number_input("Wzrost (cm)", min_value=100.0, value=175.0, step=1.0, key="wzrost_bf")
    obwod_szyi = st.number_input("Obwód szyi (cm)", min_value=20.0, value=40.0, step=0.5)
    obwod_talii = st.number_input("Obwód talii (cm)", min_value=50.0, value=80.0, step=0.5)
    if plec_bf == "Kobieta": obwod_bioder = st.number_input("Obwód bioder (cm)", min_value=60.0, value=95.0, step=0.5)
    if st.button("Oblicz poziom tłuszczu"):
        body_fat = 0
        try:
            if plec_bf == "Mężczyzna": body_fat = 495 / (1.0324 - 0.19077 * math.log10(obwod_talii - obwod_szyi) + 0.15456 * math.log10(wzrost_bf)) - 450
            else: body_fat = 495 / (1.29579 - 0.35004 * math.log10(obwod_talii + obwod_bioder - obwod_szyi) + 0.22100 * math.log10(wzrost_bf)) - 450
            st.metric(label="Szacowany poziom tkanki tłuszczowej", value=f"{body_fat:.1f}%")
        except ValueError: st.error("Wprowadzone wymiary są nieprawidłowe.")


# --- ZAKŁADKA 4: BIBLIOTEKA ĆWICZEŃ (ZMIENIONA LOGIKA) ---
with tab4:
    st.header("🎬 Biblioteka Ćwiczeń")
    st.info("Wybierz partię mięśniową, a następnie ćwiczenie, aby zobaczyć instruktaż wideo.")

    # NOWA, ZAGNIEŻDŻONA STRUKTURA DANYCH Z KATEGORIAMI
    cwiczenia_kategorie = {
        "Klatka piersiowa": {
            "Wyciskanie sztangi na ławce płaskiej": "https://www.youtube.com/watch?v=vcBig73ojpE",
            "Wyciskanie hantli na ławce skośnej": "http://googleusercontent.