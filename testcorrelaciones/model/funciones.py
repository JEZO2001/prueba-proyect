import math


# --- 1. PRESIÓN DE BURBUJA (Pb) ---
def standing_pb(Rs, yg, API, T):
    """
    Calcula la Presión de Burbuja usando Standing (1947).
    Fuente: PDF Página 20 [cite: 467]
    T en Fahrenheit.
    """
    # a = 0.00091(T) - 0.0125(API)
    a = 0.00091 * T - 0.0125 * API

    # Pb = 18.2 * [(Rs/yg)^0.83 * 10^(a - 1.4)]
    term1 = (Rs / yg) ** 0.83
    term2 = 10 ** (a - 1.4)
    pb = 18.2 * (term1 * term2)
    return pb


# --- 2. SOLUBILIDAD DEL GAS (Rs) ---
def standing_rs(P, yg, API, T):
    """
    Calcula la Solubilidad del Gas (Rs) usando Standing (1947).
    Fuente: PDF Página 25 [cite: 542]
    """
    # x = 0.0125*API - 0.00091*T
    x = 0.0125 * API - 0.00091 * T

    # Rs = yg * [((P/18.2) + 1.4) * 10^x]^1.2048
    term_inner = (P / 18.2) + 1.4
    rs = yg * (term_inner * (10 ** x)) ** 1.2048
    return rs


# --- 3. FACTOR VOLUMÉTRICO DEL PETRÓLEO (Bo) ---
def standing_bo_saturado(Rs, yg, yo, T):
    """
    Calcula Bo para petróleo SATURADO usando Standing (1981).
    Fuente: PDF Página 33
    """
    # Bo = 0.9759 + 0.000120 * [Rs * (yg/yo)^0.5 + 1.25*T]^1.2
    term_inner = Rs * ((yg / yo) ** 0.5) + 1.25 * T
    bo = 0.9759 + 0.000120 * (term_inner ** 1.2)
    return bo


def bo_undersaturated(Bob, Co, Pb, P):
    """
    Calcula Bo para petróleo SUBSATURADO (P > Pb).
    Fuente: PDF Página 37 [cite: 761]
    Formula: Bo = Bob * exp(Co * (Pb - P)) (Nota: PDF dice Pb-P, usualmente es P-Pb para compresibilidad,
    pero seguimos la fuente del PDF que usa el exponente para ajustar el volumen).
    """
    import math
    # Bo = Bob * e^(Co * (Pb - P))
    # Nota: Verifica el signo en tu clase, a veces es exp(Co*(Pb - P)) para indicar que el volumen se reduce al aumentar P.
    bo = Bob * math.exp(Co * (Pb - P))
    return bo