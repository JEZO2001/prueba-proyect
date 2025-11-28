import xlwings as xw
import pandas as pd
import numpy as np
# Importación absoluta
from testcorrelaciones.model import funciones
from testcorrelaciones.model import graficas


def main():
    wb = xw.Book.caller()

    # 1. DEFINIR HOJAS
    sheet_inputs = wb.sheets.active

    # Manejo de la hoja "Resultados"
    try:
        sheet_results = wb.sheets['Resultados']
        sheet_results.clear()
        for pic in sheet_results.pictures:
            pic.delete()
    except:
        sheet_results = wb.sheets.add('Resultados', after=sheet_inputs)

    try:
        # 2. LEER INPUTS
        Pb_input = sheet_inputs.range('B4').value
        Rsb_input = sheet_inputs.range('B5').value
        API_input = sheet_inputs.range('B6').value
        yg_input = sheet_inputs.range('B7').value
        P_res = sheet_inputs.range('B8').value
        T_input = sheet_inputs.range('B9').value
        P_atm = sheet_inputs.range('B10').value

        if P_atm is None: P_atm = 14.7

        # 3. CÁLCULOS
        yo = funciones.calcular_gamma_o(API_input)
        presiones = funciones.generar_presiones(P_res, P_atm)

        lista_rs, lista_bo, lista_mu, lista_rho, lista_co = [], [], [], [], []

        for p in presiones:
            # --- ZONA SUBSATURADA (P > Pb) ---
            if p > Pb_input:
                rs = Rsb_input
                co = funciones.vasquez_beggs_co(Rsb_input, yg_input, API_input, T_input,
                                                p)

                bob = funciones.standing_bo_saturado(Rsb_input, yg_input, yo, T_input)
                bo = funciones.bo_subsaturado(bob, co, Pb_input, p)

                rho_ob = funciones.standing_densidad_saturado(Rsb_input, yg_input, yo,
                                                              T_input)
                rho = funciones.densidad_subsaturado(rho_ob, co, Pb_input, p)

                mu_od = funciones.beggs_robinson_mu_dead(API_input, T_input)
                mu_ob = funciones.beggs_robinson_mu_saturado(mu_od, Rsb_input)
                mu = funciones.vasquez_beggs_mu_subsaturado(mu_ob, p, Pb_input)

            # --- ZONA SATURADA (P <= Pb) ---
            else:
                rs = funciones.standing_rs(p, yg_input, API_input, T_input)
                co = 0

                bo = funciones.standing_bo_saturado(rs, yg_input, yo, T_input)

                rho = funciones.standing_densidad_saturado(rs, yg_input, yo, T_input)

                mu_od = funciones.beggs_robinson_mu_dead(API_input, T_input)
                mu = funciones.beggs_robinson_mu_saturado(mu_od, rs)

            lista_rs.append(rs)
            lista_bo.append(bo)
            lista_mu.append(mu)
            lista_rho.append(rho)
            lista_co.append(co)

        # 4. EXPORTAR RESULTADOS
        sheet_results.range('A1').value = "Tabla de Resultados PVT"

        df = pd.DataFrame({
            'Presión (psia)': presiones,
            'Rs (scf/STB)': lista_rs,
            'Bo (bbl/STB)': lista_bo,
            'Viscosidad (cp)': lista_mu,
            'Densidad (lb/ft3)': lista_rho,
            'Co (1/psi)': lista_co
        })

        sheet_results.range('A3').value = df

        # 5. GENERAR GRÁFICAS
        # Gráfica Rs
        fig_rs = graficas.crear_grafica_propiedad(presiones, lista_rs, Pb_input,
                                                  "Rs (scf/STB)",
                                                  "Solubilidad vs Presión")
        sheet_results.pictures.add(fig_rs, name='Plot_Rs', update=True,
                                   left=sheet_results.range('H3').left,
                                   top=sheet_results.range('H3').top)

        # Gráfica Bo
        fig_bo = graficas.crear_grafica_propiedad(presiones, lista_bo, Pb_input,
                                                  "Bo (bbl/STB)",
                                                  "Factor Volumétrico vs Presión")
        sheet_results.pictures.add(fig_bo, name='Plot_Bo', update=True,
                                   left=sheet_results.range('H20').left,
                                   top=sheet_results.range('H20').top)

        # Gráfica Viscosidad
        fig_mu = graficas.crear_grafica_propiedad(presiones, lista_mu, Pb_input,
                                                  "Viscosidad (cp)",
                                                  "Viscosidad vs Presión")
        sheet_results.pictures.add(fig_mu, name='Plot_Mu', update=True,
                                   left=sheet_results.range('N3').left,
                                   top=sheet_results.range('N3').top)

        # Gráfica Densidad
        fig_rho = graficas.crear_grafica_propiedad(presiones, lista_rho, Pb_input,
                                                   "Densidad (lb/ft3)",
                                                   "Densidad vs Presión")
        sheet_results.pictures.add(fig_rho, name='Plot_Rho', update=True,
                                   left=sheet_results.range('N20').left,
                                   top=sheet_results.range('N20').top)

        sheet_inputs.range('D4').value = "¡Cálculos listos en hoja Resultados!"
        sheet_results.activate()

    except Exception as e:
        sheet_inputs.range('D4').value = f"Error: {str(e)}"


if __name__ == "__main__":
    xw.Book("testdoftwaree.xlsm").set_mock_caller()
    main()