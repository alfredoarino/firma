import streamlit as st
import os
import base64
import pandas as pd

# Credenciales (puedes cambiar estas credenciales o usar una fuente más segura)
USERNAME = "admin"
PASSWORD = "password"


# Función para la autenticación
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD


# Estado inicial de sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Página de inicio de sesión
if not st.session_state.authenticated:
    st.title("Inicio de Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar Sesión"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success("Inicio de sesión exitoso. Cargando documentos...")
            st.rerun()  # Recargar para mostrar la página principal
        else:
            st.error("Usuario o contraseña incorrectos.")
else:
    # Página principal (lista de PDF)
    st.title("Visor de PDF desde un Directorio")

    # Ruta del directorio con los PDFs (puedes cambiar esta ruta)
    pdf_directory = r"K:\LABORAL\Kilometraje\Año 2024\Diciembre 24"

    # Obtener lista de archivos PDF en el directorio
    if os.path.exists(pdf_directory):
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]
    else:
        st.error(f"El directorio '{pdf_directory}' no existe.")
        pdf_files = []

    # Si hay archivos PDF, mostrar tabla y permitir selección
    if pdf_files:
        # Crear un DataFrame para mostrar en una tabla
        df = pd.DataFrame({"Archivos PDF": pdf_files})

        st.sidebar.subheader("Selecciona un archivo PDF de la lista")

        # Mostrar la tabla de archivos
        selected_index = st.sidebar.radio(
            "Archivos disponibles:",
            options=list(range(len(pdf_files))),
            format_func=lambda x: pdf_files[x]
        )

        # Archivo seleccionado
        selected_pdf = pdf_files[selected_index]

        # Ruta completa del PDF seleccionado
        pdf_path = os.path.join(pdf_directory, selected_pdf)

        # Mostrar visor de PDF
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
            pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
            pdf_display = f'data:application/pdf;base64,{pdf_base64}#toolbar=0'

            st.markdown(
                f"""
                <iframe src="{pdf_display}" width="1000" height="800" style="border: none;"></iframe>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.warning("No se encontraron archivos PDF en el directorio especificado.")

    # Opción para cerrar sesión
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()
