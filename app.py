import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud

dp = pd.read_csv('desempleo(cr).csv')
tmr = pd.read_csv('tasa_cambio(cr).csv')
pib = pd.read_csv('pib(cr).csv')
cp = pd.read_csv('colcap(cr).csv')
inf = pd.read_csv('inflacion(cr).csv')

# Días y tendencias
degree = 3

dp['fecha'] = pd.to_datetime(dp['fecha'])
dp = dp.sort_values('fecha')
dp['dias'] = (dp['fecha'] - dp['fecha'].min()).dt.days
coefs_dp = np.polyfit(dp['dias'], dp['tasa_desempleo'], degree)
poly_dp = np.poly1d(coefs_dp)
dp['tendencia'] = poly_dp(dp['dias'])

pib['fecha'] = pd.to_datetime(pib['fecha'])
pib = pib.sort_values('fecha')
pib['dias'] = (pib['fecha'] - pib['fecha'].min()).dt.days
coefs_pib = np.polyfit(pib['dias'], pib['pib_trimestral'], degree)
poly_pib = np.poly1d(coefs_pib)
pib['tendencia'] = poly_pib(pib['dias'])

tmr['fecha'] = pd.to_datetime(tmr['fecha'])
tmr = tmr.sort_values('fecha')
tmr['dias'] = (tmr['fecha'] - tmr['fecha'].min()).dt.days
coefs_tmr = np.polyfit(tmr['dias'], tmr['tasa_cambio(trm)'], degree)
poly_tmr = np.poly1d(coefs_tmr)
tmr['tendencia'] = poly_tmr(tmr['dias'])

cp['fecha'] = pd.to_datetime(cp['fecha'])
cp = cp.sort_values('fecha')
cp['dias'] = (cp['fecha'] - cp['fecha'].min()).dt.days
coefs_cp = np.polyfit(cp['dias'], cp['colcap'], degree)
poly_cp = np.poly1d(coefs_cp)
cp['tendencia'] = poly_cp(cp['dias'])

inf['fecha'] = pd.to_datetime(inf['fecha'])
inf = inf.sort_values('fecha')
inf['dias'] = (inf['fecha'] - inf['fecha'].min()).dt.days
coefs_inf = np.polyfit(inf['dias'], inf['inflacion'], degree)
poly_inf = np.poly1d(coefs_inf)
inf['tendencia'] = poly_inf(inf['dias'])

st.title("Análisis variables económicas")
# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Desempleo", "Inflación", "PIB", "TRM", "Tasa de Cambio"])

# Tab Desempleo
# Tab Desempleo
with tab1:
    st.header("Desempleo")
    try:
st.subheader("Análisis Desempleo")
    fig = px.line(dp, x='fecha', y='tasa_desempleo', title='Tendencia del desempleo en el tiempo')
    fig.add_trace(px.line(dp, x='fecha', y='tendencia').data[0])  
    fig.data[1].line.dash = 'dash'  
    fig.data[1].line.color = 'red'  
    fig.data[1].name = 'Tendencia'  
    fig.add_vline(x='2018-08-07', line_dash="dash", line_color="gray")
    fig.add_vline(x='2022-08-07', line_dash="dash", line_color="gray")
    fig.add_annotation(x='2014-08-07', y=14, text="P.Santos", showarrow=False, font=dict(size=16))
    fig.add_annotation(x='2019-08-07', y=18, text="P.Duque", showarrow=False, font=dict(size=16))
    fig.add_annotation(x='2023-08-07', y=16, text="P.Petro", showarrow=False, font=dict(size=16))
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Tasa de Desempleo %', 
        xaxis_tickangle=45,
        template='plotly_white',
        width=1000,
        height=500
    )
    st.plotly_chart(fig)
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
