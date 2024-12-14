import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail account credentials
gmail_user = 'myndiukmaria@gmail.com'
gmail_password = 'lpgg ronv vtgf nmpk'
email_subject = 'Confirmación de Turno'
email_from = gmail_user

# Título de la aplicación
st.title("Sistema de Asignación de Turnos")

# Lista de especialidades
especialidades = [
    "Cardiología", "Dermatología", "Ginecología", "Pediatría", "Oftalmología",
    "Neurología", "Psiquiatría", "Urología", "Oncología", "Endocrinología",
    "Gastroenterología", "Hematología", "Infectología", "Nefrología", "Neumología",
    "Reumatología", "Traumatología", "Otorrinolaringología", "Cirugía General", "Medicina Interna",
    "Clínica Médica", "Alergología", "Anestesiología", "Angiología", "Bioquímica Clínica",
    "Cirugía Cardiovascular", "Cirugía Plástica", "Cirugía Torácica", "Dermatología Pediátrica",
    "Endocrinología Pediátrica", "Geriatría", "Hepatología", "Inmunología", "Medicina del Deporte",
    "Medicina Familiar", "Medicina Nuclear", "Medicina Preventiva", "Neurocirugía", "Neurofisiología",
    "Nutrición", "Odontología", "Oncología Pediátrica", "Patología", "Pediatría Neonatal",
    "Radiología", "Radioterapia", "Toxicología", "Urgencias Médicas"
]

# Simulación de un sistema de login simple
user_type = st.sidebar.selectbox("Selecciona tu tipo de usuario", ["Paciente", "Hospital"])

if user_type == "Paciente":
    # Crear un formulario para solicitar turno
    with st.form("form_turno"):
        nombre = st.text_input("Nombre del paciente")
        email = st.text_input("Correo electrónico")
        telefono = st.text_input("Teléfono")
        especialidad = st.selectbox("Selecciona una especialidad", especialidades)
        fecha = st.date_input("Selecciona la fecha del turno")
        hora = st.time_input("Selecciona la hora del turno")
        submit = st.form_submit_button("Solicitar Turno")

    # Almacenar y mostrar los turnos solicitados
    if submit:
        turno = {"Nombre": nombre, "Correo": email, "Teléfono": telefono, "Especialidad": especialidad, "Fecha": fecha, "Hora": hora}
        st.write("Turno solicitado:")
        st.write(turno)

        # Guardar el turno en un DataFrame (puedes usar una base de datos en una aplicación real)
        if "turnos" not in st.session_state:
            st.session_state.turnos = []
        st.session_state.turnos.append(turno)

        # Enviar correo electrónico con los detalles del turno
        email_text = f"Hola {nombre}, tu turno para {especialidad} ha sido confirmado para el {fecha} a las {hora}. Teléfono de contacto: {telefono}."
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email
        msg['Subject'] = email_subject
        msg.attach(MIMEText(email_text, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            server.sendmail(email_from, email, text)
            server.quit()
            st.success("Turno solicitado y correo electrónico enviado.")
        except Exception as e:
            st.error(f"Error al enviar el correo electrónico: {e}")

    # Mostrar los turnos del paciente
    if "turnos" in st.session_state:
        st.write("Tus turnos solicitados:")
        df_turnos = pd.DataFrame(st.session_state.turnos)
        df_turnos_paciente = df_turnos[df_turnos["Nombre"] == nombre]
        st.write(df_turnos_paciente)

elif user_type == "Hospital":
    # Mostrar todos los turnos solicitados
    if "turnos" in st.session_state:
        st.write("Turnos solicitados:")
        df_turnos = pd.DataFrame(st.session_state.turnos)
        st.write(df_turnos)
    else:
        st.write("No hay turnos solicitados.")
