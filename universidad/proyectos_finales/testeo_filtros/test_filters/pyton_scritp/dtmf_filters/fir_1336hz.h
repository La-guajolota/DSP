#ifndef FIR_1336HZ_H
#define FIR_1336HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA 1336 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 11
// Ventana utilizada: hamming
// Número de coeficientes: 11

#define FILTER_FREQUENCY 1336
#define FILTER_LENGTH 11
#define FILTER_ORDER 11

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {
      0.01497870f,  -0.03042671f,  -0.14638779f,  -0.12642302f,   0.16723533f,   0.36802906f,   0.16723533f,  -0.12642302f, 
     -0.14638779f,  -0.03042671f,   0.01497870f

};

#endif // FIR_1336HZ_H
