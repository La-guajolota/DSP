/**
 * @file main.cpp
 * @brief Sistema de detección de frecuencias DTMF utilizando filtros FIR/IIR en Arduino.
 * 
 * Este programa implementa un sistema de detección de frecuencias DTMF (Dual-Tone Multi-Frequency)
 * utilizando filtros digitales FIR o IIR. El sistema permite seleccionar un filtro específico
 * para detectar una frecuencia objetivo (como las frecuencias DTMF estándar) y reporta la detección
 * a través del puerto serial. El programa está diseñado para ejecutarse en un Arduino y utiliza
 * un micrófono (como el KY-038) para capturar señales de audio.
 * 
 * ### Características principales:
 * - **Filtros FIR/IIR**: Se pueden incluir filtros FIR o IIR para detectar frecuencias específicas.
 * - **Frecuencia de muestreo**: Configurable (por defecto, 8000 Hz).
 * - **Detección de frecuencia**: Basada en un umbral de energía configurable.
 * - **Salida serial**: Reporta la detección de frecuencias y valores de energía en tiempo real.
 * 
 * ### Configuración:
 * - Descomenta el archivo de filtro FIR o IIR correspondiente en la sección de configuración.
 * - Asegúrate de incluir los coeficientes del filtro en un archivo de encabezado (`.h`).
 * - Conecta el micrófono al pin analógico configurado (`audioInPin`).
 
 * ### Ejemplo de salida serial:
 * ```
 * === Sistema de Detección DTMF con Filtros Digitales ===
 * Frecuencia objetivo: 697 Hz
 * Tipo de filtro: FIR (Orden: 31)
 * Frecuencia de muestreo: 8000 Hz
 * Umbral de detección: 30.0
 * Iniciando detección...
 * 
 * Muestra: 100 | Entrada: 0.0123V | Salida filtro: 0.0456 | Energía: 0.0021 | Frecuencia 697 Hz: DETECTADA ✓
 * 
 * *** FRECUENCIA 697 Hz DETECTADA! ***
 * ```
 * 
 * ### Notas:
 * - Este programa está diseñado para pruebas y demostraciones de detección de frecuencias.
 * 
 * @author Adrian Silva Palafox
 * @date Junio 2025
 */
#include <Arduino.h>

//==============================================================================
// CONFIGURACIÓN DE FILTROS - DESCOMENTA EL QUE QUIERAS USAR
//==============================================================================

// Filtros FIR (descomenta uno)
// #include "fir_697hz.h"     // Filtro FIR para 697 Hz
// #include "fir_770hz.h"     // Filtro FIR para 770 Hz
// #include "fir_852hz.h"     // Filtro FIR para 852 Hz
// #include "fir_941hz.h"     // Filtro FIR para 941 Hz
// #include "fir_1209hz.h"    // Filtro FIR para 1209 Hz
// #include "fir_1336hz.h"    // Filtro FIR para 1336 Hz
// #include "fir_1477hz.h"    // Filtro FIR para 1477 Hz
#include "fir_1633hz.h"    // Filtro FIR para 1633 Hz

// Filtros IIR (descomenta uno)
// #include "iir_697hz.h"     // Filtro IIR para 697 Hz
// #include "iir_770hz.h"     // Filtro IIR para 770 Hz
// #include "iir_852hz.h"     // Filtro IIR para 852 Hz
// #include "iir_941hz.h"     // Filtro IIR para 941 Hz
// #include "iir_1209hz.h"    // Filtro IIR para 1209 Hz
// #include "iir_1336hz.h"    // Filtro IIR para 1336 Hz
// #include "iir_1477hz.h"    // Filtro IIR para 1477 Hz
// #include "iir_1633hz.h"    // Filtro IIR para 1633 Hz

//==============================================================================
// CONFIGURACIÓN DEL SISTEMA
//==============================================================================

// Pines de entrada y configuración
const int audioInPin = A0;              // Pin analógico para entrada de audio (micrófono KY-038)
const int sampleRate = 8000;            // Frecuencia de muestreo en Hz
const unsigned long samplePeriod = 1000000 / sampleRate; // Período en microsegundos

