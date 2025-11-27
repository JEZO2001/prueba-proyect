import matplotlib.pyplot as plt


def crear_grafica_pv(presiones, valores, nombre_eje_y, titulo):
    """
    Genera una gráfica de Matplotlib y devuelve el objeto figura.
    """
    fig, ax = plt.figure(figsize=(8, 5)), plt.gca()

    ax.plot(presiones, valores, linewidth=2, color='#1f77b4', label=nombre_eje_y)

    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel("Presión (psia)", fontsize=12)
    ax.set_ylabel(nombre_eje_y, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    # Añadir línea vertical indicando Pb (opcional, visualmente útil)
    # Si quisieras marcar el Pb, necesitarías pasarlo como argumento.

    plt.tight_layout()
    return fig