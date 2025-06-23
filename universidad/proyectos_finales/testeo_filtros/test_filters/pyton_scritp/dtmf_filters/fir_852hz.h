#ifndef FIR_852HZ_H
#define FIR_852HZ_H

//==============================================================================
// FILTRO FIR PASABANDA PARA 852 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 11
// Ventana utilizada: hamming
// Número de coeficientes: 11

#define FILTER_FREQUENCY 852
#define FILTER_LENGTH 11
#define FILTER_ORDER 11

// Coeficientes del filtro FIR
const float filter_coeffs[FILTER_LENGTH] = {
     -0.02838305f,  -0.05437077f,  -0.06098785f,   0.05696913f,   0.25935835f,   0.36252567f,   0.25935835f,   0.05696913f, 
     -0.06098785f,  -0.05437077f,  -0.02838305f

};

#endif // FIR_852HZ_H
