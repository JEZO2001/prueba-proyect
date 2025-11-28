import matplotlib.pyplot as plt


def crear_grafica_propiedad(presiones, valores, Pb, nombre_y, titulo):
    """
    Genera gráfica X-Y con línea vertical en Pb.
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Graficar la curva principal
    ax.plot(presiones, valores, linewidth=2, color='blue', label=nombre_y)

    # Agregar línea roja en Pb (Presión de Burbuja)
    ax.axvline(x=Pb, color='red', linestyle='--', linewidth=1.5, label=f'Pb = {Pb} psi')

    ax.set_title(titulo, fontsize=11, fontweight='bold')
    ax.set_xlabel("Presión (psia)")
    ax.set_ylabel(nombre_y)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()

    plt.tight_layout()
    return fig