// Variables para temporización
unsigned long lastSampleTime = 0;

// Configuración de detección
const float DETECTION_THRESHOLD = 30.0;  // Umbral empírico para detección
const int DETECTION_BUFFER_SIZE = 100;   // Número de muestras para promediar detección
int detectionBuffer[DETECTION_BUFFER_SIZE] = {0};
int detectionIndex = 0;
unsigned long detectionCount = 0;

//==============================================================================
// VARIABLES PARA FILTROS FIR
//==============================================================================
#ifdef FILTER_LENGTH
// Buffer circular para muestras de entrada (filtros FIR)
float firSamples[FILTER_LENGTH] = {0.0};
int firSampleIndex = 0;
#endif

//==============================================================================
// VARIABLES PARA FILTROS IIR
//==============================================================================
#ifdef IIR_ORDER
// Buffers para filtros IIR (entrada y salida)
float iirInputBuffer[IIR_ORDER + 1] = {0.0};
float iirOutputBuffer[IIR_ORDER + 1] = {0.0};
int iirBufferIndex = 0;
#endif

//==============================================================================
// FUNCIONES DE FILTRADO
//==============================================================================

#ifdef FILTER_LENGTH
/**
 * @brief Aplica filtro FIR a la muestra actual
 * @param inputSample Muestra de entrada
 * @return Valor filtrado
 */
float applyFIRFilter(float inputSample) {
    // Almacenar muestra en buffer circular
    firSamples[firSampleIndex] = inputSample;
    
    // Calcular salida del filtro FIR
    float output = 0.0;
    for (int i = 0, index = firSampleIndex; i < FILTER_LENGTH; i++) {
        output += filter_coeffs[i] * firSamples[index];
        index = (index > 0) ? index - 1 : FILTER_LENGTH - 1;
    }
    
    // Actualizar índice del buffer circular
    firSampleIndex = (firSampleIndex + 1) % FILTER_LENGTH;
    
    return output;
}
#endif

#ifdef IIR_ORDER
/**
 * @brief Aplica filtro IIR a la muestra actual
 * @param inputSample Muestra de entrada
 * @return Valor filtrado
 */
float applyIIRFilter(float inputSample) {
    // Rotar buffers
    for (int i = IIR_ORDER; i > 0; i--) {
        iirInputBuffer[i] = iirInputBuffer[i-1];
        iirOutputBuffer[i] = iirOutputBuffer[i-1];
    }
    
    // Nueva muestra de entrada
    iirInputBuffer[0] = inputSample;
    
    // Calcular nueva salida
    float output = 0.0;
    
    // Parte feedforward (coeficientes b)
    for (int i = 0; i <= IIR_ORDER; i++) {
        output += b_coeffs[i] * iirInputBuffer[i];
    }
    
    // Parte feedback (coeficientes a, excluyendo a[0])
    for (int i = 1; i <= IIR_ORDER; i++) {
        output -= a_coeffs[i] * iirOutputBuffer[i];
    }
    
    // Normalizar por a[0] (usualmente 1.0)
    output /= a_coeffs[0];
    
    // Almacenar nueva salida
    iirOutputBuffer[0] = output;
    
    return output;
}
#endif

/**
 * @brief Detecta si hay energía significativa en la banda de frecuencia del filtro
 * @param filteredValue Valor de salida del filtro
 * @return true si se detecta la frecuencia objetivo
 */
bool detectFrequency(float filteredValue) {
    // Calcular energía (magnitud al cuadrado)
    float energy = filteredValue * filteredValue;
    
    // Actualizar buffer de detección con promedio móvil
    detectionBuffer[detectionIndex] = (energy > DETECTION_THRESHOLD) ? 1 : 0;
    detectionIndex = (detectionIndex + 1) % DETECTION_BUFFER_SIZE;
    
    // Calcular promedio de detecciones
    int detectionSum = 0;
    for (int i = 0; i < DETECTION_BUFFER_SIZE; i++) {
        detectionSum += detectionBuffer[i];
    }
    
    // Se considera detectada si más del 70% de las muestras recientes superan el umbral
    return (detectionSum > (DETECTION_BUFFER_SIZE * 0.7));
}

