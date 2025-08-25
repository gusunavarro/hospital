import streamlit as st
from datetime import datetime
import json  # Esta biblioteca nos ayuda a guardar y leer archivos
import os  # Nos ayuda a trabajar con archivos y carpetas

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Medicamentos Hospitalarios",
    page_icon="💊",
    layout="wide"
)

# Nombre del archivo donde guardaremos los datos
ARCHIVO_DATOS = "medicamentos.json"


# FUNCIÓN PARA GUARDAR LOS DATOS EN EL ARCHIVO
def guardar_medicamentos():
    """
    Esta función toma todos los medicamentos de la memoria
    y los escribe en un archivo para que no se pierdan
    """
    try:
        with open(ARCHIVO_DATOS, 'w') as archivo:  # 'w' significa que vamos a escribir
            json.dump(st.session_state.medicamentos, archivo)  # Convertimos a JSON y guardamos
    except Exception as e:
        st.error(f"Error al guardar: {e}")


# FUNCIÓN PARA CARGAR LOS DATOS DESDE EL ARCHIVO
def cargar_medicamentos():
    """
    Esta función lee el archivo y carga los medicamentos a la memoria
    cuando abrimos la aplicación
    """
    try:
        if os.path.exists(ARCHIVO_DATOS):  # Si el archivo existe...
            with open(ARCHIVO_DATOS, 'r') as archivo:  # 'r' significa que vamos a leer
                return json.load(archivo)  # Convertimos de JSON a lista de Python
        else:
            return []  # Si el archivo no existe, devolvemos lista vacía
    except Exception as e:
        st.error(f"Error al cargar: {e}")
        return []


# Título de la aplicación
st.title("💊 Sistema de Ingreso de Medicamentos - DATOS PERMANENTES")
st.markdown("---")

# INICIALIZAMOS LOS MEDICAMENTOS
# Si es la primera vez que abrimos la página, cargamos desde el archivo
if 'medicamentos' not in st.session_state:
    st.session_state.medicamentos = cargar_medicamentos()  # ¡Cargamos los datos guardados!

# Sidebar para navegación
pagina = st.sidebar.selectbox(
    "Navegación:",
    ["🏠 Inicio", "➕ Ingresar Medicamento", "📋 Lista de Medicamentos", "🔍 Buscar Medicamento", "🗑️ Limpiar Datos"]
)

# --- PÁGINA DE INICIO ---
if pagina == "🏠 Inicio":
    st.header("Bienvenido al Sistema de Medicamentos")
    st.write("""
    **✨ NUEVA FUNCIONALIDAD:**
    - Los datos ahora se guardan permanentemente
    - No se pierden al cerrar el navegador
    - Se almacenan en un archivo seguro en tu computadora
    """)

    total_medicamentos = len(st.session_state.medicamentos)
    st.metric("Total de medicamentos registrados", total_medicamentos)

    if total_medicamentos > 0:
        ultimo_med = st.session_state.medicamentos[-1]
        st.info(f"Último medicamento registrado: **{ultimo_med['nombre']}**")

    # Mostramos información del archivo
    st.markdown("---")
    st.write("**📊 Información del almacenamiento:**")
    if os.path.exists(ARCHIVO_DATOS):
        tamaño = os.path.getsize(ARCHIVO_DATOS)  # Tamaño del archivo en bytes
        st.write(f"📁 Archivo de datos: `{ARCHIVO_DATOS}`")
        st.write(f"📏 Tamaño: {tamaño} bytes")
        st.write(f"💾 Medicamentos guardados: {total_medicamentos}")
    else:
        st.write("📁 Aún no se ha creado el archivo de datos")

# --- PÁGINA PARA INGRESAR MEDICAMENTOS ---
elif pagina == "➕ Ingresar Medicamento":
    st.header("Ingresar Nuevo Medicamento")

    with st.form("formulario_medicamento"):
        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre del medicamento:*", placeholder="Ej: Paracetamol")
            laboratorio = st.text_input("Laboratorio:", placeholder="Ej: Bayer")

        with col2:
            cantidad = st.number_input("Cantidad:*", min_value=1, value=1)
            lote = st.text_input("Número de lote:", placeholder="Ej: L12345")

        fecha_vencimiento = st.date_input("Fecha de vencimiento:")
        observaciones = st.text_area("Observaciones:", placeholder="Notas adicionales...")

        enviar = st.form_submit_button("💾 Guardar Medicamento")

        if enviar:
            if nombre and cantidad > 0:
                nuevo_medicamento = {
                    'nombre': nombre.upper(),
                    'laboratorio': laboratorio.upper() if laboratorio else "NO ESPECIFICADO",
                    'cantidad': cantidad,
                    'lote': lote.upper() if lote else "SIN LOTE",
                    'fecha_vencimiento': fecha_vencimiento.strftime(
                        "%d/%m/%Y") if fecha_vencimiento else "NO ESPECIFICADA",
                    'observaciones': observaciones,
                    'fecha_ingreso': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }

                # Agregamos el medicamento a la lista en memoria
                st.session_state.medicamentos.append(nuevo_medicamento)

                # ¡ESTA ES LA PARTE IMPORTANTE NUEVA!
                # Guardamos inmediatamente en el archivo
                guardar_medicamentos()  # Llamamos a la función que creamos

                st.success("✅ Medicamento registrado y GUARDADO PERMANENTEMENTE!")
                st.balloons()

                st.write("**Resumen del medicamento ingresado:**")
                st.json(nuevo_medicamento)

            else:
                st.warning("⚠️ Por favor completa al menos el nombre y la cantidad")

