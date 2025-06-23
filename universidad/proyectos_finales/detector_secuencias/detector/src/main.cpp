/**
 * @file dtmf_detector_con_comandos.ino
 * @brief Sistema de reconocimiento de tonos DTMF y control por comandos para Arduino Mega.
 *
 * Este programa captura audio a través de un pin analógico, detecta tonos DTMF (Dual-Tone Multi-Frequency)
 * utilizando el algoritmo de Goertzel y ejecuta comandos basados en secuencias de teclas recibidas.
 *
 * El sistema está diseñado para:
 * 1. Muestrear audio a 8000 Hz.
 * 2. Analizar bloques de muestras para encontrar las frecuencias DTMF presentes.
 * 3. Indicar las frecuencias detectadas mediante 8 LEDs.
 * 4. Interpretar secuencias de teclas (delimitadas por '*' y '#') como comandos.
 * 5. Ejecutar acciones (controlar un LED) basadas en los comandos recibidos.
 *
 * @authors
 * Gabriel de Jesús García Tinoco
 */
#include <Arduino.h>
//==============================================================================
// 1. CONFIGURACIÓN GLOBAL Y CONSTANTES
//==============================================================================

// --- Configuración de Audio y Muestreo ---
const int audioInPin = A0;   // Pin analógico para la entrada de audio del micrófono.
const int sampleRate = 8000; // Frecuencia de muestreo en Hz. Fundamental para el análisis de frecuencia.
const int bufferSize = 256;  // Tamaño del buffer de audio. Almacena las muestras para procesarlas en bloque.
int audioBuffer[bufferSize]; // Arreglo para almacenar las muestras de audio.
int bufferIndex = 0;         // Índice actual para el buffer circular.

// --- Configuración de Hardware (LEDs) ---
const int ledPins[] = {2, 3, 4, 5, 6, 7, 8, 9}; // Pines digitales para los 8 LEDs indicadores de frecuencia.
const int actionLedPin = 10;                    // Pin para el LED que ejecuta las acciones de los comandos.

// --- Constantes del Sistema DTMF ---
const float lowFreq[] = {697, 770, 852, 941};
const float highFreq[] = {1209, 1336, 1477, 1633};
const float DETECTION_THRESHOLD = 30.0; // Umbral de detección para las frecuencias DTMF.
const int BLINK_DELAY_SHORT = 200;      // Retardo para parpadeo rápido en milisegundos.
const int BLINK_DELAY_LONG = 1000;      // Retardo para parpadeo lento en milisegundos;

// Matriz que mapea la combinación de una frecuencia baja y una alta a una tecla específica.
const char keys[4][4] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}};

// --- Variables de Estado y Detección ---
float filterOutputs[8];                                  // Almacena la energía calculada para cada una de las 8 frecuencias DTMF.
char lastDetectedKey = ' ';                              // Guarda la última tecla detectada para evitar repeticiones.
unsigned long lastSampleTime = 0;                        // Control de tiempo para mantener una frecuencia de muestreo constante.
const unsigned long samplePeriod = 1000000 / sampleRate; // Período de muestreo en microsegundos.

// --- Buffer para Comandos ---
String commandBuffer = ""; // Almacena la secuencia de teclas recibidas entre '*' y '#'.

//==============================================================================
// Prototipos de funciones
//==============================================================================
void processBuffer();
float applyGoertzel(int index);
void updateLedState(int pin, float energy);
int findMaxIndex(float array[], int start, int end);
void handleKey(char key);
void processCommand(String cmd);
void toggleActionLed(int state, const char *message);
void blinkActionLed(int times, int delayTime, const char *message);
void executeAccessGranted();

