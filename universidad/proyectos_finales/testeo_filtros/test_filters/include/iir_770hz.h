#ifndef IIR_770HZ_H
#define IIR_770HZ_H

//==============================================================================
// FILTRO IIR PASABANDA PARA 770 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:26:27
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 3
// Tipo de filtro: butter

#define FILTER_FREQUENCY 770
#define IIR_ORDER 3

// Coeficientes del denominador (feedback) - polos
const float a_coeffs[IIR_ORDER + 1] = {
      1.00000000f,    // a[0]
     -4.89741784f,    // a[1]
     10.94802376f,    // a[2]
    -13.99246579f,    // a[3]
     10.77739019f,    // a[4]
     -4.74594722f,    // a[5]
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

#endif // IIR_770HZ_H
