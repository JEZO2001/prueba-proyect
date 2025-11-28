import numpy as np
import math


# ==========================================
# 1. UTILIDADES
# ==========================================
def generar_presiones(P_res, P_atm):
    """
    Genera un arreglo de presiones desde P_res hasta P_atm
    disminuyendo de 10 en 10 psi.
    """
    # Se usa P_atm - 1 para asegurar que se incluya el valor atmosférico en el rango
    return np.arange(P_res, P_atm - 1, -10)


def calcular_gamma_o(API):
    """Calcula gravedad específica del oil desde API"""
    return 141.5 / (131.5 + API)


# ==========================================
# 2. SOLUBILIDAD DEL GAS (Rs)
# ==========================================
def standing_rs(P, yg, API, T):
    a = 0.00091 * T - 0.0125 * API
    x = 0.0125 * API - 0.00091 * T
    term = (P / 18.2) + 1.4
    rs = yg * (term * (10 ** x)) ** 1.2048
    return rs


# ==========================================
# 3. COMPRESIBILIDAD (Co) - SUBSATURADO
# ==========================================
def vasquez_beggs_co(Rsb, yg, API, T, P, T_sep=100, P_sep=100):
    ygc = yg * (1 + 5.912e-5 * API * T_sep * math.log10(P_sep / 114.7))

    numerator = -1433 + 5 * Rsb + 17.2 * T - 1180 * ygc + 12.61 * API
    denominator = 10 ** 5 * P
    co = numerator / denominator
    return co


# ==========================================
# 4. FACTOR VOLUMÉTRICO (Bo)
# ==========================================
def standing_bo_saturado(Rs, yg, yo, T):
    term = Rs * ((yg / yo) ** 0.5) + 1.25 * T
    bo = 0.9759 + 0.000120 * (term ** 1.2)
    return bo


def bo_subsaturado(Bob, Co, Pb, P):
    return Bob * math.exp(Co * (Pb - P))


# ==========================================
# 5. DENSIDAD DEL PETRÓLEO (rho_o)
# ==========================================
def standing_densidad_saturado(Rs, yg, yo, T):
    num = 62.4 * yo + 0.0136 * Rs * yg
    # Termino del denominador
    term = Rs * ((yg / yo) ** 0.25) + 1.25 * T
    den_val = 0.972 + 0.000147 * (term ** 1.175)

    rho = num / den_val
    return rho


def densidad_subsaturado(rho_ob, Co, Pb, P):
    return rho_ob * math.exp(Co * (P - Pb))


# ==========================================
# 6. VISCOSIDAD DEL PETRÓLEO (mu_o)
# ==========================================
def beggs_robinson_mu_dead(API, T):
    z = 3.0324 - 0.02023 * API
    y = 10 ** z
    x = y * (T ** -1.163)
    mu_od = (10 ** x) - 1.0
    return mu_od


def beggs_robinson_mu_saturado(mu_od, Rs):
    a = 10.715 * ((Rs + 100) ** -0.515)
    b = 5.44 * ((Rs + 150) ** -0.338)
    mu_ob = a * (mu_od ** b)
    return mu_ob


def vasquez_beggs_mu_subsaturado(mu_ob, P, Pb):

    m = 2.6 * (P ** 1.187) * math.exp(-11.513 - 8.98e-5 * P)
    mu = mu_ob * ((P / Pb) ** m)
    return mu