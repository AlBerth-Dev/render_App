import pandas as pd
import scipy.stats
import streamlit as st
import time

# estas son variables de estado que se conservan cuando Streamlit vuelve a ejecutar este script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0 # variable para el número de experimento

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

chart = st.line_chart([0.5]) # Implementamos la gráfica que mostrará la probabilidad 

def toss_coin(n): # función que emula el lanzamiento de una moneda

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no +=1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])    # Actualizamos la gráfica de probabilidaad
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10) # Slider para seleccionar # de lanzamientos
start_button = st.button('Ejecutar')

if start_button:        # Ejecutamos el experimento
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    mean = toss_coin(number_of_trials) # Lanzamos las monedas     

    # Usamos las variables de estado para mostrar el DataFrame después de cada ejecución de la aplicación
    st.session_state['experiment_no'] += 1
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                            columns=['no', 'iteraciones', 'media'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = \
        st.session_state['df_experiment_results'].reset_index(drop = True)

st.session_state['df_experiment_results'].index.name = 'Experimento'
st.write(st.session_state['df_experiment_results'][['no','iteraciones', 'media']]) # Mostramos la tabla final