# --- PÁGINA PARA VER TODOS LOS MEDICAMENTOS ---
elif pagina == "📋 Lista de Medicamentos":
    st.header("Lista de Medicamentos Registrados")

    if not st.session_state.medicamentos:
        st.info("📝 No hay medicamentos registrados. Ve a 'Ingresar Medicamento' para agregar el primero.")
    else:
        total_medicamentos = len(st.session_state.medicamentos)
        total_unidades = sum(med['cantidad'] for med in st.session_state.medicamentos)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total medicamentos", total_medicamentos)
        col2.metric("Total unidades", total_unidades)
        col3.metric("💾 Guardado en", "ARCHIVO" if os.path.exists(ARCHIVO_DATOS) else "MEMORIA")

        st.subheader("Filtros")
        buscar_nombre = st.text_input("Buscar por nombre:", "").upper()

        if buscar_nombre:
            medicamentos_filtrados = [
                med for med in st.session_state.medicamentos
                if buscar_nombre in med['nombre']
            ]
        else:
            medicamentos_filtrados = st.session_state.medicamentos

        st.subheader(f"Medicamentos ({len(medicamentos_filtrados)})")

        for i, med in enumerate(medicamentos_filtrados):
            with st.expander(f"💊 {med['nombre']} - {med['cantidad']} unidades"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Laboratorio:** {med['laboratorio']}")
                    st.write(f"**Lote:** {med['lote']}")
                    st.write(f"**Cantidad:** {med['cantidad']}")

                with col2:
                    st.write(f"**Vencimiento:** {med['fecha_vencimiento']}")
                    st.write(f"**Ingresado:** {med['fecha_ingreso']}")
                    if med['observaciones']:
                        st.write(f"**Observaciones:** {med['observaciones']}")

                # Botón para eliminar con confirmación
                if st.button(f"❌ Eliminar este medicamento", key=f"eliminar_{i}"):
                    st.session_state.medicamentos.remove(med)
                    guardar_medicamentos()  # Guardamos los cambios en el archivo
                    st.rerun()  # Recargamos la página para ver los cambios

# --- PÁGINA PARA BUSCAR MEDICAMENTOS ---
elif pagina == "🔍 Buscar Medicamento":
    st.header("Buscar Medicamento")

    if not st.session_state.medicamentos:
        st.info("No hay medicamentos registrados para buscar.")
    else:
        termino_busqueda = st.text_input("🔍 Buscar medicamento por nombre:", "").upper()

        if termino_busqueda:
            resultados = [
                med for med in st.session_state.medicamentos
                if termino_busqueda in med['nombre']
            ]

            if resultados:
                st.success(f"✅ Se encontraron {len(resultados)} medicamento(s)")

                for med in resultados:
                    st.write(f"**💊 {med['nombre']}**")
                    st.write(f"Laboratorio: {med['laboratorio']}")
                    st.write(f"Cantidad: {med['cantidad']} unidades")
                    st.write(f"Lote: {med['lote']}")
                    st.write(f"Ingresado: {med['fecha_ingreso']}")
                    st.markdown("---")
            else:
                st.warning("❌ No se encontraron medicamentos con ese nombre")

# --- PÁGINA NUEVA: LIMPIAR DATOS ---
elif pagina == "🗑️ Limpiar Datos":
    st.header("Limpiar Base de Datos")
    st.warning("⚠️ ZONA DE PELIGRO - Estas acciones no se pueden deshacer")

    if st.button("🗑️ ELIMINAR TODOS LOS MEDICAMENTOS"):
        st.session_state.medicamentos = []  # Vaciamos la lista
        guardar_medicamentos()  # Guardamos la lista vacía
        st.success("✅ Todos los medicamentos han sido eliminados")
        st.rerun()

    st.markdown("---")
    st.write("**📊 Estado actual:**")
    st.write(f"Medicamentos registrados: {len(st.session_state.medicamentos)}")

    if os.path.exists(ARCHIVO_DATOS):
        st.write(f"📁 Archivo de datos: `{os.path.abspath(ARCHIVO_DATOS)}`")
        st.write(f"📏 Tamaño: {os.path.getsize(ARCHIVO_DATOS)} bytes")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("🏥 Sistema de Gestión de Medicamentos - Almacenamiento PERMANENTE en archivo JSON")
st.caption("💾 Los datos se guardan automáticamente y persisten después de cerrar el navegador")

# Información adicional sobre el archivo
if os.path.exists(ARCHIVO_DATOS):
    st.sidebar.info(f"📁 Archivo: {ARCHIVO_DATOS}")
    st.sidebar.info(f"📦 Medicamentos: {len(st.session_state.medicamentos)}")
