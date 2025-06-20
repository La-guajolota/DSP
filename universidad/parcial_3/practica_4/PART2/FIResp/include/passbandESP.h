// recuencia de muestreo (Hz): 6666
// Frecuencia de corte inferior (Hz): 200
// Frecuencia de corte superior (Hz): 250
// Orden del filtro: 31
// Tipo de ventana (rectangular, hanning, hamming, blackman): hamming

const float filter_coeffs[] = {
    -0.0011349724,    -0.0013041142,    -0.0016691340,    -0.0021563960,
    -0.0026293532,    -0.0029131377,    -0.0028275073,    -0.0022225072,
    -0.0010106533,    0.0008100707,    0.0031466461,    0.0058169284,
    0.0085705196,    0.0111215798,    0.0131885349,    0.0145344294,
    0.0150015002,    0.0145344294,    0.0131885349,    0.0111215798,
    0.0085705196,    0.0058169284,    0.0031466461,    0.0008100707,
    -0.0010106533,    -0.0022225072,    -0.0028275073,    -0.0029131377,
    -0.0026293532,    -0.0021563960,    -0.0016691340,    -0.0013041142,
    -0.0011349724
};

const int FILTER_ORDER = 32;
const int FILTER_LENGTH = 33;
