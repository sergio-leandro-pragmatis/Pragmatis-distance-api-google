import googlemaps
import pandas as pd
from streamlit import cli as stcli
import pandas as pd
import streamlit as st
import numpy as np
import sys
from PIL import Image


api_key = 'AIzaSyBz6KWncEdc8LNhpBI9XmdQ973h9a6-hCY'
gmaps = googlemaps.Client(key='AIzaSyBz6KWncEdc8LNhpBI9XmdQ973h9a6-hCY')


def API_matrix_distance(locais):



    origem = locais['locais_origem']
    origem = [x for x in origem if pd.isnull(x) == False]
    destino = locais['locais_destino']
    destino = [x for x in destino if pd.isnull(x) == False]
    origem_id = locais['id_origem']
    origem_id = [x for x in origem_id if pd.isnull(x) == False]
    destino_id = locais['id_destino']
    destino_id = [x for x in destino_id if pd.isnull(x) == False]
    colunas = ['ID_ORIGEM', 'L_ORIGEM','ID_DESTINO', 'L_DESTINO','DISTANCIA','DURACAO']
    matriz = pd.DataFrame(columns=colunas)

    info_distance = []
    info_duration = []
    matrix_distance = [[0] * len(destino)] * len(origem)
    matrix_time = [[0] * len(destino)] * len(origem)

    for i in range(len(origem)):
        for j in range(len(origem)):
            if origem[i] == destino[j]:
                distancia = 0
                duration = 0

            else:
                try:
                    consulta = gmaps.distance_matrix(origem[i], destino[j])
                    distancia = consulta['rows'][0]['elements'][0]['distance']['value']
                    duration = consulta['rows'][0]['elements'][0]['duration']['value']
                except:
                    distancia = ''
                    duration = ''

            info_distance.append(distancia)
            info_duration.append(duration)

        matrix_distance[i] = info_distance
        matrix_time[i] = info_duration

        info_distance, info_duration = [], []

    return np.array(matrix_distance),np.array(matrix_time), origem

def nearest_neighbor(instancia,start):
    size = len(instancia)
    instancia = np.array(instancia)
    import time
    ini = time.time()

    #vari??veis de controle:

    cost = 0
    num_ins = 0
    start_0 =start
    last_ins = start
    aux_1 = []
    solution = []
    cidades_nao_inseridas = []
    for i in range(size):
        cidades_nao_inseridas.append(i)
    while num_ins < size:
        for i in cidades_nao_inseridas:
            aux_1.append(instancia[last_ins, i])
            new_cost = min(aux_1)
        for i in cidades_nao_inseridas:
            if instancia[last_ins, i] ==new_cost:
                last_ins = i
                solution.append(last_ins)
                cost = cost + new_cost
                num_ins = num_ins + 1
        aux_1 = []
        aux_2 =[ ]
        cidades_nao_inseridas.remove(last_ins)
    solution.append(start_0)
    cost = cost + instancia[last_ins, start_0]
    fim = time.time()

    return(solution,cost,fim-ini )

def main():

    st.title("Pragmatis Consultoria - Squad Anaytics")
    
    foto = Image.open('logo_analytics.png')
    st.image(foto, caption='Squad Analytics', use_column_width=False)

    st.markdown('# Pragmatis Consultoria - Squad Analytics')
    st.markdown('## Roteirizador: caixeiro viajante pela heur??stica do vizinho mais pr??ximo')

    st.write('Ol??, seja bem vindo ao nosso roteirzador, em caso de bugs reporte para:sergio.campos@pragmatis.com.br')

    st.write('Por favor, realize abaixo o input dos dados para a busca:')

    input = st.file_uploader("Insira o input (.xlsx)", type ='xlsx')

    if input:
        df = pd.read_excel(input)
        st.table(df)

    use_API = st.button('Roteriza????o')

    matriz_distancia = []
    matriz_tempo = []

    key = 0
    tempo = 0
    distancia = 0

    if use_API:
        tempo_, distancia_, cidades = API_matrix_distance(df)

        st.markdown('## Resultados:')
        st.write('Matriz de Tempos:')
        tempodf = st.dataframe(tempo_)
        st.write('Matriz de Dist??ncias:')
        distanciadf = st.dataframe(distancia_)

        solution, cost, tempo= nearest_neighbor(distancia_, 0)
        solutiont, costt, tempot = nearest_neighbor(tempo_,0)

        cidades = cidades
        solution_ = []

        for i in solution:
            aux = cidades[i]
            solution_.append(aux)
        st.markdown('### Roteiriza????o por Distancia:')

        st.write('Rota Recomendada:', solution_)
        st.write(f'Dist??ncia Percorrida: { str(cost/1000)} KM')
        st.write('Tempo:', tempo)

        solution_ = []

        for i in solutiont:
            aux = cidades[i]
            solution_.append(aux)

        st.markdown('### Roteiriza????o por Tempo:')
        st.write('Rota Recomendada:', solution_)
        st.write('Dura????o do percurso (min):', costt)
        st.write('Tempo:', tempot)

if __name__ == '__main__':
        main()
