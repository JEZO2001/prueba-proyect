import xlwings as xw
import numpy as np
from testcorrelaciones.model import funciones
from testcorrelaciones.model import graficas


def main():
    # 1. Conexión con el libro de Excel
    wb = xw.Book.caller()
    sheet = wb.sheets[0]  # Trabajamos en la primera hoja

    try:
        # ---------------------------------------------------------
        # 2. LECTURA DE DATOS (INPUTS)
        # Asume que los datos están en la columna B
        # ---------------------------------------------------------
        # Temperatura del sistema (Fahrenheit)
        T = sheet.range('B4').value
        # Gravedad API del petróleo
        API = sheet.range('B5').value
        # Gravedad específica del gas (yg)
        yg = sheet.range('B6').value
        # Gravedad específica del petróleo (yo) - Opcional si se calcula con API
        yo = sheet.range('B7').value
        # Solubilidad del gas actual o de prueba (Rs) en scf/STB
        Rs_input = sheet.range('B8').value
        # Presión máxima del reservorio para la gráfica (psia)
        P_res = sheet.range('B9').value

        # Validación simple de datos
        if None in [T, API, yg, Rs_input, P_res]:
            sheet.range('D4').value = "Error: Faltan datos de entrada en la columna B."
            return

        # ---------------------------------------------------------
        # 3. CÁLCULOS (Llamando a funciones.py)
        # ---------------------------------------------------------

        # A) Calcular Presión de Burbuja (Pb) usando Standing
        # Fuente: Correlación de Standing Pb [cite: 467]
        Pb = funciones.standing_pb(Rs_input, yg, API, T)

        # Enviar resultado numérico a Excel
        sheet.range('B12').value = Pb  # Celda donde aparecerá el Pb calculado

        # B) Generar barrido de presiones para las gráficas
        # Crea 50 puntos desde 14.7 psi hasta la presión del reservorio
        presiones = np.linspace(14.7, P_res, 50)

        valores_rs = []
        valores_bo = []

        # C) Loop para calcular propiedades en cada presión
        for p in presiones:
            # --- Cálculo de Rs (Solubilidad) ---
            if p < Pb:
                # Si P < Pb, el gas se libera, Rs disminuye. Standing Rs [cite: 542]
                rs_calc = funciones.standing_rs(p, yg, API, T)
            else:
                # Si P >= Pb, el Rs es constante (todo el gas está disuelto)
                rs_calc = Rs_input
            valores_rs.append(rs_calc)

            # --- Cálculo de Bo (Factor Volumétrico) ---
            if p < Pb:
                # Zona Saturada (Standing) [cite: 702]
                bo_calc = funciones.standing_bo_saturado(rs_calc, yg, yo, T)
            else:
                # Zona Subsaturada (P > Pb)
                # Primero calculamos Bo en el punto de burbuja
                Bob = funciones.standing_bo_saturado(Rs_input, yg, yo, T)
                # Compresibilidad (Co) - Usando Vasquez-Beggs como ejemplo [cite: 638]
                # Nota: Para simplificar aquí usaremos un Co promedio,
                # pero idealmente deberías llamar a funciones.vasquez_beggs_co(...)
                Co = 0.000015

                # Fórmula subsaturada [cite: 761]
                import math
                bo_calc = Bob * math.exp(
                    Co * (Pb - p))  # Nota: revisar signo según convención
            valores_bo.append(bo_calc)

        # ---------------------------------------------------------
        # 4. GRAFICACIÓN (Llamando a graficas.py)
        # ---------------------------------------------------------

        # Crear gráfica de Rs vs Presión
        fig_rs = graficas.crear_grafica_pv(
            presiones,
            valores_rs,
            "Rs (scf/STB)",
            "Solubilidad del Gas vs Presión"
        )

        # Crear gráfica de Bo vs Presión
        fig_bo = graficas.crear_grafica_pv(
            presiones,
            valores_bo,
            "Bo (bbl/STB)",
            "Factor Volumétrico vs Presión"
        )

        # ---------------------------------------------------------
        # 5. SALIDA VISUAL A EXCEL
        # ---------------------------------------------------------

        # Pegar gráfica de Rs
        sheet.pictures.add(
            fig_rs,
            name='Plot_Rs',
            update=True,
            left=sheet.range('E4').left,
            top=sheet.range('E4').top,
            scale=0.8
        )

        # Pegar gráfica de Bo
        sheet.pictures.add(
            fig_bo,
            name='Plot_Bo',
            update=True,
            left=sheet.range('E25').left,  # Más abajo
            top=sheet.range('E25').top,
            scale=0.8
        )

        sheet.range('D4').value = "Cálculo completado exitosamente."

    except Exception as e:
        sheet.range('D4').value = f"Error en Python: {str(e)}"


# Bloque para probar localmente sin abrir Excel (mock caller)
if __name__ == "__main__":
    xw.Book("testdoftwaree.xlsm").set_mock_caller()
    main()