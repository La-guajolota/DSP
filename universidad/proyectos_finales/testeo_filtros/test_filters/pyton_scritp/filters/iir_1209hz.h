#ifndef IIR_1209HZ_H
#define IIR_1209HZ_H

//==============================================================================
// FILTRO IIR PASABANDA PARA 1209 Hz
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:05
// Frecuencia de muestreo: 8000 Hz
// Orden del filtro: 2
// Tipo de filtro: butter

#define FILTER_FREQUENCY 1209
#define IIR_ORDER 2

// Coeficientes del denominador (feedback) - polos
const float a_coeffs[IIR_ORDER + 1] = {
      1.00000000f,    // a[0]
     -2.30897511f,    // a[1]
      3.29961388f,    // a[2]
     -2.27082178f,    // a[3]
      0.96722743f    // a[4]
};

// Coeficientes del numerador (feedforward) - zeros
const float b_coeffs[IIR_ORDER + 1] = {
      0.00013651f,    // b[0]
      0.00000000f,    // b[1]
     -0.00027302f,    // b[2]
      0.00000000f,    // b[3]
      0.00013651f    // b[4]

};

#endif // IIR_1209HZ_H
