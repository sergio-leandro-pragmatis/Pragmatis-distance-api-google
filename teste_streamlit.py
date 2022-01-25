import streamlit as st
import googlemaps
import pandas as pd
import sys
from streamlit import cli as stcli

import pandas as pd
from io import BytesIO
import streamlit as st

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def take_distance(local_A, local_B):
    api_key = 'AIzaSyBz6KWncEdc8LNhpBI9XmdQ973h9a6-hCY'
    # Requires API key
    gmaps = googlemaps.Client(key='AIzaSyBz6KWncEdc8LNhpBI9XmdQ973h9a6-hCY')

    # Requires cities name
    my_dist = gmaps.distance_matrix(local_A, local_B)['rows'][0]['elements'][0]

    distance = my_dist['distance']['text']
    duration = my_dist['duration']['text']

    #dados = pd.DataFrame(my_dist)
    #dados = dados.drop('status', axis = 1)[:1]

    return distance,duration

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

        distancia_ = []
        duracao_ = []
        origem_ = []
        destino_ = []
        id_list = []

        if input:
            df = pd.read_excel(input)
            st.table(df)

            origem = df['origem']
            destino = df['destino']

            st.subheader('Resultados:')

            for i in range(len(origem)):
                #st.write('Origem:', origem[i],'\nDestino:' ,destino[i])
                distancia, duracao = take_distance(origem[i], destino[i])


                distancia_.append(distancia)
                duracao_.append(duracao)
                origem_.append(origem[i])
                destino_.append(destino[i])
                id_list.append(f'000{str(i)}GMDP')

            dados_extract = {'id': id_list, 'Origem': origem_, 'Destino':destino_, 'Distância':distancia_, 'Duração':duracao_ }

            df_results = pd.DataFrame(dados_extract)

            st.table(dados_extract)

            st.download_button(label = "📥 Download Current Result as CSV", data = df_results.to_csv(), mime = 'text/csv',file_name='Output.csv')

if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
