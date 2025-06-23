#ifndef FIR_941HZ_H
#define FIR_941HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA 941 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 11
// Ventana utilizada: hamming
// Número de coeficientes: 11

#define FILTER_FREQUENCY 941
#define FILTER_LENGTH 11
#define FILTER_ORDER 11

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {
     -0.02485014f,  -0.06026106f,  -0.08754275f,   0.02306547f,   0.24633931f,   0.36540459f,   0.24633931f,   0.02306547f, 
     -0.08754275f,  -0.06026106f,  -0.02485014f

};

#endif // FIR_941HZ_H
