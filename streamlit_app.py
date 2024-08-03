import streamlit as st
import os
import json
import requests

st.title(" 🎈Music-Api🎈")
st.write(
    "Comienza buscando un autor y una cancion!"
)

# Directorio donde se encuentran los archivos JSON
json_dir = 'json_autores'

# Función para cargar autores desde los archivos JSON
def load_autores_from_json(json_dir):
    autores = {}
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(json_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for entry in data:
                    if 'Nombre' in entry:
                        # Actualiza el diccionario con el autor y su URL
                        autores[entry['Nombre'].replace('Acordes', '')] = entry.get('url', 'URL no disponible')
    return autores

# Función para cargar canciones desde la API
def load_canciones(autor):
    url = f"https://mailernode.onrender.com/scrapCanciones?autor={autor}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Asumiendo que el JSON contiene una lista de canciones con un campo 'nombre' y 'url'
        return [{'nombre': cancion['nombre'].replace('acordes', ''), 'url': cancion['url']} for cancion in data]
    else:
        st.error(f"Error al obtener canciones para el autor {autor} (HTTP {response.status_code})")
        return []

def load_ruta_autor_cancion(autor, cancion):
    url = f"https://mailernode.onrender.com/scrapAcordesCanciones?autor={autor}&cancion={cancion}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Asumiendo que el JSON contiene una lista de canciones con un campo 'nombre' y 'url'
        return {'nombre': data['nombre'],
                'autor' : data['autor'],
                'tonalidad': data['tonalidad'],
                'body': data['body'],
                'bodyCompleto': data['bodyCompleto']

                }
    else:
        st.error(f"Error al obtener cancion para el autor {autor} (HTTP {response.status_code})")
        return {}
# Cargar autores desde los archivos JSON
autores = load_autores_from_json(json_dir)
autor_url =''
cancion_url=''
# Filtrar opciones según el texto ingresado
filtered_autores = list(autores.keys())

# Añadir un selectbox con las opciones filtradas para autores
if filtered_autores:
    autor = st.selectbox('Selecciona un autor:', filtered_autores)
    st.write('Has seleccionado el autor:', autor)
    
    if autor:
        # Cargar canciones para el autor seleccionado
        autor_url = autores[autor]
        filtered_canciones = load_canciones(autores[autor])

else:
    st.write("No hay autores disponibles para el filtro actual.")

# Añadir un selectbox con las opciones filtradas para canciones
if filtered_canciones:
    nombres_canciones = [cancion['nombre'] for cancion in filtered_canciones]
    cancion_seleccionada = st.selectbox('Selecciona una canción:', nombres_canciones)
    
    # Obtener la URL de la canción seleccionada
    url_cancion = next((cancion['url'] for cancion in filtered_canciones if cancion['nombre'] == cancion_seleccionada), None)
    
    st.write('Has seleccionado la canción:', cancion_seleccionada)
    if url_cancion:
        cancion_url = url_cancion
        st.text('Tonalidad: '+load_ruta_autor_cancion(autor_url, cancion_url)['tonalidad']['fundamental'])
        st.text('Tonalidad Relativa Menor:'+ load_ruta_autor_cancion(autor_url, cancion_url)['tonalidad']['relativaMenor'])

        st.text(load_ruta_autor_cancion(autor_url, cancion_url)['bodyCompleto'])

    else:
        st.write("URL no disponible para la canción seleccionada.")
else:
    st.write("No hay canciones disponibles para el filtro actual.")
