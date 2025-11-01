import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import io
import base64

# Configurar la página
st.set_page_config(
    page_title="Simulador de Resorte",
    page_icon="🔬",
    layout="wide"
)

# Título principal
st.title("🔬 Simulador de Compresión de Resorte")
st.markdown("---")

class SimulacionResorteWeb:
    def __init__(self, k, longitud_natural):
        self.k = k
        self.longitud_natural = longitud_natural
    
    def fuerza_resorte(self, x):
        return -self.k * x
    
    def trabajo_compresion(self, x_inicial, x_final):
        def integrando(x):
            return -self.fuerza_resorte(x)
        trabajo, error = quad(integrando, x_inicial, x_final)
        return trabajo
    
    def energia_potencial(self, x):
        return 0.5 * self.k * x**2
    
    def _dibujar_resorte(self, compresion_actual):
        """Dibuja la representación física del resorte"""
        longitud_actual = self.longitud_natural - compresion_actual
        
        fig, ax = plt.subplots(figsize=(8, 3))
        # Crear forma del resorte
        x_resorte = np.linspace(0, longitud_actual, 100)
        y_resorte = 0.1 * np.sin(20 * x_resorte / longitud_actual) * (x_resorte / longitud_actual)
        
        ax.plot(x_resorte, y_resorte, 'b-', linewidth=3, label='Resorte')
        ax.plot([0, 0], [-0.2, 0.2], 'k-', linewidth=4, label='Punto fijo')
        ax.plot([longitud_actual, longitud_actual], [-0.15, 0.15], 'r-', linewidth=6, label='Punto móvil')
        
        ax.set_xlim(-0.1, self.longitud_natural + 0.1)
        ax.set_ylim(-0.3, 0.3)
        ax.set_xlabel('Posición (m)')
        ax.set_title(f'Resorte - Compresión: {compresion_actual:.2f} m')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        return fig

