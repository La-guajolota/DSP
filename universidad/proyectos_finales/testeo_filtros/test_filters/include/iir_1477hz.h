#ifndef IIR_1477HZ_H
#define IIR_1477HZ_H

//==============================================================================
// FILTRO IIR PASABANDA PARA 1477 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:26:27
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 3
// Tipo de filtro: butter

#define FILTER_FREQUENCY 1477
#define IIR_ORDER 3

// Coeficientes del denominador (feedback) - polos
const float a_coeffs[IIR_ORDER + 1] = {
      1.00000000f,    // a[0]
     -2.37720357f,    // a[1]
      4.83663411f,    // a[2]
     -5.17761133f,    // a[3]
      4.76125430f,    // a[4]
     -2.30367982f,    // a[5]
      0.95396816f    // a[6]
};

// Coeficientes del numerador (feedforward) - zeros
const float b_coeffs[IIR_ORDER + 1] = {
      0.00000160f,    // b[0]
      0.00000000f,    // b[1]
     -0.00000479f,    // b[2]
      0.00000000f,    // b[3]
      0.00000479f,    // b[4]
      0.00000000f,    // b[5]
     -0.00000160f    // b[6]

};

#endif // IIR_1477HZ_H