//==============================================================================
// 2. FUNCIÓN DE CONFIGURACIÓN INICIAL (setup)
//==============================================================================
void setup()
{
  // Inicia la comunicación serie para depuración y visualización de resultados.
  Serial.begin(115200);

  // Configura los 8 pines de los LEDs de frecuencia como salidas y los apaga.
  for (int i = 0; i < 8; i++)
  {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  // Configura el pin del LED de acción como salida y lo apaga.
  pinMode(actionLedPin, OUTPUT);
  digitalWrite(actionLedPin, LOW);

  // Mensaje de inicio en el monitor serie.
  Serial.println("Sistema DTMF listo");
}

//==============================================================================
// 3. BUCLE PRINCIPAL (loop)
//==============================================================================
void loop()
{
  // Bucle de muestreo controlado por tiempo para mantener la frecuencia de 8kHz.
  unsigned long currentTime = micros();
  if (currentTime - lastSampleTime >= samplePeriod)
  {
    lastSampleTime = currentTime; // Actualiza el tiempo de la última muestra.

    // Lee el valor del ADC, lo normaliza (centra en cero) y lo guarda en el buffer.
    int sample = analogRead(audioInPin) - 512;
    audioBuffer[bufferIndex] = sample;

    // Incrementa el índice del buffer de forma circular.
    bufferIndex = (bufferIndex + 1) % bufferSize;

    // Procesa el buffer solo cuando se ha llenado por completo.
    if (bufferIndex == 0)
    {
      processBuffer();
    }
  }
}

//==============================================================================
// 4. LÓGICA DE PROCESAMIENTO Y DETECCIÓN
//==============================================================================

/**
 * @brief Procesa el buffer de audio para detectar tonos DTMF.
 */
void processBuffer()
{
  // Aplica el algoritmo de Goertzel y actualiza LEDs.
  for (int i = 0; i < 8; i++)
  {
    filterOutputs[i] = applyGoertzel(i);
    updateLedState(ledPins[i], filterOutputs[i]);
  }

  // Encuentra las frecuencias dominantes.
  int maxLow = findMaxIndex(filterOutputs, 0, 3);
  int maxHigh = findMaxIndex(filterOutputs, 4, 7);

  // Verifica si ambas frecuencias superan el umbral.
  if (filterOutputs[maxLow] > DETECTION_THRESHOLD && filterOutputs[maxHigh] > DETECTION_THRESHOLD)
  {
    char key = keys[maxLow][maxHigh - 4];
    if (key != lastDetectedKey)
    {
      lastDetectedKey = key;
      Serial.print("Tecla detectada: ");
      Serial.println(key);
      handleKey(key);
    }
  }
  else
  {
    lastDetectedKey = ' ';
  }
}

/**
 * @brief Actualiza el estado de un LED según el valor de energía.
 * @param pin El pin del LED.
 * @param energy La energía calculada.
 */
void updateLedState(int pin, float energy)
{
  digitalWrite(pin, energy > DETECTION_THRESHOLD ? HIGH : LOW);
}

/**
 * @brief Maneja la lógica para construir la secuencia de comandos.
 * @param key La tecla detectada.
 */
void handleKey(char key)
{
  if (key == '*')
  {
    // La tecla '*' inicia una nueva secuencia de comando, limpiando el buffer.
    commandBuffer = "";
    Serial.println("Inicio de comando");
  }
  else if (key == '#')
  {
    // La tecla '#' finaliza la secuencia y la procesa.
    Serial.print("Secuencia completa: ");
    Serial.println(commandBuffer);
    processCommand(commandBuffer);
    commandBuffer = ""; // Limpia el buffer después de procesar.
  }
  else
  {
    // Cualquier otra tecla se añade a la secuencia actual.
    commandBuffer += key;
    Serial.print("Secuencia actual: ");
    Serial.println(commandBuffer);
  }
}

//==============================================================================
// 5. FUNCIONES DE UTILIDAD
//==============================================================================

/**
 * @brief Ejecuta una acción basada en la secuencia de comando recibida.
 * @param cmd La cadena de comando completa.
 */
void processCommand(String cmd)
{
  if (cmd == "1")
  {
    toggleActionLed(HIGH, "LED DE ACCIÓN ENCENDIDO");
  }
  else if (cmd == "0")
  {
    toggleActionLed(LOW, "LED DE ACCIÓN APAGADO");
  }
  else if (cmd == "3")
  {
    executeAccessGranted();
  }
  else if (cmd == "2")
  {
    blinkActionLed(3, BLINK_DELAY_LONG, "Secuencia 2 detectada");
  }
  else if (cmd == "4")
  {
    blinkActionLed(3, BLINK_DELAY_SHORT, "Secuencia 4 detectada: parpadeo rápido 3 veces");
  }
  else if (cmd == "5")
  {
    toggleActionLed(HIGH, "Secuencia 5 detectada: encender LED por 5 segundos");
    delay(5000);
    toggleActionLed(LOW, "");
  }
  else if (cmd == "7")
  {
    blinkActionLed(2, BLINK_DELAY_LONG, "Secuencia 7 detectada: parpadeo lento 2 veces");
  }
  else
  {
    Serial.println("Comando no reconocido");
  }
}

/**
 * @brief Enciende o apaga el LED de acción con un mensaje opcional.
 * @param state Estado del LED (HIGH o LOW).
 * @param message Mensaje a imprimir en el monitor serie.
 */
void toggleActionLed(int state, const char *message)
{
  digitalWrite(actionLedPin, state);
  if (message[0] != '\0')
  {
    Serial.println(message);
  }
}

/**
 * @brief Hace parpadear el LED de acción un número de veces.
 * @param times Número de parpadeos.
 * @param delayTime Tiempo de retardo entre encendido y apagado.
 * @param message Mensaje a imprimir en el monitor serie.
 */
void blinkActionLed(int times, int delayTime, const char *message)
{
  Serial.println(message);
  for (int i = 0; i < times; i++)
  {
    toggleActionLed(HIGH, "");
    delay(delayTime);
    toggleActionLed(LOW, "");
    delay(delayTime);
  }
}

/**
 * @brief Ejecuta la acción de "Acceso Concedido".
 */
void executeAccessGranted()
{
  Serial.println("ACCESO CONCEDIDO ✔️");
  toggleActionLed(HIGH, "");
  delay(2000);
  toggleActionLed(LOW, "");
}

/**
 * @brief Encuentra el índice del valor máximo en una porción de un arreglo.
 * @param array El arreglo donde buscar.
 * @param start El índice inicial de la búsqueda.
 * @param end El índice final de la búsqueda.
 * @return El índice del valor más alto encontrado.
 */
int findMaxIndex(float array[], int start, int end)
{
  int maxIdx = start;
  float maxVal = array[start];
  for (int i = start + 1; i <= end; i++)
  {
    if (array[i] > maxVal)
    {
      maxVal = array[i];
      maxIdx = i;
    }
  }
  return maxIdx;
}

/**
 * @brief Aplica el algoritmo de Goertzel para detectar la energía de una frecuencia específica.
 * Es computacionalmente más eficiente que una FFT completa para detectar pocas frecuencias.
 * @param index El índice de la frecuencia a analizar (0-3 para bajas, 4-7 para altas).
 * @return La magnitud o energía de la frecuencia objetivo en el buffer de audio.
 */
float applyGoertzel(int index)
{
  float targetFreq = (index < 4) ? lowFreq[index] : highFreq[index - 4];
  float omega = 2.0 * PI * targetFreq / sampleRate;
  float coeff = 2.0 * cos(omega);
  float q0 = 0, q1 = 0, q2 = 0;

  for (int i = 0; i < bufferSize; i++)
  {
    q0 = coeff * q1 - q2 + audioBuffer[(bufferIndex + i) % bufferSize];
    q2 = q1;
    q1 = q0;
  }

  // Calcula la magnitud de la energía de la frecuencia.
  return sqrt(q1 * q1 + q2 * q2 - q1 * q2 * coeff);
}
