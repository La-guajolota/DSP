#include <Arduino.h>

// --- Configuración de pines ---
const int analogPin = A0; // Pin analógico de entrada
const int ledPin = 9;     // Pin PWM para visualización (opcional)

// --- Parámetros de muestreo ---
const unsigned long SAMPLE_PERIOD = 1000; // Microsegundos entre muestras (1kHz)
const int BUFFER_SIZE = 64;               // Tamaño del buffer (ajustar según memoria disponible)

// --- Buffers para almacenar muestras ---
int sample_buffer[BUFFER_SIZE];    // Buffer para muestras de entrada
int filtered_buffer[BUFFER_SIZE]; // Buffer para muestras filtradas
int buffer_index = 0;             // Índice del buffer
bool buffer_full = false;         // Indicador de buffer lleno

// --- Parámetros para filtro FIR paso-bajas ---
const int FIR_ORDER = 10; // Orden del filtro FIR
float fir_coeffs[FIR_ORDER + 1] = {
    0.0087, 0.0279, 0.0741, 0.1348, 0.1932, 0.2123,
    0.1932, 0.1348, 0.0741, 0.0279, 0.0087}; // Coeficientes precalculados
float fir_buffer[FIR_ORDER + 1] = {0};       // Buffer circular para el filtro FIR

// --- Variable para seleccionar tipo de filtro ---
int filter_type = 0; // 0: Sin filtro, 1: FIR

int apply_fir_filter(int new_sample);
void send_buffer();

// --- Configuración inicial ---
void setup() {
    Serial.begin(115200); // Iniciar comunicación serial
    pinMode(ledPin, OUTPUT); // Configurar pin de LED como salida

    // Mensaje de bienvenida
    Serial.println("Sistema de Adquisición y Filtrado Digital");
    Serial.println("Comandos disponibles:");
    Serial.println("0: Sin filtro");
    Serial.println("1: Filtro FIR");
    Serial.println("s: Enviar buffer completo");

    analogReference(DEFAULT); // Configurar referencia analógica
    delay(1000);              // Esperar estabilización
}

// --- Bucle principal ---
void loop() {
    static unsigned long last_sample = 0;
    unsigned long current_time = micros();

    // Verificar comandos seriales
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        if (cmd >= '0' && cmd <= '1') {
            filter_type = cmd - '0';
            Serial.print("Filtro cambiado a tipo: ");
            Serial.println(filter_type == 0 ? "Sin filtro" : "FIR");
        } else if (cmd == 's' || cmd == 'S') {
            send_buffer();
        }
    }

    // Muestrear a la frecuencia especificada
    if (current_time - last_sample >= SAMPLE_PERIOD) {
        int sensor_value = analogRead(analogPin); // Leer valor analógico
        int filtered_value = 0;

        // Aplicar filtro según tipo seleccionado
        switch (filter_type) {
        case 0: // Sin filtro
            filtered_value = sensor_value;
            break;
        case 1: // Filtro FIR
            filtered_value = apply_fir_filter(sensor_value);
            break;
        }

        // Visualización opcional mediante PWM
        analogWrite(ledPin, map(filtered_value, 0, 1023, 0, 255));

        // Guardar en buffer
        if (buffer_index < BUFFER_SIZE) {
            sample_buffer[buffer_index] = sensor_value;
            filtered_buffer[buffer_index] = filtered_value;
            buffer_index++;
            if (buffer_index >= BUFFER_SIZE) {
                buffer_full = true;
                Serial.println("Buffer lleno. Enviar 's' para ver datos.");
            }
        }

        last_sample = current_time;
    }
}

// --- Implementación del filtro FIR ---
int apply_fir_filter(int new_sample) {
    // Desplazar valores en el buffer
    for (int i = FIR_ORDER; i > 0; i--) {
        fir_buffer[i] = fir_buffer[i - 1];
    }

    // Añadir nueva muestra al inicio del buffer
    fir_buffer[0] = new_sample;

    // Aplicar coeficientes
    float result = 0;
    for (int i = 0; i <= FIR_ORDER; i++) {
        result += fir_coeffs[i] * fir_buffer[i];
    }

    return (int)result;
}

// --- Enviar buffer completo por puerto serial ---
void send_buffer() {
    if (!buffer_full) {
        Serial.println("Buffer no lleno. Esperando más muestras...");
        return;
    }

    // Enviar formato CSV: índice, original, filtrada
    Serial.println("index,original,filtered");
    for (int i = 0; i < BUFFER_SIZE; i++) {
        Serial.print(i);
        Serial.print(",");
        Serial.print(sample_buffer[i]);
        Serial.print(",");
        Serial.println(filtered_buffer[i]);
    }

    // Reiniciar buffer
    buffer_index = 0;
    buffer_full = false;
    Serial.println("Buffer enviado y reiniciado");
}