/**
 * @brief Obtiene el nombre de la frecuencia actual basado en el archivo incluido
 * @return String con el nombre de la frecuencia
 */
String getCurrentFrequencyName() {
    #ifdef FILTER_FREQUENCY
        return String(FILTER_FREQUENCY) + " Hz";
    #else
        return "Desconocida";
    #endif
}

/**
 * @brief Obtiene el tipo de filtro actual
 * @return String con el tipo de filtro
 */
String getFilterType() {
    #ifdef FILTER_LENGTH
        return "FIR (Orden: " + String(FILTER_ORDER) + ")";
    #elif defined(IIR_ORDER)
        return "IIR (Orden: " + String(IIR_ORDER) + ")";
    #else
        return "No definido";
    #endif
}

//==============================================================================
// CONFIGURACIÓN INICIAL
//==============================================================================
void setup() {
    Serial.begin(115200);
    
    // Configurar pin de entrada
    pinMode(audioInPin, INPUT);
    
    // Mensaje de inicio
    Serial.println("=== Sistema de Detección DTMF con Filtros Digitales ===");
    Serial.println("Frecuencia objetivo: " + getCurrentFrequencyName());
    Serial.println("Tipo de filtro: " + getFilterType());
    Serial.println("Frecuencia de muestreo: " + String(sampleRate) + " Hz");
    Serial.println("Umbral de detección: " + String(DETECTION_THRESHOLD));
    Serial.println("Iniciando detección...\n");
    
    delay(2000); // Esperar estabilización
}

//==============================================================================
// BUCLE PRINCIPAL
//==============================================================================
void loop() {
    unsigned long currentTime = micros();
    
    // Verificar si es tiempo de tomar una nueva muestra
    if (currentTime - lastSampleTime >= samplePeriod) {
        lastSampleTime = currentTime;
        
        // Leer muestra de audio y normalizar (centrar en cero)
        int rawSample = analogRead(audioInPin);
        float normalizedSample = (rawSample - 512) * (3.3 / 1024.0); // Convertir a voltaje y centrar
        
        // Aplicar filtro según el tipo definido
        float filteredOutput = 0.0;
        
        #ifdef FILTER_LENGTH
            // Usar filtro FIR
            filteredOutput = applyFIRFilter(normalizedSample);
        #elif defined(IIR_ORDER)
            // Usar filtro IIR
            filteredOutput = applyIIRFilter(normalizedSample);
        #else
            #error "No se ha definido ningún filtro. Incluye un archivo de coeficientes FIR o IIR."
        #endif
        
        // Detectar frecuencia objetivo
        bool frequencyDetected = detectFrequency(filteredOutput);
        
        // Enviar resultados por serial cada cierto número de muestras
        detectionCount++;
        if (detectionCount % 100 == 0) { // Cada 100 muestras (cada ~12.5ms a 8kHz)
            Serial.print("Muestra: ");
            Serial.print(detectionCount);
            Serial.print(" | Entrada: ");
            Serial.print(normalizedSample, 4);
            Serial.print("V | Salida filtro: ");
            Serial.print(filteredOutput, 4);
            Serial.print(" | Energía: ");
            Serial.print(filteredOutput * filteredOutput, 4);
            Serial.print(" | Frecuencia " + getCurrentFrequencyName() + ": ");
            Serial.println(frequencyDetected ? "DETECTADA ✓" : "No detectada");
        }
        
        // Mostrar detección prominente cuando se encuentra la frecuencia
        static bool lastDetectionState = false;
        if (frequencyDetected && !lastDetectionState) {
            Serial.println("\n*** FRECUENCIA " + getCurrentFrequencyName() + " DETECTADA! ***\n");
        } else if (!frequencyDetected && lastDetectionState) {
            Serial.println("\n--- Frecuencia " + getCurrentFrequencyName() + " perdida ---\n");
        }
        lastDetectionState = frequencyDetected;
    }
}
