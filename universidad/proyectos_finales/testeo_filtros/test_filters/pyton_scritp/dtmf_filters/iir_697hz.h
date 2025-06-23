#ifndef IIR_697HZ_H
#define IIR_697HZ_H

//==============================================================================
// FILTRO IIR PASABANDA PARA 697 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:26:27
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 3
// Tipo de filtro: butter

#define FILTER_FREQUENCY 697
#define IIR_ORDER 3

// Coeficientes del denominador (feedback) - polos
const float a_coeffs[IIR_ORDER + 1] = {
      1.00000000f,    // a[0]
     -5.08332949f,    // a[1]
     11.56655521f,    // a[2]
    -14.87301282f,    // a[3]
     11.38628104f,    // a[4]
     -4.92610888f,    // a[5]
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

#endif // IIR_697HZ_H
