import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Análisis de variables económicas", layout="wide")
st.title("Análisis de variables económicas")


import nbformat
from wordcloud import WordCloud

def mostrar_nube_de_palabras():
    try:
        text_contents = ""
        for file_name in ["trabajo_final.ipynb", "proyecto_final.ipynb"]:
            with open(file_name, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)
                for cell in nb.cells:
                    if cell.cell_type in ["markdown", "code"]:
                        text_contents += cell.source + "\n"

        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_contents)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"No se pudo generar la nube de palabras: {e}")






# Función para graficar líneas con tendencia y anotaciones
def graficar_linea_con_tendencia(df, titulo, columna_valor, columna_fecha="fecha"):
    try:
        df[columna_fecha] = pd.to_datetime(df[columna_fecha])
        df = df.sort_values(by=columna_fecha)
        x = np.arange(len(df))
        y = df[columna_valor].values

        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)

        fig, ax = plt.subplots()
        ax.plot(df[columna_fecha], y, label=columna_valor, linewidth=2)
        ax.plot(df[columna_fecha], p(x), 'r--', label='Tendencia')

        # Líneas de cambio presidencial
        ax.axvline(pd.to_datetime('2010-08-07'), color='black', linestyle='--')
        ax.axvline(pd.to_datetime('2018-08-07'), color='black', linestyle='--')
        ax.axvline(pd.to_datetime('2022-08-07'), color='black', linestyle='--')

        ax.text(pd.to_datetime('2012-01-01'), max(y)*0.8, "P.Santos")
        ax.text(pd.to_datetime('2019-01-01'), max(y)*0.8, "P.Duque")
        ax.text(pd.to_datetime('2023-01-01'), max(y)*0.8, "P.Petro")

        ax.set_xlabel("Fecha")
        ax.set_ylabel(columna_valor)
        ax.set_title(titulo)
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"No se pudo generar el gráfico: {e}")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Desempleo", "Inflación", "PIB", "TRM", "Tasa de Cambio"])

