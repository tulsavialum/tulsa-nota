import streamlit as st
from fpdf import FPDF
import pandas as pd
import datetime
import os

# =========================================================
# CONFIGURACION
# =========================================================

st.set_page_config(
    page_title="TULSA - Nota de Servicio",
    page_icon="app/static/icon-192.png",
    layout="wide"
)

# ── PWA: manifest + meta tags (icono embebido base64) ──
_ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAYAAABS3GwHAAAABmJLR0QA/wD/AP+gvaeTAAASc0lEQVR4nO3dfZAU9Z3H8ffv1zM7M/vIrrIEUFlE2IUFFlwNIIhgDF6MQkTxkugl5jS5S+qqLiYmuUtVLknV5S45r9QkZV28itE8GE1EFEQFo9ED8ZFnll0WkefH3UXZ3WF3Hrr7d3/sLuzzEzvTC/19VVHlzvT099s9/en+zUx3q0iRUdMXZTU74WuNMldiVDFQDIwE8oEsICNVtcV5KQbUA6eU4pCBbQqzTdvW+lO7nt+fqqJqKGeWOXnpaEvbXwCWAp8EgkM5f+Fb2xXmBVzz24aq1R8M5YyHJADZpYsXKmXux6gbAWso5ilEN1yUWaNRD9dXrPrLUMzwnAKQNXnJDVqbHwPXDEUzQgzA61rr79TveH7TucxkUAGIlN08NpjUDxrFHedSXIhz5AKPhWy+XVe9qnEwMxhwALJLF39ewaNA7mAKCpEC+4zL3dGqVesG+sL+B6BoQTgnO+dhjPqHgRYRIg0c4LuNO1c9OJAX9SsA+eXL8uxY7HlQCwbTmRBpo8zjjSb8j+x8JtGvyfuaIHv6rYXacdYamHHu3QmRFqsb48nb2fNyvK8Je/3KMr98WR7J5Guy8YvzzKRQwCpPZI1+llP77d4m1D0+U7QgbMdiz8vGL85Tn8nNzv0d/KjnbZxejgA5Y6c/Auq2oe9LiLQpDRUeDSVqd7/W0wTdBqD1q87/TF1fQqSLmhcunLQ7Xru7ottnOz8QKbt5bMDWlcj3/OLC0aC1M7N+x4t7Oz/RZXwUTOoHkY1fXFhyXWM9ybJlXUY8HQKQNXnJDXJ6g7ggGWZnV8a6/IjbIQBamx+lrSEh0kyh/j17+q2F7R87E4Ds0sULgblp70qI9MnHcX7Q/oEzAVDK3J/+foRILwX3RspuHtv2t4aWK7kwapF3bQmRNmHL1md29hrAspJ3AgHPWhIijRR8ZUz5LZnQNgQy6nOediREeuVFm9WtAHpk6bJsWi5gF8I3jOIuAB0nMRe5e4Pwn+uYsyyijXLLve5ECA9EcutjC3TrTauE8B0X9UlNyx3bhPAdpdQ0DYzyuhEhvGFKNBg581P41UUaVLbXXQjhkXyN3KVZ+Feo1wuGhbjQSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCErw3Lm2GVTZnAz753L+XTJhLKkBtWnM9i8QTr3t3Bt37yKw4eqfG6nS5UTuli43UT7ZVNmcBrT/4XGcFhmU0xSB/XR5m37D4OHR1eIRh2Q6Cffe9e2fgvQPl52fzk/q943UYXwy4A5dMmet2CSJGFc8q8bqGLYRcAGfNfuPJysrxuoYthFwAh0kkCIHxNAiB8TQIgfE0CIHxNAiB8TQIgfE0CIHxNAiB8TQIgfG3YBcB1h9XJqWIIGTP83tthF4DqvYe8bkGkyPHaj71uoYthF4BH/7ja6xZEijyxfK3XLXRhhQqLf+R1E+1trdxLTlaEq8uKUUp53Y4YIivWvMm//uyxYTfEHXZXhLUpnzaR+Z+czojc4XcKbWf33XObJ3UfeuxZT+oOREO0ife27mL9+xVet9KtYRuA80lDxUpP6uZOXeJJ3QvJsPsMIEQ6SQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK9JAISvSQCEr0kAhK8FvG6gCyuAc8nlEAh63Um/vVpje1LXmVDqSd1BScSxjuwD1/G6kw5UTuli43UT7TV9+bvn1xsr+i1QtZnIUz/3uo0Oht0QyP3EZV63IFLEKSr2uoUuht0QKLz8UZJzFmEsy+tW+m3hnDJP6r7+9jZP6g6Gcl2CG//qdRtdDLsh0PmooWKlJ3Vzpy7xpO6FZNgNgc5H9Y2n014znkimveaFSAIwBN54J/1Dkfe3V6e95oVIAjAEvv/A43xcH01bvUTS5l9++uu01buQSQCGwKGjNcxbdh9r120kFk+krE48keTNjRVc/4X72b5rX8rq+Il8CBa+JkcA4WsSAOFrEgDhaxIA4WvenAqhi0gs+zx2lkLtXUH4jWpU++fVKJJL7iaZd5iM5X8kcLqbz+kXX0fs5mtwj68lsnYzqm2SwBTidy7BiW8m9Oe1WC4wfinNC4sxJLHWPUJoT3PbxDjzvkF8UhY4B1traZxrvkG8JIz1+sOE9iXP9lOgULueJvLW/tbXWzjzv0l8/PGzfWaVE799EU79BsIr16HPtG5hxl5Nsmw6TkEe0Iyq20tg23oCxxr7WGER7EX/RGL0HkJ/eA6ruxMqM6YQv2MJDpWE/rQS68zvZAoz7cs0Xz0KveUJwlvqelm+1v2hm0Q1fYw+UkFg20asaLuCbcvX/kwV10Y116E/eJOMrR+g3NbHxy+leeEk6LDOAJWFWzKPZMlE3NwwJBrRRysIbHkXqyG9Z9Z6E4Ci+SQnj4OTcZxZC3HeriYQb/e8CuGOLca5WOP21GHGSJyiElze6/i4ysEdV4LTdJS2VJmsMdjjWk7Ecq+cSsae91uesiZgXz0TZ4QCl9ZaCi6aiFOUicpSHfsZZcGYO0lU/5SMkw6gMYUTcYoyzvYZyMcpKsGpq26pbwAVxrn2Ppo/VYxxGtHHjqC4BGfWVSRn/w2BVx4k/Nb+jjuBDssUwBQW44xrwvQ0UfIg2r6MxOTRJMevwdrdukJVAcmr5uFcVoO1pq735StsRu/7EG0HMKNnkii9lsS1H5Lx54cI7Y12XD77ONaBEy096zDuuLnYU67FvuTnZL6wDWVa13tRCao262yfgTEkl91PrKQAYrVYJ05CQSmJkjkkrrmejKceJLQ/fb+sexCAEPb0q3BjW4msbST+xfkki3MIbO9rL3iuHHTdSdwJV+OE3m8J3Nhy7Lwo+qSFm9+PWZw+iQpNJLFoNsGnN5w96vTlkiXEri/GRDcRfvxRgnUtvxWYUTcQ+/Jd2Iu+SmL/DwkdPYe9n4kS2LIZNXkudmkxZvf2lo0zdwb2pQE4toHgMYde33L3MMHnHiKj3gBB3On30Lx0Nomld2D98jcdd1Kn3iX8xxXotr19zgKav3k39rTZOC9tI9Dtomjc2fcSKylA7VtO5KkXseKttab9Pc23zSGxdBnWI090rJVC6f8MECkjOTkHtesdrA/fJfBRBs7Mq3resw0VZdD7d6FDU0leEQEsnMkzcGNVWDX9XA1NG8l47xim5DbiE7P6nh5a6ky9Gle7WG/9+czGD6BO/JXQuwdBj8aeOm7Ai9SZ+vBNAvUGc8VVOEEAhSm+Cseysba+22441h9J9I6nyNiThJxy7KLeLlBSmNyLMRpoajw7BOoy2SjsqUVgThB89eXWjb+1VsWfyNhnQ1459rj0XQyV5gAoTMlcnHADgYoqlLOfQOUJzLhrSI5IdQKAY9sINIRxpkzFWOOwSy5GfbCp3Xi5D9rBevNPBBvySd74WZx+HT8DmLwRYJrRtSc7Peeia46hjMbkFwxsWbpj7ya44wRkz8AelwFqBPaUiZCoJLizc+1+MFF07SlQYdzcToEfuYimbz9M9DsPE/3uI0S/djOOe5zgK2taPnd1Rxfg5mpwj6PrOn2QMY3o2npQEdy8/u5czl16A6AKsMtKMWRi3/ITTn/zp8SuvKhlLD5tzCDn2fnvtnFtN7s7ew+BXR9jJpTjXFqOnd9EoLLqzEv6pWkbode3oy7+NPHZY1rG+L1yIZkEgphQ5z2bwoQiLbOID8Ux38Ha9haWycWeUozJmUHysgBqz4buv0jok8ZEwmAMKtlpLxE7hlW1mUBlBdqNADVk/P6HhHd+1PPsTByVMKDCmFDnla4xoTAYutZKofQGoGAWyXEB1NFNBCs3EajaRGD7O1iNCqdsDs5AummOtmzjeSNx27/uojEtf0fruzkU21iVW9DhKSQWzsRtriCwt7nzRH0wqK1Pk3EYnGvvwI70de6PjXXgQxQZOFOv7DjUUyOwS68A4lj7Dwywjx7Uvk3goI2ZVI5dUo5rNRDYsrX/n1fay5yGPTEb3INYhzqtp8YdhF76HeEXHyPy8vsoCkkunI/b287EPYJ1pAn05dilozo+FynFnpAJzoGutVIojR+CNe70OTi6ieC6JwhVxc604OhSmmbNwr50JdaBdulXYcyo8ThZ7d+9ZvTx46hT2wkcux1n7EJit9QR2noQFSkiueBGXJXAqtjU/Zj30HsEGj5FYnwuatuzWHEY8GXa7jGCa14lec9nSF7h9nEUMKgdqwnOKSFR8iWabssntGU3igKcGbeQmJSJOraKjJ31A+2ih3J1BLdWkVg8g8TcLEz9OoJ7+3l0ObO+FeRdTnL+rSSzDXrLKoIf9TSuMajK5YT2Tid2+eeIz9hMZEtPw61mAutfwpq0DOeGb9EcXklwby0qcxzJuUtI5rjojc/3UmvopS8A1niS08ZCYjOB/e3fEBuregdq1gKSZSVkHNhxdlSji0jc9UM67GPtnYQffoBgw1Eylv8vZuldJGb+Hc1XAhhInsTa8HvCGw5334ezl8CukyRmhQlU7uz5q8c+qMOrCW2dTfOVBX0nKL6L0G9/ATd/keS022me3lrVPY2uXE74xZf6/zmkTwZV9SbWjV/HznfR6zdg9ffLpQ7r20C8hsBbjxN6rY8jiKkh+MrLJL96K/an/xb7g/8hEO3hBcdfIvIHh/hnbyF53dewF7TVOkFg/a8Jvb5jcEerQUrf2aCBfNxLRmESteijJztueDoP97LRmEQd+lgdihDu6PGYjO5m1IQ+dBB1ZqOzMHmfwM3NBCeKrj2OSnZapMyxOIXZqLo96KgDWWNxRlrowwdRtsKMnIibFTv798UTcLMtVM1udJNp+Z589HiM/gh9pObsGxT5BM6oES09HT6IstsvZ+uydF67mYW4BXkYYqiTR9HN/Tj+qBySdz5E7PItRP7jkR6+YmwviBl9OW7IRdXsaVmGszPrefnOrG8XYvXouhqU3WkBely+tpqcXc+ZY3EKcyB6CKuu83f7FiZvNG5uBOwGdG03tdJA5ZQujgGhtFcW/TfgAIh+imvglNddCOGRxgCYj0CN6nta4RnTROAvD5AZaUQPrxurne8aA6CqgMledyJ646BOVHP+3CnpvHFMK0yF110I4QllqjVKvdf3lEJcgIzerSM69gYQ62taIS40rstGfWL7K6cNap3XzQiRZvG8TPctDaDhSa+7ESLN3jm66YUmDdCQm/EM8nuA8BGl1ApoOxv07WeajTG/87QjIdIn6Wr9NLQ7HdoJBB8A0nQhmhBeMmui25+rgXYBaN6+4rBCPeZdU0KkidEPtP1nh0tQXEv/GPg47Q0JkT7/11i5cn3bHx0CEN3+XI1B/SD9PQmRFsa4/Fv7B7pchBidkvErFO+krych0sTwZLRqVYffvLpehfvMM45Wzp1AQ7r6EiINTrnK/k7nB7u9DL1+x4t7Ferrqe9JiPQwintO73zpeOfHezzDNl5bvSNUWBIB5qW0MyFSzBjzi+jOFx7q7rleb0TSuHPm95XimdS0JUTqKcWrURXuMvRp08c1Fm+YeOboF0IZoXJg4hD3JkSqbQrZ3NRU9VyPNxrq+1ZU+9+INcaTtwKrh7IzIVJsk7Gsm+qqV/V61+X+XWX30R4nUTj92ZBxxqKYOSTtCZEiSvFqyOamU5Ur+/xRt/+XmdZWOona6lWhwuJG4Abk/y4jhiGj1C8bTeju3oY97Q3qxmjZkxfPV5ongPGDeb0QKXDKKO6JVqxaMZAXDepGA4m66gO5BcW/cTQXATMZZJCEGAIGw5Ouspec3rn6/YG++Jw33Mwpi2daiv8Grj/XeQkxIIp1xuEHnU9vGNgshkjW5CU3aG3+GbgJ+XwgUscG8zJGP9D+rM7BGvKhS97Uz00wxvkSqMUGZgz1/IUvxYF3lFIrXK2fbruYZSikdOw+YvJN41wVmGcUZQZmKLgUGNH6L5zK2uK8kwATBXUK1AmUuwujd2tlNmWFzIajm15oSkXR/wcKqxAkm8CMrAAAAABJRU5ErkJggg=="
st.markdown(f"""
<link rel="manifest" href="app/static/manifest.json">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="TULSA">
<link rel="apple-touch-icon" href="data:image/png;base64,{_ICON_B64}">
<link rel="icon" type="image/png" href="data:image/png;base64,{_ICON_B64}">
<meta name="theme-color" content="#0D2B4E">
""", unsafe_allow_html=True)

