#ifndef FIR_1633HZ_H
#define FIR_1633HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA 1633 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 11
// Ventana utilizada: hamming
// Número de coeficientes: 11

#define FILTER_FREQUENCY 1633
#define FILTER_LENGTH 11
#define FILTER_ORDER 11

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {
      0.02852556f,   0.02449678f,  -0.10889811f,  -0.20574740f,   0.09328956f,   0.35979274f,   0.09328956f,  -0.20574740f, 
     -0.10889811f,   0.02449678f,   0.02852556f

};

#endif // FIR_1633HZ_H