# Tab Desempleo
# Tab Desempleo
with tab1:
    st.header("Desempleo")
    try:
        df = pd.read_csv("desempleo(cr).csv")
        st.dataframe(df)
        graficar_linea_con_tendencia(df, "Evolución del Desempleo", "tasa_desempleo")
    except Exception as e:
        st.error(f"No se pudo cargar el gráfico: {e}")
        
    try:
        st.image("DESEMPLEO.png", use_container_width=True)
    except:
        st.warning("Imagen no disponible.")
    
    # Análisis embellecido
    st.subheader("Análisis")
    st.markdown(
        """
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left:6px solid #6c63ff;">
            <p style="font-size:16px;">
                Tras la llegada del nuevo gobierno, los gráficos muestran cambios económicos clave. 
                El <strong>COLCAP</strong> cae y la <strong>TRM</strong> sube, superando los $4.800, reflejando 
                incertidumbre por reformas y menor confianza inversionista. Aunque influyen factores externos, 
                las políticas locales también generaron impacto. <br><br>
                El <strong>desempleo mejora tras la pandemia</strong>, pero se estanca, y la subida de 
                <strong>tasas de interés</strong> encarece el crédito, frenando el consumo. Además, el retiro 
                del <strong>subsidio a la gasolina</strong> desde septiembre de 2022 elevó precios y contribuyó 
                al pico inflacionario. <br><br>
                En conjunto, se evidencia cómo <strong>decisiones de política pública afectan directamente 
                los indicadores</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Tab Inflación
with tab2:
    st.header("Inflación")
    try:
        df = pd.read_csv("inflacion(cr).csv")
        st.dataframe(df)
        graficar_linea_con_tendencia(df, "Evolución de la Inflación", "inflacion")
    except Exception as e:
        st.error(f"No se pudo cargar el gráfico: {e}")
    
    try:
        st.image("INFLACION.png", use_container_width=True)
    except:
        st.warning("Imagen no disponible.")
    
    # Análisis embellecido
    st.subheader("Análisis")
    st.markdown(
    """
    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left:6px solid #E76F51; font-size:16px;">
        <p>
            Los gráficos muestran que la <strong>TRM e inflación subieron a fines de 2022</strong>, coincidiendo con el nuevo gobierno y sus reformas, 
            lo que causó <strong>incertidumbre y caída del COLCAP</strong>.
        </p>
        <p>
            La inflación también fue impulsada por la <strong>guerra en Ucrania</strong>, la <strong>crisis de suministros</strong> 
            y la <strong>eliminación del subsidio a la gasolina</strong>.
        </p>
        <p>
            El <strong>desempleo se estabilizó</strong> pese a programas de empleo, y los <strong>aumentos de tasas del Banco de la República</strong> 
            <strong>frenaron el PIB</strong>.
        </p>
        <p>
            La <strong>presidencia de Trump</strong> generó <strong>incertidumbre en exportadores colombianos</strong> 
            por dudas sobre tratados comerciales y redujo ayudas económicas.
        </p>
    </div>
    """,
    unsafe_allow_html=True)


# Tab PIB
with tab3:
    st.header("PIB")
    try:
        df = pd.read_csv("pib(cr).csv")
        st.dataframe(df)
        graficar_linea_con_tendencia(df, "Evolución del PIB", "pib_trimestral")
    except Exception as e:
        st.error(f"No se pudo cargar el gráfico: {e}")
    
    try:
        st.image("PIB1.png", use_container_width=True)
    except:
        st.warning("Imagen no disponible.")
    
    try:
        with open("PIB.txt", "r", encoding="utf-8") as f:
            st.subheader("Análisis")
            st.write(f.read())
    except:
        st.markdown(
        """
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left:6px solid #3C91E6; font-size:16px;">
            <p><strong>2022-2023 (inicio de gobierno):</strong><br>
            El lenguaje era profético y desafiante, con un tono de advertencia frente a los riesgos económicos.</p>

            <p><strong>2023-2024 (desempeño económico):</strong><br>
            Hay un tono más triunfalista, apelando a estadísticas y logros concretos como la reducción del desempleo, la inflación de alimentos, y el aumento del salario real.</p>

            <p><strong>2024-2025 (crítica estructural):</strong><br>
            El lenguaje se vuelve más estructural y filosófico, con amplias reflexiones sobre la desigualdad, el modelo económico, y una fuerte carga emocional y crítica.</p>
        </div>
        """,
        unsafe_allow_html=True)

# Tab TRM
with tab4:
    st.header("TRM")
    try:
        df = pd.read_csv("tasa cambio(cr).csv")
        st.dataframe(df)
        graficar_linea_con_tendencia(df, "Evolución de la TRM", "tasa_cambio(trm)")
    except Exception as e:
        st.error(f"No se pudo cargar el gráfico: {e}")
    
    try:
        st.image("TRM.png", use_container_width=True)
    except:
        st.warning("Imagen no disponible.")
    
    try:
        with open("TRM.txt", "r", encoding="utf-8") as f:
            st.subheader("Análisis")
            st.write(f.read())
    except:
        st.subheader("Análisis")
        st.markdown("""
        ### Parte 3: Relación entre Desempeño Económico y Discursos
        #### Tareas
        - Comparar tendencias económicas con el contenido de los discursos  
        - Relacionar el uso de ciertas palabras o temas en los discursos con momentos clave en la economía.
        En los discursos analizados (como el del PIB), se observa un uso frecuente de términos como **“crecimiento”**, **“cambió”**, **“pueblo”** y **“justicia social”**. Estos temas se intensifican especialmente en momentos de reformas o anuncios de política pública. Por ejemplo:
        El discurso sobre el PIB promueve un crecimiento con enfoque social, mientras que en los datos económicos se ve una desaceleración del PIB en los trimestres posteriores, lo que genera un contraste entre el optimismo discursivo y la realidad económica.
        - Se repiten palabras como **“reforma”** y **“energía”**, justo cuando la TRM y la inflación suben (segundo semestre de 2022), lo que sugiere que estos anuncios pudieron coincidir con una mayor percepción de riesgo en los mercados.
        """)


# Tab Tasa de Cambio (COLCAP)
with tab5:
    st.header("Tasa de Cambio (COLCAP)")
    
    # Cargar CSV y graficar
    try:
        df = pd.read_csv("colcap(cr).csv")
        st.dataframe(df)
        graficar_linea_con_tendencia(df, "Evolución del COLCAP", "colcap")
    except Exception as e:
        st.error(f"No se pudo cargar el gráfico: {e}")
    
    # Análisis embellecido directamente sin imagen
    st.subheader("Análisis")
    st.markdown("""
    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left:6px solid #009688; font-size:16px;">
        <p>
        <strong>Evaluar el impacto de la comunicación en la percepción económica</strong><br><br>
        Los discursos analizados promueven confianza desde lo social y político, pero no siempre generan seguridad en los mercados.
        Por ejemplo:
        </p>
        <ul>
            <li>El uso constante de términos como “transformación” o “modelo económico alternativo” coincide con la caída del COLCAP.</li>
            <li>La insistencia en subsidios y reformas sin detalles técnicos parece coincidir con un aumento en la TRM.</li>
        </ul>
        <p>
        Esto sugiere que el tono del discurso tiene un impacto real en la percepción económica, en especial cuando no está acompañado de claridad en la ejecución de políticas.
        </p>
        <hr>
        <strong>Conclusión final:</strong><br>
        Existe una brecha entre el discurso gubernamental y los resultados económicos. Mientras los discursos promueven justicia social y transformación:
        </p>
        <ul>
            <li>El COLCAP cae → desconfianza del mercado.</li>
            <li>La inflación sube → por retiro de subsidios y factores externos.</li>
            <li>La TRM se dispara → por incertidumbre política.</li>
            <li>El PIB se desacelera → a pesar del discurso de crecimiento.</li>
        </ul>
        <p>
        La comunicación política influye en las expectativas económicas: debe ser clara, técnica y coherente con la realidad para evitar volatilidad.
        </p>
    </div>
    """, unsafe_allow_html=True)
