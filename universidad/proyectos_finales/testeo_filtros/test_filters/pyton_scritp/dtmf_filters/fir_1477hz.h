#ifndef FIR_1477HZ_H
#define FIR_1477HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA 1477 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 11
// Ventana utilizada: hamming
// Número de coeficientes: 11

#define FILTER_FREQUENCY 1477
#define FILTER_LENGTH 11
#define FILTER_ORDER 11

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {
      0.02566683f,  -0.00439100f,  -0.13600551f,  -0.16840290f,   0.13202680f,   0.36249132f,   0.13202680f,  -0.16840290f, 
     -0.13600551f,  -0.00439100f,   0.02566683f

};

#endif // FIR_1477HZ_H