# =========================================================
# ESTADO
# =========================================================

# Valores por defecto de la sesion
_DEFAULTS = {
    "items":          [],
    "ss_cliente":     "",
    "ss_ubicacion":   "",
    "ss_telefono":    "",
    "ss_folio_nota":  "",
    "ss_metodo_pago": "Efectivo",
    "ss_estatus":     "Pagado",
    "ss_tecnico":     "",
    "ss_esquema":     0,
    "ss_descuento":   10,
    "ss_aplicar_desc": False,
    "ss_iva":         False,
    "ss_viaticos":    False,
    "ss_costo_viat":  0.0,
    "ss_notas":       "",
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f4f6f8;
}

.stButton > button {
    background-color: #0D2B4E;
    color: white;
    border-radius: 6px;
    border: none;
    font-weight: bold;
    width: 100%;
    height: 45px;
    font-size: 15px;
}

.stButton > button:hover {
    background-color: #00adef;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# COLORES
# =========================================================

NAVY       = (13,  43,  78)
AZUL       = (0,  173, 239)
GRIS_H     = (245, 247, 250)
GRIS_BORDE = (210, 215, 220)
VERDE      = (0,  160,  70)
ROJO       = (190,  30,  45)
NEGRO      = (35,   35,  35)
GRIS_MED   = (100, 100, 100)

# =========================================================
# FUNCIONES
# =========================================================

def limpiar_texto(texto):
    return str(texto).encode("latin-1", "replace").decode("latin-1")

def money(valor):
    return f"$ {valor:,.2f}"

# =========================================================
# PDF CLASS
# =========================================================

def escribir_justificado(pdf, h, texto, margen_izq=13, margen_der=200):
    """
    Escribe texto justificado usando cell() (sin auto-wrap de write).
    - Primera linea: arranca desde pdf.get_x() actual.
    - Lineas siguientes: desde margen_izq.
    - Ultima linea: alineada a la izquierda.
    """
    palabras = texto.split()
    if not palabras:
        return

    x_inicio    = pdf.get_x()
    ancho_1ra   = margen_der - x_inicio
    ancho_resto = margen_der - margen_izq

    # ── Paso 1: armar lineas ──────────────────────────────
    lineas       = []
    linea_actual = []
    ancho_actual = 0
    primera      = True

    for palabra in palabras:
        aw    = ancho_1ra if primera else ancho_resto
        w_pal = pdf.get_string_width(palabra)
        w_sep = pdf.get_string_width(" ") if linea_actual else 0

        if linea_actual and ancho_actual + w_sep + w_pal > aw:
            lineas.append((linea_actual[:], aw, primera))
            linea_actual = [palabra]
            ancho_actual = w_pal
            primera      = False
        else:
            if linea_actual:
                ancho_actual += pdf.get_string_width(" ")
            linea_actual.append(palabra)
            ancho_actual += w_pal

    if linea_actual:
        lineas.append((linea_actual,
                       ancho_1ra if primera else ancho_resto,
                       primera))

    # ── Paso 2: renderizar con cell() (posicion exacta) ──
    for i, (pals, ancho_disp, es_primera) in enumerate(lineas):
        es_ultima = (i == len(lineas) - 1)

        if not es_primera:
            pdf.set_x(margen_izq)

        if es_ultima or len(pals) == 1:
            # Ultima linea: cada palabra con su espacio normal
            for j, pal in enumerate(pals):
                w_pal = pdf.get_string_width(pal)
                sep   = pdf.get_string_width(" ") if j < len(pals) - 1 else 0
                pdf.cell(w_pal + sep, h, pal)
        else:
            # Linea justificada: distribuir espacio sobrante entre palabras
            ancho_pals = sum(pdf.get_string_width(p) for p in pals)
            gap = (ancho_disp - ancho_pals) / max(len(pals) - 1, 1)
            for j, pal in enumerate(pals):
                w_pal  = pdf.get_string_width(pal)
                cell_w = w_pal + (gap if j < len(pals) - 1 else 0)
                pdf.cell(cell_w, h, pal)

        if not es_ultima:
            pdf.ln(h)



class PDF(FPDF):
    pass

# =========================================================
# SIDEBAR
# =========================================================

# Nota de servicio: folio fijo vacio
folio = ""

with st.sidebar:

    st.header("Informacion General")

    # ── Cargar sesion ──────────────────────────────────
    archivo_cargado = st.file_uploader(
        "Cargar cotizacion (.json)",
        type=["json"],
        label_visibility="collapsed"
    )
    if archivo_cargado is not None:
        # Usar file_id para evitar rerun en loop
        file_id = archivo_cargado.file_id
        if st.session_state.get("_ultimo_json") != file_id:
            import json as _json
            try:
                datos = _json.loads(archivo_cargado.read().decode("utf-8"))
                st.session_state["ss_cliente"]    = datos.get("cliente", "")
                st.session_state["ss_ubicacion"]  = datos.get("ubicacion", "")
                st.session_state["ss_telefono"]   = datos.get("telefono", "")
                st.session_state["ss_folio"]      = datos.get("folio", "TULSA-2024-001")
                st.session_state["ss_esquema"]    = datos.get("esquema_idx", 0)
                st.session_state["ss_aplicar_desc"] = datos.get("aplicar_descuento", False)
                st.session_state["ss_descuento"]    = datos.get("descuento_pct", 10)
                st.session_state["ss_iva"]        = datos.get("iva_incluido", False)
                st.session_state["ss_viaticos"]   = datos.get("cobrar_viaticos", False)
                st.session_state["ss_costo_viat"] = datos.get("costo_viaticos", 0.0)
                st.session_state["ss_notas"]      = datos.get("notas", "")
                st.session_state["ss_folio_nota"] = datos.get("folio_nota", "")
                st.session_state["ss_metodo_pago"]= datos.get("metodo_pago", "Efectivo")
                st.session_state["ss_estatus"]    = datos.get("estatus_pago", "Pagado")
                st.session_state["ss_tecnico"]    = datos.get("tecnico", "")
                st.session_state["items"]         = datos.get("items", [])
                if "fecha" in datos:
                    try:
                        st.session_state["ss_fecha"] = datetime.date.fromisoformat(datos["fecha"])
                    except Exception:
                        pass
                st.session_state["_ultimo_json"] = file_id
                st.success("Cotizacion cargada correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al cargar: {e}")

    st.divider()

    cliente   = st.text_input("Cliente",   key="ss_cliente")
    ubicacion = st.text_input("Domicilio", key="ss_ubicacion")
    telefono  = st.text_input("Telefono",  key="ss_telefono")
    folio     = st.text_input(
        "Folio (opcional)",
        key="ss_folio_nota",
        placeholder="Ej: NS-2026-001"
    )
    if "ss_fecha" not in st.session_state:
        st.session_state["ss_fecha"] = datetime.date.today()
    fecha_hoy = st.date_input("Fecha", key="ss_fecha")

    st.divider()

    metodo_pago = st.selectbox(
        "Metodo de pago",
        options=["Efectivo", "Tarjeta debito", "Tarjeta credito",
                 "Transferencia", "Cheque", "Otro"],
        index=["Efectivo", "Tarjeta debito", "Tarjeta credito",
               "Transferencia", "Cheque", "Otro"].index(
                   st.session_state.get("ss_metodo_pago", "Efectivo")
               ),
        key="ss_metodo_pago"
    )

    estatus_pago = st.selectbox(
        "Estatus de pago",
        options=["Pagado", "Pago parcial", "Pendiente"],
        index=["Pagado", "Pago parcial", "Pendiente"].index(
                   st.session_state.get("ss_estatus", "Pagado")
               ),
        key="ss_estatus"
    )

    tecnico = st.text_input(
        "Atendido por (opcional)",
        key="ss_tecnico",
        placeholder="Nombre del tecnico o instalador"
    )

    st.divider()

    esquema_pago = st.radio(
        "Esquema de pago",
        options=["50/50  -  Piezas sueltas", "40/30/30  -  Obra integral"],
        index=st.session_state["ss_esquema"],
        key="ss_esquema_radio"
    )
    es_obra_integral = esquema_pago.startswith("40")

    st.divider()

    aplicar_descuento = st.checkbox(
        "Aplicar descuento",
        value=st.session_state["ss_aplicar_desc"],
        key="ss_aplicar_desc"
    )
    if aplicar_descuento:
        descuento_pct = st.number_input(
            "Descuento (%)", min_value=1, max_value=100,
            value=max(1, st.session_state["ss_descuento"]),
            key="ss_descuento_inp"
        )
    else:
        descuento_pct = 0

    iva_incluido    = st.checkbox("Desglosar IVA (16%)",
                                  value=st.session_state["ss_iva"],
                                  key="ss_iva_chk")
    cobrar_viaticos = st.checkbox("Cobrar viaticos",
                                  value=st.session_state["ss_viaticos"],
                                  key="ss_viat_chk")

    if cobrar_viaticos:
        costo_viaticos = st.number_input(
            "Costo de viaticos ($)", min_value=0.0, step=100.0,
            value=st.session_state["ss_costo_viat"], key="ss_costo_inp"
        )
    else:
        costo_viaticos = 0.0

    st.divider()

    notas = st.text_area(
        "Notas / Aclaraciones (opcional)",
        value=st.session_state["ss_notas"],
        height=100,
        key="ss_notas_area",
        placeholder="Ej: Cliente acuerda anticipo del 25%. "
                    "Se detectaron descuadres en vano de ventana cocina..."
    )

    st.divider()

    # ── Guardar sesion ─────────────────────────────────
    import json as _json
    _sesion = {
        "cliente":        cliente,
        "ubicacion":      ubicacion,
        "telefono":       telefono,
        "folio_nota":     folio,
        "metodo_pago":    metodo_pago,
        "estatus_pago":   estatus_pago,
        "tecnico":        tecnico,
        "fecha":          fecha_hoy.isoformat(),
        "esquema_idx":    0 if not es_obra_integral else 1,
        "aplicar_descuento": aplicar_descuento,
        "descuento_pct":  descuento_pct,
        "iva_incluido":   iva_incluido,
        "cobrar_viaticos":cobrar_viaticos,
        "costo_viaticos": costo_viaticos,
        "notas":          notas,
        "items":          st.session_state["items"],
    }
    st.download_button(
        label="Guardar sesion (.json)",
        data=_json.dumps(_sesion, ensure_ascii=False, indent=2),
        file_name=f"NotaServicio_{fecha_hoy.isoformat()}.json",
        mime="application/json"
    )

# =========================================================
# TITULO
# =========================================================

st.title("TULSA - Nota de Servicio")
st.write("Genera notas de servicio profesionales.")

# =========================================================
# CAPTURA
# =========================================================

with st.container():

    c1, c2, c3, c4 = st.columns([1, 4, 2, 2])

    with c1:
        cantidad = st.number_input("Cant.", min_value=1, value=1)

    with c2:
        descripcion = st.text_area("Descripcion", height=90)

    with c3:
        medidas = st.text_input("Medidas HxL", "100 x 100 cm")

    with c4:
        precio = st.number_input("Precio Unitario", min_value=0.0, step=100.0)

    if st.button("AGREGAR CONCEPTO"):
        if descripcion.strip() == "":
            st.warning("Ingrese una descripcion.")
        else:
            import uuid as _uuid
            st.session_state["items"].append({
                "_id":         str(_uuid.uuid4()),  # ID estable para keys
                "Cant":        cantidad,
                "Descripcion": descripcion,
                "Medidas":     medidas,
                "PrecioUnit":  precio,
                "Total":       cantidad * precio
            })
            st.rerun()

# =========================================================
# TABLA VISTA PREVIA
# =========================================================

if st.session_state["items"]:

    st.divider()

    # ── Tabla editable con eliminacion por fila ──
    st.markdown("**Conceptos agregados** (puedes eliminar o editar cada fila):")

    # Asegurar que todos los items tengan _id y PrecioUnit (compat. JSON viejo)
    import uuid as _uuid
    for _item in st.session_state["items"]:
        if "_id" not in _item:
            _item["_id"] = str(_uuid.uuid4())
        if "PrecioUnit" not in _item:
            _item["PrecioUnit"] = (_item["Total"] / _item["Cant"]
                                   if _item["Cant"] else 0)

    # Encabezados
    h0, h1, h2, h3, h4, h5, h6 = st.columns([0.35, 0.5, 2.8, 1.4, 1.1, 1.1, 0.55])
    h0.markdown("**#**")
    h1.markdown("**Cant.**")
    h2.markdown("**Descripcion**")
    h3.markdown("**Medidas**")
    h4.markdown("**P. Unit.**")
    h5.markdown("**Total**")
    h6.markdown("**Del.**")

    idx_eliminar = None

    for i, item in enumerate(st.session_state["items"]):
        # Usar _id estable como key — evita el bug de valores cruzados al borrar
        uid = item["_id"]
        c0, c1, c2, c3, c4, c5, c6 = st.columns([0.35, 0.5, 2.8, 1.4, 1.1, 1.1, 0.55])
        c0.markdown(f"{i + 1}")

        nueva_cant = c1.number_input(
            "", min_value=1, value=int(item["Cant"]),
            key=f"cant_{uid}", label_visibility="collapsed"
        )
        nueva_desc = c2.text_input(
            "", value=item.get("Descripcion", item.get("Descripci\xf3n", "")),
            key=f"desc_{uid}", label_visibility="collapsed"
        )
        nuevas_med = c3.text_input(
            "", value=item["Medidas"],
            key=f"med_{uid}", label_visibility="collapsed"
        )
        nuevo_precio = c4.number_input(
            "", min_value=0.0, step=100.0,
            value=float(item["PrecioUnit"]),
            key=f"precio_{uid}", label_visibility="collapsed"
        )
        nuevo_total = nueva_cant * nuevo_precio
        c5.markdown(f"{money(nuevo_total)}")

        # Actualizar si cambio algo
        if (nueva_cant   != item["Cant"]
                or nueva_desc  != item.get("Descripcion", item.get("Descripci\xf3n", ""))
                or nuevas_med  != item["Medidas"]
                or nuevo_precio != item["PrecioUnit"]):
            st.session_state["items"][i]["Cant"]       = nueva_cant
            st.session_state["items"][i]["Descripcion"]= nueva_desc
            st.session_state["items"][i]["Medidas"]    = nuevas_med
            st.session_state["items"][i]["PrecioUnit"] = nuevo_precio
            st.session_state["items"][i]["Total"]      = nuevo_total

        if c6.button("X", key=f"del_{uid}"):
            idx_eliminar = i

    if idx_eliminar is not None:
        st.session_state["items"].pop(idx_eliminar)
        st.rerun()

    df = pd.DataFrame(st.session_state["items"])

    subtotal_prev  = df["Total"].sum()
    descuento_prev = subtotal_prev * (descuento_pct / 100)
    subtotal_desc  = subtotal_prev - descuento_prev
    base_iva_prev  = subtotal_desc + costo_viaticos
    iva_prev       = base_iva_prev * 0.16

    total_mostrar_prev = base_iva_prev
    if iva_incluido:
        total_mostrar_prev += iva_prev

    st.markdown(f"### Subtotal: {money(subtotal_prev)}")
    if aplicar_descuento and descuento_prev > 0:
        st.markdown(f"### Descuento ({descuento_pct}%): - {money(descuento_prev)}")
    if cobrar_viaticos:
        st.markdown(f"### Viaticos: {money(costo_viaticos)}")
    if iva_incluido:
        st.markdown(f"### IVA (16%): {money(iva_prev)}")
    st.markdown(f"## Total Final: {money(total_mostrar_prev)}")

    # =====================================================
    # BOTONES
    # =====================================================

    b1, b2 = st.columns(2)

    with b1:
        if st.button("LIMPIAR LISTA"):
            st.session_state["items"] = []
            st.rerun()

    with b2:
        if st.button("GENERAR PDF PROFESIONAL"):
            try:

                pdf = PDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                # ─────────────────────────────────────────
                # ENCABEZADO NAVY
                # ─────────────────────────────────────────

                HEADER_H = 45
                pdf.set_fill_color(*NAVY)
                pdf.rect(0, 0, 210, HEADER_H, "F")

                # Logo centrado verticalmente en la franja
                logo = "quita fonod.png"
                if os.path.isfile(logo):
                    try:
                        LOGO_W    = 48     # mas grande
                        LOGO_H_EST = 18    # proporcion aprox del logo TULSA
                        logo_y = (HEADER_H - LOGO_H_EST) / 2
                        pdf.image(logo, 10, logo_y, LOGO_W)
                    except Exception:
                        pass

                # Datos del negocio — centrados verticalmente entre logo y bloque NOTA
                NEG_FONT  = 7.5
                NEG_LH    = 5.2   # interlineado
                NEG_LINES = 3     # RFC + direccion + tel
                NEG_H     = NEG_LINES * NEG_LH
                neg_x = 62
                neg_y = (HEADER_H - NEG_H) / 2  # centrado vertical exacto
                pdf.set_font("Helvetica", "", NEG_FONT)
                pdf.set_text_color(200, 220, 240)
                for neg_linea in [
                    "RFC: VIGA920128UJ4",
                    "Revoluci\xf3n 48, Barrio Alto. CP. 28450. Comala, Col.",
                    "Tel: 3122415481",
                ]:
                    pdf.set_xy(neg_x, neg_y)
                    pdf.cell(0, NEG_LH, neg_linea, 0, 0)
                    neg_y += NEG_LH

                # "NOTA" grande a la derecha
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Helvetica", "B", 32)
                pdf.set_xy(0, 6)
                pdf.cell(198, 14, "NOTA", 0, 1, "R")

                # Subtitulo
                pdf.set_font("Helvetica", "", 10)
                pdf.set_x(0)
                pdf.cell(198, 6, "Canceler\xeda en Aluminio y Vidrio", 0, 1, "R")

                # Folio y fecha
                pdf.set_font("Helvetica", "", 9)
                pdf.set_x(0)
                folio_texto = folio.strip() if folio.strip() else "_______________"
                pdf.cell(
                    198, 6,
                    f"Folio: {folio_texto}  |  Fecha: {fecha_hoy.strftime('%d/%m/%Y')}",
                    0, 1, "R"
                )

                # Linea separadora cyan bajo el header
                pdf.set_draw_color(*AZUL)
                pdf.set_line_width(0.8)
                pdf.line(0, HEADER_H, 210, HEADER_H)
                # Reset a gris para evitar que lineas navy
                # del encabezado afecten la caja del cliente
                pdf.set_draw_color(*GRIS_BORDE)
                pdf.set_line_width(0.3)

                # ─────────────────────────────────────────
                # CAJA CLIENTE
                # ─────────────────────────────────────────

                pdf.ln(5)
                box_y  = pdf.get_y()
                PAD_V  = 3    # padding top/bottom
                LINE_H = 5    # altura de cada renglon
                box_h  = PAD_V + LINE_H + LINE_H + PAD_V  # siempre 2 renglones = 16
                tiene_tel = telefono.strip() != ""

                # Fondo, borde y barra izquierda
                pdf.set_fill_color(*GRIS_H)
                pdf.rect(10, box_y, 190, box_h, "F")
                pdf.set_draw_color(*GRIS_BORDE)
                pdf.rect(10, box_y, 190, box_h, "D")
                pdf.set_fill_color(*NAVY)
                pdf.rect(10, box_y, 3, box_h, "F")
                pdf.set_draw_color(*GRIS_BORDE)

                # Columna izquierda: CLIENTE + DOMICILIO
                col_izq_lbl = 28   # ancho etiqueta
                col_izq_val = 85   # ancho valor (hasta mitad de caja)

                pdf.set_text_color(*NEGRO)
                pdf.set_xy(16, box_y + PAD_V)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(col_izq_lbl, LINE_H, "CLIENTE:", 0, 0)
                pdf.set_font("Helvetica", "", 10)
                pdf.cell(col_izq_val, LINE_H, limpiar_texto(cliente), 0, 1)

                pdf.set_xy(16, box_y + PAD_V + LINE_H)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(col_izq_lbl, LINE_H, "DOMICILIO:", 0, 0)
                pdf.set_font("Helvetica", "", 10)
                pdf.cell(col_izq_val, LINE_H, limpiar_texto(ubicacion), 0, 1)

                # Columna derecha: TELÉFONO centrado verticalmente
                if tiene_tel:
                    tel_x   = 140   # x inicio columna derecha
                    tel_lbl = 22
                    tel_y   = box_y + (box_h - LINE_H) / 2  # centrado vertical
                    pdf.set_xy(tel_x, tel_y)
                    pdf.set_font("Helvetica", "B", 10)
                    pdf.set_text_color(*NEGRO)
                    pdf.cell(tel_lbl, LINE_H, "TEL\xc9FONO:", 0, 0)
                    pdf.set_font("Helvetica", "", 10)
                    pdf.cell(0, LINE_H, limpiar_texto(telefono), 0, 1)

                # Mover cursor debajo de la caja con padding minimo
                pdf.set_xy(10, box_y + box_h + 4)

                # ─────────────────────────────────────────
                # TABLA ENCABEZADO
                # ─────────────────────────────────────────

                col_num  = 8
                col_cant = 12
                col_desc = 110
                col_med  = 30
                col_imp  = 30
                margen_x = 10

                pdf.set_x(margen_x)
                pdf.set_fill_color(*NAVY)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_draw_color(*NAVY)

                pdf.cell(col_num,  9, "#",     1, 0, "C", True)
                pdf.cell(col_cant, 9, "CANT.", 1, 0, "C", True)
                pdf.cell(
                    col_desc, 9,
                    "DESCRIPCI\xd3N DE FABRICACI\xd3N / SERVICIO",
                    1, 0, "C", True
                )
                pdf.cell(col_med, 9, "MEDIDAS HxL", 1, 0, "C", True)
                pdf.cell(col_imp, 9, "IMPORTE",     1, 1, "C", True)

                # ─────────────────────────────────────────
                # TABLA FILAS
                # ─────────────────────────────────────────

                pdf.set_draw_color(*GRIS_BORDE)
                pdf.set_text_color(*NEGRO)
                pdf.set_font("Helvetica", "", 9)

                subtotal  = 0
                fila_par  = False
                num_fila  = 0

                for item in st.session_state["items"]:
                    num_fila += 1

                    desc = limpiar_texto(item.get("Descripcion", item.get("Descripción", "")))
                    meds = limpiar_texto(item["Medidas"])

                    # Medir con el mismo ancho que se usa al renderizar (col_desc-2)
                    lineas   = pdf.multi_cell(col_desc - 2, 5, desc, split_only=True)
                    n_lineas = len(lineas)
                    # Padding: 2 arriba + 2 abajo; minimo 12mm
                    altura   = max(12, n_lineas * 5 + 4)

                    x = margen_x
                    y = pdf.get_y()

                    if y + altura > 260:
                        pdf.add_page()
                        y = pdf.get_y()

                    fill_color = GRIS_H if fila_par else (255, 255, 255)
                    pdf.set_fill_color(*fill_color)
                    pdf.rect(
                        x, y,
                        col_num + col_cant + col_desc + col_med + col_imp,
                        altura, "F"
                    )
                    fila_par = not fila_par

                    pdf.set_draw_color(*GRIS_BORDE)

                    # NUMERO CONSECUTIVO
                    pdf.set_xy(x, y)
                    pdf.rect(x, y, col_num, altura)
                    pdf.set_font("Helvetica", "", 8)
                    pdf.set_text_color(*GRIS_MED)
                    pdf.multi_cell(col_num, altura, str(num_fila), 0, "C")
                    pdf.set_text_color(*NEGRO)

                    # CANTIDAD
                    pdf.set_xy(x + col_num, y)
                    pdf.rect(x + col_num, y, col_cant, altura)
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.multi_cell(col_cant, altura, str(item["Cant"]), 0, "C")

                    # DESCRIPCION
                    alto_texto = n_lineas * 5
                    y_desc     = y + (altura - alto_texto) / 2
                    pdf.set_font("Helvetica", "", 9)
                    pdf.rect(x + col_num + col_cant, y, col_desc, altura)
                    pdf.set_xy(x + col_num + col_cant + 2, y_desc)
                    pdf.multi_cell(col_desc - 2, 5, desc, 0, "J")

                    # MEDIDAS
                    pdf.set_xy(x + col_num + col_cant + col_desc, y)
                    pdf.rect(x + col_num + col_cant + col_desc, y, col_med, altura)
                    pdf.multi_cell(col_med, altura, meds, 0, "C")

                    # IMPORTE
                    pdf.set_xy(x + col_num + col_cant + col_desc + col_med, y)
                    pdf.rect(x + col_num + col_cant + col_desc + col_med, y, col_imp, altura)
                    pdf.multi_cell(col_imp, altura, money(item["Total"]), 0, "R")

                    pdf.set_xy(x, y + altura)
                    subtotal += item["Total"]

                # ─────────────────────────────────────────
                # TOTALES
                # ─────────────────────────────────────────

                descuento          = subtotal * (descuento_pct / 100)
                subtotal_descuento = subtotal - descuento
                base_iva           = subtotal_descuento + costo_viaticos
                iva                = base_iva * 0.16
                total_pdf = base_iva
                if iva_incluido:
                    total_pdf += iva

                pdf.ln(5)
                tot_x = 110
                tot_w = 90
                tot_y = pdf.get_y()

                n_filas = 2  # subtotal + viaticos siempre presentes
                if aplicar_descuento and descuento > 0:
                    n_filas += 1
                if iva_incluido:
                    n_filas += 1
                tot_h = n_filas * 8 + 20

                pdf.set_fill_color(*GRIS_H)
                pdf.rect(tot_x, tot_y, tot_w, tot_h, "F")

                lbl_w = 50
                val_x = tot_x + lbl_w
                val_w = tot_w - lbl_w

                def fila_total(label, valor,
                               color_lbl=None, color_val=None, negrita=False):
                    pdf.set_x(tot_x + 4)
                    pdf.set_font("Helvetica", "B" if negrita else "", 10)
                    pdf.set_text_color(*(color_lbl or NEGRO))
                    pdf.cell(lbl_w - 4, 8, label, 0, 0, "L")
                    pdf.set_x(val_x)
                    pdf.set_font("Helvetica", "B" if negrita else "", 10)
                    pdf.set_text_color(*(color_val or NEGRO))
                    pdf.cell(val_w - 4, 8, valor, 0, 1, "R")

                fila_total("SUBTOTAL:", money(subtotal), negrita=True)

                if aplicar_descuento and descuento > 0:
                    fila_total(
                        f"DESCUENTO ({descuento_pct}%):",
                        f"- {money(descuento)}",
                        color_lbl=ROJO, color_val=ROJO, negrita=True
                    )

                # VIATICOS
                cy = pdf.get_y()
                pdf.set_x(tot_x + 4)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(*NEGRO)
                pdf.cell(lbl_w - 4, 8, "VI\xc1TICOS:", 0, 0, "L")

                if cobrar_viaticos:
                    pdf.set_x(val_x)
                    pdf.set_font("Helvetica", "", 10)
                    pdf.set_text_color(*NEGRO)
                    pdf.cell(val_w - 4, 8, money(costo_viaticos), 0, 1, "R")
                else:
                    pdf.set_x(val_x)
                    pdf.set_font("Helvetica", "", 10)
                    pdf.set_text_color(*NEGRO)
                    pdf.cell(val_w - 30, 8, "$ 0.00", 0, 0, "R")
                    badge_x = val_x + val_w - 28
                    pdf.set_fill_color(*VERDE)
                    pdf.rect(badge_x, cy + 1.5, 26, 5.5, "F")
                    pdf.set_xy(badge_x, cy + 1)
                    pdf.set_font("Helvetica", "B", 7)
                    pdf.set_text_color(255, 255, 255)
                    pdf.cell(26, 7, "CORTESIA", 0, 1, "C")

                if iva_incluido:
                    fila_total("I.V.A. (16%):", money(iva), negrita=True)

                # Separador navy
                sep_y = pdf.get_y()
                pdf.set_draw_color(*NAVY)
                pdf.set_line_width(0.5)
                pdf.line(tot_x + 4, sep_y, tot_x + tot_w - 4, sep_y)
                pdf.set_line_width(0.3)
                pdf.set_draw_color(*GRIS_BORDE)
                pdf.ln(2)

                # TOTAL FINAL
                pdf.set_x(tot_x + 4)
                pdf.set_font("Helvetica", "B", 13)
                pdf.set_text_color(*NAVY)
                pdf.cell(lbl_w - 4, 9, "TOTAL FINAL:", 0, 0, "L")
                pdf.set_x(val_x)
                pdf.set_font("Helvetica", "B", 14)
                pdf.cell(val_w - 4, 9, money(total_pdf), 0, 1, "R")

                pdf.set_x(val_x)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(*GRIS_MED)
                pdf.cell(val_w - 4, 6, "MXN", 0, 1, "R")

                # Metodo de pago + Estatus
                pdf.ln(3)
                mp_y = pdf.get_y()

                # Badge estatus (color segun valor)
                estatus_colores = {
                    "Pagado":       VERDE,
                    "Pago parcial": (220, 140, 0),
                    "Pendiente":    ROJO,
                }
                col_estatus = estatus_colores.get(estatus_pago, VERDE)
                badge_w = 40; badge_h = 8
                badge_x2 = tot_x + tot_w - badge_w - 4
                pdf.set_fill_color(*col_estatus)
                pdf.rect(badge_x2, mp_y, badge_w, badge_h, "F")
                pdf.set_xy(badge_x2, mp_y + 1)
                pdf.set_font("Helvetica", "B", 7)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(badge_w, 6, limpiar_texto(estatus_pago.upper()), 0, 0, "C")

                # Metodo de pago a la izquierda del badge
                pdf.set_xy(tot_x + 4, mp_y + 1)
                pdf.set_font("Helvetica", "B", 8)
                pdf.set_text_color(*NEGRO)
                pdf.cell(30, 6, "Pago:", 0, 0)
                pdf.set_font("Helvetica", "", 8)
                pdf.cell(badge_x2 - tot_x - 34, 6, limpiar_texto(metodo_pago), 0, 1)

                # Tecnico (si se llenó)
                if tecnico.strip():
                    pdf.set_x(tot_x + 4)
                    pdf.set_font("Helvetica", "B", 8)
                    pdf.set_text_color(*NEGRO)
                    pdf.cell(30, 6, "Atendido:", 0, 0)
                    pdf.set_font("Helvetica", "", 8)
                    pdf.cell(0, 6, limpiar_texto(tecnico.strip()), 0, 1)

                # ─────────────────────────────────────────
                # NOTAS / ACLARACIONES (si existen)
                # ─────────────────────────────────────────

                if notas and notas.strip():
                    pdf.ln(8)
                    nota_y = pdf.get_y()
                    pdf.set_fill_color(*GRIS_H)
                    pdf.rect(10, nota_y, 190, 7, "F")
                    pdf.set_fill_color(*AZUL)
                    pdf.rect(10, nota_y, 3, 7, "F")
                    pdf.set_xy(16, nota_y + 1)
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.set_text_color(*NAVY)
                    pdf.cell(0, 5, "Notas / Aclaraciones:", 0, 1)
                    pdf.ln(2)
                    pdf.set_x(14)
                    pdf.set_font("Helvetica", "", 9)
                    pdf.set_text_color(*NEGRO)
                    pdf.multi_cell(186, 5, limpiar_texto(notas.strip()))

                # ─────────────────────────────────────────
                # GRACIAS
                # ─────────────────────────────────────────

                # Texto legal digital
                pdf.ln(6)
                pdf.set_draw_color(*GRIS_BORDE)
                pdf.set_line_width(0.3)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(3)
                pdf.set_font("Helvetica", "", 6)
                pdf.set_text_color(120, 120, 120)
                texto_legal = (
                    "Este documento es una nota digital generada por TULSA Aluminio y Vidrio. "
                    "La recepci\xf3n del presente comprobante por cualquier medio electr\xf3nico "
                    "(WhatsApp, correo o similar) constituye la aceptaci\xf3n total e "
                    "incondicional de los trabajos realizados y de los T\xe9rminos y Condiciones "
                    "de TULSA, con el mismo valor legal que una firma aut\xf3grafa, conforme "
                    "al C\xf3digo de Comercio y el C\xf3digo Civil Federal."
                )
                pdf.multi_cell(190, 3.5, texto_legal, 0, "J")

                pdf.ln(4)
                # Asegurar espacio suficiente; si no, nueva pagina
                if pdf.get_y() + 16 > (297 - 15):
                    pdf.add_page()
                gracias_y = pdf.get_y()
                pdf.set_auto_page_break(False)
                pdf.set_fill_color(*NAVY)
                pdf.rect(10, gracias_y, 190, 12, "F")
                pdf.set_xy(10, gracias_y + 2)
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(190, 8, "\xa1Gracias por su preferencia!", 0, 1, "C")
                pdf.set_auto_page_break(True, margin=15)

                # ─────────────────────────────────────────
                # EXPORTAR
                # ─────────────────────────────────────────

                nombre_archivo = f"NotaServicio_TULSA_{fecha_hoy.strftime('%Y%m%d')}.pdf"
                pdf_bytes = pdf.output(dest="S").encode("latin-1")

                st.success("Nota generada correctamente.")

                st.download_button(
                    label="DESCARGAR PDF",
                    data=pdf_bytes,
                    file_name=nombre_archivo,
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Error al generar PDF:\n\n{e}")

else:
    st.info("Agrega conceptos para comenzar.")
