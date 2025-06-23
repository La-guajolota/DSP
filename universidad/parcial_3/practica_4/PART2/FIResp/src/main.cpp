#include <Arduino.h>

// Incluir archivo de coeficientes generado por Python
//#include "lowpass15.h" //106us de procesamiento
//#include "lowpass31.h" //130us
// #include "lowpass63.h"   //148us

#include "lowpassESP.h"
//#include "highpassESP.h"
//#include "passbandESP.h"


// Configuración de pines
const int analogInPin = 34; // Pin analógico de entrada (ESP32 ADC pin)
const int dacOutPin = 25;   // Pin de salida DAC (ESP32 DAC pin)

// Buffer circular para almacenar muestras de entrada
float samples[FILTER_LENGTH] = {0.0};
int sampleIndex = 0;

// Variables para temporización
constexpr unsigned long SAMPLE_PERIOD_US = 150; // Período de muestreo en microsegundos (6k666Hz)
unsigned long lastSampleTime = 0;

// Variables para estadísticas
unsigned long sampleCount = 0;
unsigned long processingTime = 0;

void setup() {
    Serial.begin(115200); // Iniciar comunicación serial
    pinMode(dacOutPin, OUTPUT); // Configurar pin DAC como salida

    Serial.println("Filtro FIR iniciado");
    Serial.printf("Orden del filtro: %d\n", FILTER_ORDER);
    Serial.printf("Período de muestreo: %lu us\n", SAMPLE_PERIOD_US);

    delay(1000); // Esperar estabilización
}

void loop() {
    unsigned long currentTime = micros();

    // Verificar si es tiempo de tomar una nueva muestra
    if (currentTime - lastSampleTime >= SAMPLE_PERIOD_US) {
        lastSampleTime = currentTime; // Actualizar tiempo de muestreo

        unsigned long startProcessingTime = micros(); // Inicio del procesamiento

        // Leer valor analógico y convertir a voltaje
        float voltage = analogRead(analogInPin) * (3.3 / 4095.0);

        // Almacenar en el buffer circular
        samples[sampleIndex] = voltage;

        // Aplicar el filtro FIR
        float outputValue = 0.0;
        for (int i = 0, index = sampleIndex; i < FILTER_LENGTH; i++) {
            outputValue += filter_coeffs[i] * samples[index];
            index = (index > 0) ? index - 1 : FILTER_LENGTH - 1;
        }

        // Limitar salida entre 0 y 3.3V y convertir para el DAC
        uint8_t dacValue = constrain(outputValue, 0, 3.3) * (255.0 / 3.3);

        dacWrite(dacOutPin, dacValue); // Enviar al DAC

        sampleIndex = (sampleIndex + 1) % FILTER_LENGTH; // Actualizar índice del buffer

        processingTime = micros() - startProcessingTime; // Calcular tiempo de procesamiento
        sampleCount++; // Incrementar contador de muestras

        // Mostrar estadísticas cada 1000 muestras
        if (sampleCount % 1000 == 0) {
            Serial.printf("Tiempo de procesamiento: %lu us\n", processingTime);
        }
    }
}