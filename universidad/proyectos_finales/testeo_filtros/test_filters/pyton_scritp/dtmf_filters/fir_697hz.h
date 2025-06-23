#ifndef FIR_697HZ_H
#define FIR_697HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA 697 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 11
// Ventana utilizada: hamming
// Número de coeficientes: 11

#define FILTER_FREQUENCY 697
#define FILTER_LENGTH 11
#define FILTER_ORDER 11

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {
     -0.02562321f,  -0.03393353f,  -0.00990209f,   0.10894631f,   0.27150666f,   0.34860540f,   0.27150666f,   0.10894631f, 
     -0.00990209f,  -0.03393353f,  -0.02562321f

};

#endif // FIR_697HZ_H
