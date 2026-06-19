import streamlit as st
import os

# ==========================================
# 1. ESTRUCTURA DEL REGISTRO (Igual que antes)
# ==========================================
class RegistroCamiseta:
    def __init__(self, id_registro, nya, contra, pais_cam, liga, equipo, nom_jug, num_jug, vender):
        self.id = id_registro
        self.nya = nya[:30]
        self.contra = contra[:8]
        self.pais_cam = pais_cam[:30]
        self.liga = liga[:30]
        self.equipo = equipo[:30]
        self.nom_jug = nom_jug[:30]
        self.num_jug = int(num_jug)
        self.vender = bool(vender)

    def convertir_a_linea(self):
        return f"{self.id}|{self.nya}|{self.contra}|{self.pais_cam}|{self.liga}|{self.equipo}|{self.nom_jug}|{self.num_jug}|{self.vender}\n"

# ==========================================
# 2. OPERACIONES CON EL ARCHIVO .TXT
# ==========================================
def guardar_en_archivo(registro, nombre_archivo="mundial_market.txt"):
    with open(nombre_archivo, "a", encoding="utf-8") as archivo:
        archivo.write(registro.convertir_a_linea())

def leer_desde_archivo(nombre_archivo="mundial_market.txt"):
    registros = []
    if not os.path.exists(nombre_archivo):
        return registros
        
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                campos = linea.split('|')
                es_venta = campos[8] == 'True'
                reg = RegistroCamiseta(
                    id_registro=campos[0], nya=campos[1], contra=campos[2], pais_cam=campos[3],
                    liga=campos[4], equipo=campos[5], nom_jug=campos[6], num_jug=int(campos[7]), vender=es_venta
                )
                registros.append(reg)
    return registros

# ==========================================
# 3. INTERFAZ WEB (STREAMLIT)
# ==========================================
# Configuración de la página
st.set_page_config(page_title="MundialMarket", page_icon="⚽")

st.title("⚽ MundialMarket")
st.write("Marketplace para vender o intercambiar objetos de colección (Camisetas de Clubes).")

# Menú lateral
menu = ["Ver Mercado", "Publicar Camiseta"]
eleccion = st.sidebar.selectbox("Menú de Opciones", menu)

if eleccion == "Ver Mercado":
    st.header("🛒 Mercado Actual")
    registros = leer_desde_archivo()
    
    if not registros:
        st.info("No hay camisetas registradas actualmente en MundialMarket.")
    else:
        for reg in registros:
            tipo_operacion = "💰 PARA VENTA" if reg.vender else "🔄 PARA INTERCAMBIO"
            # Usamos cajitas de Streamlit para que se vea lindo
            with st.container():
                st.subheader(f"{reg.equipo} - {reg.nom_jug} #{reg.num_jug}")
                st.write(f"**ID:** {reg.id} | **Liga:** {reg.liga} ({reg.pais_cam})")
                st.write(f"**Operación:** {tipo_operacion} | **Ofrecido por:** {reg.nya}")
                st.divider()

elif eleccion == "Publicar Camiseta":
    st.header("📝 Registrar nueva camiseta")
    
    # Formulario web
    with st.form("form_registro", clear_on_submit=True):
        st.write("Complete los datos de la camiseta:")
        nya = st.text_input("Nombre y Apellido (NyA)", max_chars=30)
        contra = st.text_input("Contraseña", max_chars=8, type="password")
        pais_cam = st.text_input("País del club (pais_cam)", max_chars=30)
        liga = st.text_input("Liga (liga)", max_chars=30)
        equipo = st.text_input("Nombre del equipo (equipo)", max_chars=30)
        nom_jug = st.text_input("Nombre del jugador (nom_jug)", max_chars=30)
        num_jug = st.number_input("Número del jugador", min_value=1, step=1)
        
        opc_vender = st.radio("¿Qué desea hacer?", ["Vender", "Intercambiar"])
        
        # Botón de envío
        submit = st.form_submit_button("Publicar Camiseta")
        
        if submit:
            if not nya or not contra or not equipo:
                st.error("Por favor complete los campos obligatorios (NyA, Contraseña, Equipo).")
            else:
                lista_actual = leer_desde_archivo()
                nuevo_id = str(len(lista_actual) + 1)
                vender_booleano = True if opc_vender == "Vender" else False
                
                nuevo_registro = RegistroCamiseta(
                    nuevo_id, nya, contra, pais_cam, liga, equipo, nom_jug, num_jug, vender_booleano
                )
                guardar_en_archivo(nuevo_registro)
                st.success(f"¡Éxito! Camiseta publicada en el mercado con el ID: {nuevo_id}")