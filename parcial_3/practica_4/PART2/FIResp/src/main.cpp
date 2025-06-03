#include <Arduino.h>

// Incluir archivo de coeficientes generado por Python
// Descomentar el filtro que se desea utilizar
#include "lowpass1.h"
//#include "highpass_coeffs.h"
//#include "bandpass_coeffs.h"

// Configuración de pines
const int analogInPin = 34; // Pin analógico de entrada (ESP32 ADC pin)
const int dacOutPin = 25;   // Pin de salida DAC (ESP32 DAC pin)

// Buffer circular para almacenar muestras de entrada
float samples[FILTER_LENGTH];
int sampleIndex = 0;

// Variables para temporización
const unsigned long SAMPLE_PERIOD_US = 1000; // Período de muestreo en microsegundos (1kHz)
unsigned long lastSampleTime = 0;

// Variables para estadísticas
unsigned long sampleCount = 0;
unsigned long processingTime = 0;

void setup() {
    // Iniciar comunicación serial
    Serial.begin(115200);
    
    // Inicializar buffer de muestras
    for (int i = 0; i < FILTER_LENGTH; i++) {
        samples[i] = 0.0;
    }

    // Configurar pin DAC como salida
    pinMode(dacOutPin, OUTPUT);

    Serial.println("Filtro FIR iniciado");
    Serial.print("Orden del filtro: ");
    Serial.println(FILTER_ORDER);
    Serial.print("Período de muestreo: ");
    Serial.print(SAMPLE_PERIOD_US);
    Serial.println(" us");

    // Esperar estabilización
    delay(1000);
}

void loop() {
    unsigned long currentTime = micros();

    // Verificar si es tiempo de tomar una nueva muestra
    if (currentTime - lastSampleTime >= SAMPLE_PERIOD_US) {
        // Guardar tiempo para cálculo de procesamiento
        unsigned long startProcessingTime = micros();

        // Leer valor analógico (0-4095 para ESP32 ADC)
        int sensorValue = analogRead(analogInPin);

        // Convertir a voltaje (0.0-3.3V para ESP32)
        float voltage = sensorValue * (3.3 / 4095.0);

        // Almacenar en el buffer circular
        samples[sampleIndex] = voltage;

        // Aplicar el filtro FIR
        float outputValue = 0.0;
        int index = sampleIndex;

        for (int i = 0; i < FILTER_LENGTH; i++) {
            outputValue += filter_coeffs[i] * samples[index];
            index = (index > 0) ? index - 1 : FILTER_LENGTH - 1;
        }

        // Limitar salida entre 0 y 3.3V
        outputValue = constrain(outputValue, 0.0, 3.3);

        // Convertir a valor para el DAC (0-255 para ESP32 DAC)
        uint8_t dacValue = (uint8_t)(outputValue * 255.0 / 3.3);

        // Enviar al DAC
        dacWrite(dacOutPin, dacValue);

        // Actualizar índice del buffer
        sampleIndex = (sampleIndex + 1) % FILTER_LENGTH;

        // Guardar tiempo de muestreo
        lastSampleTime = currentTime;

        // Calcular tiempo de procesamiento
        processingTime = micros() - startProcessingTime;

        // Incrementar contador de muestras
        sampleCount++;

        // Cada 1000 muestras, mostrar estadísticas
        if (sampleCount % 1000 == 0) {
            Serial.print("Tiempo de procesamiento: ");
            Serial.print(processingTime);
            Serial.println(" us");
        }
    }
}