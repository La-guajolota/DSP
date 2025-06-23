#ifndef IIR_1633HZ_H
#define IIR_1633HZ_H

//==============================================================================
// FILTRO IIR PASABANDA PARA 1633 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:26:27
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 3
// Tipo de filtro: butter

#define FILTER_FREQUENCY 1633
#define IIR_ORDER 3

// Coeficientes del denominador (feedback) - polos
const float a_coeffs[IIR_ORDER + 1] = {
      1.00000000f,    // a[0]
     -1.69232013f,    // a[1]
      3.90755572f,    // a[2]
     -3.51120689f,    // a[3]
      3.84665679f,    // a[4]
     -1.63997892f,    // a[5]
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

#endif // IIR_1633HZ_H
