import streamlit as st
import googlemaps
import pandas as pd
import sys
from streamlit import cli as stcli
def take_distance(local_A, local_B):
    api_key = 'AIzaSyBz6KWncEdc8LNhpBI9XmdQ973h9a6-hCY'
    # Requires API key
    gmaps = googlemaps.Client(key='AIzaSyBz6KWncEdc8LNhpBI9XmdQ973h9a6-hCY')

    # Requires cities name
    my_dist = gmaps.distance_matrix(local_A, local_B)['rows'][0]['elements'][0]

    dados = pd.DataFrame(my_dist)
    dados = dados.drop('status', axis = 1)[:1]

    return dados

def main():
    st.title("Pragmatis Consultoria - Squad Anaytics")


    menu = ["Distance Matrix - Google API"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Distance Matrix - Google API":
        st.header("Distance Matrix - Google API")
        st.write(
            'Olá, seja bem vindo a nossa ferramenta de cálculo de distâncias e transportes por aplicativo.')
        st.write(
            "Para essa análise é necessário que o arquivo de input dos dados possua o formato abaixo, fique atendo ao cabeçalho das colunas esses não devem ser alterados:")

        input_template = {
            'Origem': ['São Paulo', 'Recife', 'Belém', 'Brasilia'],
            'Destino': ['Rio de Janeiro', 'Brasilia', 'São Paulo', 'Curitiba']}

        st.table(input_template)

        input = st.file_uploader("Insira o input (.xlsx)", type='xlsx')

        if input:
            df = pd.read_excel(input)
            st.table(df)

            origem = df['origem']
            destino = df['destino']

            for i in range(len(origem)):
                st.write('Origem:', origem[i],'\nDestino:' ,destino[i])
                st.table(take_distance(origem[i], destino[i]))


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())