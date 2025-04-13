import streamlit as st
from datetime import datetime
import math

st.title("🧪 Calculadora de Radiofármacos")

tabs = st.tabs(["Volume da Nanopartícula", "Atividade 99mTc"])

# === ABA 1: VOLUME NANO ===
with tabs[0]:
    st.header("Volume da Nanopartícula")
    conc = st.number_input("Concentração da nanopartícula (mg/mL)", min_value=0.0, step=0.01)
    massa = st.number_input("Massa desejada por animal (mg)", min_value=0.0, step=0.01)
    volume_final = st.number_input("Volume final por animal (µL)", min_value=0.0, step=1.0)

    if st.button("Calcular Volume", key="btn_nano"):
        if conc > 0:
            conc_mg_por_uL = conc / 1000
            volume_nano_uL = massa / conc_mg_por_uL
            volume_agua_uL = volume_final - volume_nano_uL

            st.success(f"Pipetar **{volume_nano_uL:.2f} µL** da nanopartícula")
            st.info(f"Completar com **{volume_agua_uL:.2f} µL** de salina/água")
        else:
            st.error("A concentração precisa ser maior que zero.")

# === ABA 2: ATIVIDADE ===
with tabs[1]:
    st.header("Cálculo da Atividade 99mTc")

    A0 = st.number_input("Atividade inicial (µCi)", min_value=0.0)
    hora_inicio = st.text_input("Horário da atividade inicial (ex: 13:30)")
    hora_injecao = st.text_input("Horário da injeção (ex: 14:00)")
    V_tec = st.number_input("Volume de 99mTc (µL)", min_value=0.0)
    V_sncl2 = st.number_input("Volume de SnCl2 (µL)", min_value=0.0)
    V_tec_usado = st.number_input("Volume da solução reduzida usada (µL)", min_value=0.0)
    V_nano = st.number_input("Volume da nanopartícula (µL)", min_value=0.0)
    V_salina = st.number_input("Volume de salina (µL)", min_value=0.0)
    n_animais = st.number_input("Número de animais", min_value=1, step=1)

    if st.button("Calcular Atividade", key="btn_atividade"):
        try:
            t0 = datetime.strptime(hora_inicio, "%H:%M")
            t1 = datetime.strptime(hora_injecao, "%H:%M")
            t = (t1 - t0).seconds / 3600
            T12 = 6.01
            lamb = math.log(2) / T12

            At = A0 * math.exp(-lamb * t)
            A_reduzida_total = At * (V_tec / (V_tec + V_sncl2))
            A_usada = A_reduzida_total * (V_tec_usado / (V_tec + V_sncl2))
            V_final = V_tec_usado + V_nano + V_salina
            A_final = A_usada * (V_tec_usado / V_final)
            A_por_animal = A_final / n_animais
            V_por_animal = V_final / n_animais

            st.success(f"Tempo decorrido: {t:.2f} horas")
            st.info(f"Atividade após decaimento: {At:.2f} µCi")
            st.info(f"Atividade total reduzida: {A_reduzida_total:.2f} µCi")
            st.info(f"Atividade usada na marcação: {A_usada:.2f} µCi")
            st.success(f"Atividade final: {A_final:.2f} µCi")
            st.success(f"Atividade por animal: {A_por_animal:.2f} µCi")
            st.info(f"Volume por animal: {V_por_animal:.2f} µL")
        except Exception as e:
            st.error(f"Erro: {e}")
