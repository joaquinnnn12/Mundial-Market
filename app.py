import streamlit as st
import os

# ==========================================
# 1. ESTRUCTURA DEL REGISTRO (Actualizado con Precio)
# ==========================================
class RegistroCamiseta:
    def __init__(self, id_registro, nya, pais_cam, liga, equipo, nom_jug, num_jug, vender, precio=0.0):
        self.id = id_registro
        self.nya = nya[:30]
        self.pais_cam = pais_cam[:30]
        self.liga = liga[:30]
        self.equipo = equipo[:30]
        self.nom_jug = nom_jug[:30]
        self.num_jug = int(num_jug)
        self.vender = bool(vender)
        self.precio = float(precio) # Nuevo campo: Precio (número decimal)

    def convertir_a_linea(self):
        # Agregamos el precio al final de la línea separado por '|'
        return f"{self.id}|{self.nya}|{self.pais_cam}|{self.liga}|{self.equipo}|{self.nom_jug}|{self.num_jug}|{self.vender}|{self.precio}\n"

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
                
                # Como quitamos la contraseña, los índices bajaron 1 posición
                es_venta = campos[7] == 'True'
                precio_guardado = float(campos[8]) if len(campos) > 8 else 0.0
                
                reg = RegistroCamiseta(
                    id_registro=campos[0], 
                    nya=campos[1], 
                    pais_cam=campos[2],
                    liga=campos[3], 
                    equipo=campos[4], 
                    nom_jug=campos[5], 
                    num_jug=int(campos[6]), 
                    vender=es_venta,
                    precio=precio_guardado # Pasamos el precio al registro
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
            # Si es venta mostramos el precio, si es intercambio no
            if reg.vender:
                tipo_operacion = f"💰 PARA VENTA (${reg.precio})"
            else:
                tipo_operacion = "🔄 PARA INTERCAMBIO"
                
            with st.container():
                st.subheader(f"{reg.equipo} - {reg.nom_jug} #{reg.num_jug}")
                st.write(f"**ID:** {reg.id} | **Liga:** {reg.liga} ({reg.pais_cam})")
                st.write(f"**Operación:** {tipo_operacion} | **Ofrecido por:** {reg.nya}")
                st.divider()

elif eleccion == "Publicar Camiseta":
    st.header("📝 Registrar nueva camiseta")
    
    with st.form("form_registro", clear_on_submit=True):
        st.write("Complete los datos de la camiseta:")
        nya = st.text_input("Nombre y Apellido (NyA)", max_chars=30)
        pais_cam = st.text_input("País del club (pais_cam)", max_chars=30)
        liga = st.text_input("Liga (liga)", max_chars=30)
        equipo = st.text_input("Nombre del equipo (equipo)", max_chars=30)
        nom_jug = st.text_input("Nombre del jugador (nom_jug)", max_chars=30)
        num_jug = st.number_input("Número del jugador", min_value=1, step=1)
        
        opc_vender = st.radio("¿Qué desea hacer?", ["Vender", "Intercambiar"])
        
        # CONDICIÓN: Si elige vender, le pedimos el precio. Si no, queda en 0.
        precio_venta = 0.0
        if opc_vender == "Vender":
            precio_venta = st.number_input("Precio de la camiseta ($)", min_value=0.0, step=1000.0)
        else:
            st.info("Al ser un intercambio, no se requiere precio.")
            
        submit = st.form_submit_button("Publicar Camiseta")
        
        if submit:
            if not nya or not equipo:
                st.error("Por favor complete los campos obligatorios (NyA, Equipo).")
            else:
                lista_actual = leer_desde_archivo()
                nuevo_id = str(len(lista_actual) + 1)
                vender_booleano = True if opc_vender == "Vender" else False
                
                nuevo_registro = RegistroCamiseta(
                    nuevo_id, nya, pais_cam, liga, equipo, nom_jug, num_jug, vender_booleano, precio_venta
                )
                guardar_en_archivo(nuevo_registro)
                st.success(f"¡Éxito! Camiseta publicada en el mercado con el ID: {nuevo_id}")
