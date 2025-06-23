#ifndef FIR_1209HZ_H
#define FIR_1209HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA 1209 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 11
// Ventana utilizada: hamming
// Número de coeficientes: 11

#define FILTER_FREQUENCY 1209
#define FILTER_LENGTH 11
#define FILTER_ORDER 11

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {
      0.00104646f,  -0.04922714f,  -0.14105668f,  -0.08146032f,   0.19664735f,   0.37040013f,   0.19664735f,  -0.08146032f, 
     -0.14105668f,  -0.04922714f,   0.00104646f

};

#endif // FIR_1209HZ_H