def main():
    # Sidebar para controles
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        k = st.slider(
            "Constante del resorte k (N/m)",
            min_value=10,
            max_value=500,
            value=100,
            step=10,
            help="Rigidez del resorte - mayor k = más rígido"
        )
        
        longitud_natural = st.slider(
            "Longitud natural (m)",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1
        )
        
        compresion_maxima = st.slider(
            "Compresión máxima a simular (m)",
            min_value=0.1,
            max_value=0.9,
            value=0.8,
            step=0.1,
            help="Máxima compresión permitida"
        )
        
        st.markdown("---")
        st.header("🔍 Cálculo Específico")
        
        col1, col2 = st.columns(2)
        with col1:
            x_inicial = st.number_input("Compresión inicial (m)", 0.0, 0.9, 0.0, 0.1)
        with col2:
            x_final = st.number_input("Compresión final (m)", 0.1, 1.0, 0.5, 0.1)
    
    # Crear instancia del resorte
    resorte = SimulacionResorteWeb(k, longitud_natural)
    
    # Mostrar información resumida
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Constante k", f"{k} N/m")
    with col2:
        st.metric("Longitud natural", f"{longitud_natural} m")
    with col3:
        trabajo_especifico = resorte.trabajo_compresion(x_inicial, x_final)
        st.metric("Trabajo calculado", f"{trabajo_especifico:.2f} J")
    
    st.markdown("---")
    
    # Pestañas para diferentes visualizaciones
    tab1, tab2, tab3 = st.tabs(["📊 Gráficos Completos", "🎯 Cálculo Específico", "🔍 Representación Física"])
    
    with tab1:
        st.header("Análisis Gráfico Completo")
        
        # Generar datos para gráficos
        compresiones = np.linspace(0, compresion_maxima, 100)
        trabajos = [resorte.trabajo_compresion(0, x) for x in compresiones]
        energias = [resorte.energia_potencial(x) for x in compresiones]
        fuerzas = [-resorte.fuerza_resorte(x) for x in compresiones]
        
        # Crear subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Gráfico 1: Trabajo
        ax1.plot(compresiones, trabajos, 'b-', linewidth=2, label='Trabajo realizado')
        ax1.fill_between(compresiones, trabajos, alpha=0.3, color='blue')
        ax1.set_xlabel('Compresión (m)')
        ax1.set_ylabel('Trabajo (J)')
        ax1.set_title('Trabajo para comprimir el resorte')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Gráfico 2: Energía
        ax2.plot(compresiones, energias, 'r-', linewidth=2, label='Energía potencial')
        ax2.fill_between(compresiones, energias, alpha=0.3, color='red')
        ax2.set_xlabel('Compresión (m)')
        ax2.set_ylabel('Energía (J)')
        ax2.set_title('Energía potencial almacenada')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Gráfico 3: Fuerza
        ax3.plot(compresiones, fuerzas, 'g-', linewidth=2, label='Fuerza aplicada')
        ax3.fill_between(compresiones, fuerzas, alpha=0.3, color='green')
        ax3.set_xlabel('Compresión (m)')
        ax3.set_ylabel('Fuerza (N)')
        ax3.set_title('Fuerza necesaria para comprimir')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Gráfico 4: Comparación
        ax4.plot(compresiones, trabajos, 'b-', linewidth=2, label='Trabajo')
        ax4.plot(compresiones, energias, 'r--', linewidth=2, label='Energía')
        ax4.set_xlabel('Compresión (m)')
        ax4.set_ylabel('Energía/Trabajo (J)')
        ax4.set_title('Comparación: Trabajo vs Energía')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Explicación
        with st.expander("📝 Explicación de los gráficos"):
            st.markdown("""
            **Interpretación física:**
            - **Trabajo**: Energía que gastas para comprimir el resorte
            - **Energía potencial**: Energía que el resorte almacena
            - **Fuerza**: Esfuerzo necesario en cada punto
            
            **¡En un resorte ideal, el trabajo realizado es igual a la energía almacenada!**
            """)
    
    with tab2:
        st.header("Cálculo de Trabajo Específico")
        
        # Calcular valores específicos
        trabajo = resorte.trabajo_compresion(x_inicial, x_final)
        fuerza_inicial = -resorte.fuerza_resorte(x_inicial)
        fuerza_final = -resorte.fuerza_resorte(x_final)
        energia_final = resorte.energia_potencial(x_final)
        
        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Parámetros de Entrada")
            st.write(f"**Compresión inicial:** {x_inicial} m")
            st.write(f"**Compresión final:** {x_final} m")
            st.write(f"**Constante k:** {k} N/m")
        
        with col2:
            st.subheader("📊 Resultados")
            st.metric("Trabajo realizado", f"{trabajo:.4f} J")
            st.metric("Fuerza inicial", f"{fuerza_inicial:.2f} N")
            st.metric("Fuerza final", f"{fuerza_final:.2f} N")
            st.metric("Energía almacenada", f"{energia_final:.4f} J")
        
        # Gráfico específico
        fig, ax = plt.subplots(figsize=(10, 6))
        compresiones_especificas = np.linspace(x_inicial, x_final, 50)
        trabajos_especificos = [resorte.trabajo_compresion(x_inicial, x) for x in compresiones_especificas]
        
        ax.plot(compresiones_especificas, trabajos_especificos, 'purple', linewidth=3, 
                label=f'Trabajo de {x_inicial}m a {x_final}m')
        ax.fill_between(compresiones_especificas, trabajos_especificos, alpha=0.3, color='purple')
        ax.set_xlabel('Compresión (m)')
        ax.set_ylabel('Trabajo acumulado (J)')
        ax.set_title(f'Trabajo para comprimir de {x_inicial}m a {x_final}m')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
    
    with tab3:
        st.header("Representación Física del Resorte")
        
        # Control deslizante para compresión actual
        compresion_actual = st.slider(
            "Compresión actual",
            min_value=0.0,
            max_value=compresion_maxima,
            value=0.3,
            step=0.01,
            key="comp_actual"
        )
        
        # Calcular valores para esta compresión
        trabajo_actual = resorte.trabajo_compresion(0, compresion_actual)
        fuerza_actual = -resorte.fuerza_resorte(compresion_actual)
        energia_actual = resorte.energia_potencial(compresion_actual)
        
        # Mostrar métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Trabajo realizado", f"{trabajo_actual:.2f} J")
        with col2:
            st.metric("Fuerza actual", f"{fuerza_actual:.2f} N")
        with col3:
            st.metric("Energía almacenada", f"{energia_actual:.2f} J")
        
        # Dibujar resorte
        fig_resorte = resorte._dibujar_resorte(compresion_actual)
        st.pyplot(fig_resorte)
        
        # Explicación del estado actual
        st.info(f"""
        **Estado actual del resorte:**
        - **Compresión:** {compresion_actual:.2f} m ({compresion_actual/longitud_natural*100:.1f}% de la longitud natural)
        - **Longitud actual:** {longitud_natural - compresion_actual:.2f} m
        - **Energía lista para liberar:** {energia_actual:.2f} J
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "**🔬 Simulador de Física - Ley de Hooke y Cálculo Integral** • "
        "Creado con Streamlit, NumPy y Matplotlib"
    )

if __name__ == "__main__":
    main()
    )

if __name__ == "__main__":
    main()

