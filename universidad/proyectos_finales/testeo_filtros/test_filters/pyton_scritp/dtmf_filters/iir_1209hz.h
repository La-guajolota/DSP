#ifndef IIR_1209HZ_H
#define IIR_1209HZ_H

//==============================================================================
// FILTRO IIR PASABANDA PARA 1209 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:26:27
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 3
// Tipo de filtro: butter

#define FILTER_FREQUENCY 1209
#define IIR_ORDER 3

// Coeficientes del denominador (feedback) - polos
const float a_coeffs[IIR_ORDER + 1] = {
      1.00000000f,    // a[0]
     -3.46512461f,    // a[1]
      6.95536324f,    // a[2]
     -8.36292165f,    // a[3]
      6.84696035f,    // a[4]
     -3.35795292f,    // a[5]
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

#endif // IIR_1209HZ_H
