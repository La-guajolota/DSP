#ifndef FIR_770HZ_H
#define FIR_770HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA 770 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 11
// Ventana utilizada: hamming
// Número de coeficientes: 11

#define FILTER_FREQUENCY 770
#define FILTER_LENGTH 11
#define FILTER_ORDER 11

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {
     -0.02837990f,  -0.04498676f,  -0.03427492f,   0.08617667f,   0.26819961f,   0.35743154f,   0.26819961f,   0.08617667f, 
     -0.03427492f,  -0.04498676f,  -0.02837990f

};

#endif // FIR_770HZ_H
