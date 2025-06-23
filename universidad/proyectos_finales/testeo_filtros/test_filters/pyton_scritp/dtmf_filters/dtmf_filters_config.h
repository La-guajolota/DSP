#ifndef DTMF_FILTERS_CONFIG_H
#define DTMF_FILTERS_CONFIG_H

//==============================================================================
// CONFIGURACIÓN DE FILTROS DTMF
//==============================================================================
// Generado automáticamente el 2025-06-22 21:28:23
// Frecuencias DTMF disponibles: 697, 770, 852, 941, 1209, 1336, 1477, 1633 Hz

// Para usar un filtro específico, descomenta UNA de las siguientes líneas:

// #include "fir_697hz.h"     // Filtro FIR para 697 Hz
// #include "fir_770hz.h"     // Filtro FIR para 770 Hz
// #include "fir_852hz.h"     // Filtro FIR para 852 Hz
// #include "fir_941hz.h"     // Filtro FIR para 941 Hz
// #include "fir_1209hz.h"     // Filtro FIR para 1209 Hz
// #include "fir_1336hz.h"     // Filtro FIR para 1336 Hz
// #include "fir_1477hz.h"     // Filtro FIR para 1477 Hz
// #include "fir_1633hz.h"     // Filtro FIR para 1633 Hz

// Ejemplo de uso en main.cpp:
// 1. Incluye este archivo: #include "dtmf_filters_config.h"
// 2. Descomenta el filtro que desees usar arriba
// 3. Compila y carga a tu ESP32

#endif // DTMF_FILTERS_CONFIG_H
