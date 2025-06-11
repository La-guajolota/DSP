/*
  ESP32 - PROCESADOR DE FILTROS DIGITALES CORREGIDO
  Para estudiantes de 8vo semestre de Ing. en Telecomunicaciones y Electrónica
  
  Corrección: Sincronización mejorada para trabajo con Python
*/

#include <Arduino.h>
#include <esp_chip_info.h>
#include <esp_system.h>

// ========================================
// CONFIGURACIÓN DEL SISTEMA
// ========================================
const int AUDIO_OUT_PIN = 25;        // Pin DAC para salida de audio
const int AUDIO_IN_PIN = 36;         // Pin ADC para entrada de audio
const int STATUS_LED = 2;            // LED integrado del ESP32
const int PROCESSING_LED = 4;        // LED adicional para procesamiento

// Buffers expandidos (4x más que Arduino Mega)
const int BUFFER_SIZE = 2048;
const int MAX_SAMPLES = BUFFER_SIZE;

// ========================================
// VARIABLES GLOBALES
// ========================================
// Buffers principales
int input_buffer[BUFFER_SIZE];
int output_buffer[BUFFER_SIZE];
int buffer_index = 0;
bool buffer_ready = false;
bool buffer_processed = false;  // NUEVO: indica si el buffer fue procesado
bool collecting_data = false;

// Control de filtros
int filter_type = 0;  // 0=Bypass, 1=FIR, 2=IIR, 3=Adaptativo
unsigned long last_led_update = 0;
unsigned long processing_start_time = 0;

// Estadísticas de rendimiento
unsigned long samples_processed = 0;
unsigned long total_processing_time = 0;
float average_processing_time = 0;

// ========================================
// FILTRO FIR (51 COEFICIENTES) CORREGIDO
// ========================================
const int FIR_TAPS = 51;
// Coeficientes escalados para trabajar con rango 0-1023
float fir_coeffs[FIR_TAPS] = {
  0.0002, 0.0005, 0.0008, 0.0012, 0.0018, 0.0025, 0.0033, 0.0042,
  0.0052, 0.0063, 0.0074, 0.0085, 0.0096, 0.0106, 0.0115, 0.0123,
  0.0129, 0.0133, 0.0135, 0.0134, 0.0131, 0.0125, 0.0116, 0.0104,
  0.0089, 0.0071, 0.9500, 0.0071, 0.0089, 0.0104, 0.0116, 0.0125,
  0.0131, 0.0134, 0.0135, 0.0133, 0.0129, 0.0123, 0.0115, 0.0106,
  0.0096, 0.0085, 0.0074, 0.0063, 0.0052, 0.0042, 0.0033, 0.0025,
  0.0018, 0.0012, 0.0008
};
float fir_buffer[FIR_TAPS] = {0};

// ========================================
// FILTRO IIR BUTTERWORTH ORDEN 4 SIMPLIFICADO
// ========================================
const int IIR_ORDER = 4;
// Coeficientes para filtro pasa-bajas Butterworth fc=800Hz, fs=8000Hz
float iir_b[IIR_ORDER + 1] = {
  0.0067, 0.0269, 0.0404, 0.0269, 0.0067
};
float iir_a[IIR_ORDER + 1] = {
  1.0000, -2.3741, 2.3147, -1.0543, 0.1873
};
float iir_x[IIR_ORDER + 1] = {0};
float iir_y[IIR_ORDER + 1] = {0};

// ========================================
// FILTRO ADAPTATIVO EXPERIMENTAL
// ========================================
const int ADAPTIVE_TAPS = 21;
float adaptive_coeffs[ADAPTIVE_TAPS] = {0};
float adaptation_rate = 0.001;
bool adaptive_mode = false;

// ========================================
// VARIABLES FREERTOS
// ========================================
TaskHandle_t ProcessingTask;
SemaphoreHandle_t buffer_semaphore;

// ========================================
// DECLARACIÓN DE FUNCIONES
// ========================================
void processing_task(void* parameter);
void handle_serial_command();
void test_system_advanced();
void reset_system_with_stats();
void reset_filters();
void start_capture_advanced();
void process_audio_sample_advanced(int input_sample);
void process_single_sample(int sample);  // NUEVA DECLARACIÓN
void test_filter_functionality();  // NUEVA DECLARACIÓN PARA TEST
void debug_filter_state();  // NUEVA DECLARACIÓN PARA DEBUG
int apply_selected_filter(int input);
int apply_fir_filter_optimized(int input);
int apply_iir_filter_optimized(int input);
int apply_adaptive_filter(int input);
void send_data_compressed();
void show_advanced_stats();
void show_performance_stats();
void show_memory_info();
void update_status_indicators();
void print_welcome_message();
void print_system_info();

// ========================================
// FUNCIÓN SETUP
// ========================================
void setup() {
  Serial.begin(115200);
  delay(1000);  // Esperar estabilización
  
  // Configuración de pines
  pinMode(AUDIO_OUT_PIN, OUTPUT);
  pinMode(STATUS_LED, OUTPUT);
  pinMode(PROCESSING_LED, OUTPUT);
  
  // Configurar DAC en valor neutral
  dacWrite(AUDIO_OUT_PIN, 127);
  
  // Crear semáforo para sincronización
  buffer_semaphore = xSemaphoreCreateMutex();
  
  // Crear tarea de procesamiento en Core 1
  xTaskCreatePinnedToCore(
    processing_task,     // Función de la tarea
    "AudioProcessing",   // Nombre de la tarea
    10000,              // Tamaño del stack
    NULL,               // Parámetros
    1,                  // Prioridad
    &ProcessingTask,    // Handle de la tarea
    1                   // Core específico (Core 1)
  );
  
  // Mostrar mensaje de bienvenida
  print_welcome_message();
  print_system_info();
  
  // Secuencia de LEDs de inicialización
  for(int i = 0; i < 5; i++) {
    digitalWrite(STATUS_LED, HIGH);
    digitalWrite(PROCESSING_LED, LOW);
    delay(100);
    digitalWrite(STATUS_LED, LOW);
    digitalWrite(PROCESSING_LED, HIGH);
    delay(100);
  }
  digitalWrite(PROCESSING_LED, LOW);
  
  Serial.println("ESP32 LISTO - Sistema dual-core activado");
  Serial.print("Ejecutándose en Core: ");
  Serial.println(xPortGetCoreID());
}

// ========================================
// FUNCIÓN LOOP PRINCIPAL
// ========================================
void loop() {
  // Manejar comandos serie
  if (Serial.available() > 0) {
    handle_serial_command();
  }
  
  // Actualizar indicadores LED
  update_status_indicators();
  
  // Alimentar watchdog
  yield();
  
  // Pausa mínima para eficiencia energética
  delay(1);
}

// ========================================
// TAREA DE PROCESAMIENTO PARALELO
// ========================================
void processing_task(void* parameter) {
  for(;;) {
    if (buffer_ready && !buffer_processed && xSemaphoreTake(buffer_semaphore, portMAX_DELAY)) {
      processing_start_time = micros();
      
      // Procesar todas las muestras del buffer
      for(int i = 0; i < buffer_index; i++) {
        int processed_sample = apply_selected_filter(input_buffer[i]);
        output_buffer[i] = processed_sample;
        
        // Parpadear LED cada 100 muestras
        if(i % 100 == 0) {
          samples_processed += 100;
          digitalWrite(PROCESSING_LED, !digitalRead(PROCESSING_LED));
        }
      }
      
      // Calcular estadísticas de tiempo
      unsigned long processing_time = micros() - processing_start_time;
      total_processing_time += processing_time;
      if(samples_processed > 0) {
        average_processing_time = (float)total_processing_time / samples_processed * 1000.0;
      }
      
      // CORRECCION: Marcar como procesado pero mantener ready para envío
      buffer_processed = true;
      
      xSemaphoreGive(buffer_semaphore);
      
      // Notificar completado
      Serial.println("PROCESAMIENTO PARALELO COMPLETADO");
      Serial.print("Tiempo: ");
      Serial.print(processing_time);
      Serial.println(" μs");
    }
    
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

// ========================================
// MANEJO DE COMANDOS SERIE
// ========================================
void handle_serial_command() {
  String command = Serial.readStringUntil('\n');
  command.trim();
  
  if (command == "t" || command == "T") {
    test_system_advanced();
    
  } else if (command == "r" || command == "R") {
    reset_system_with_stats();
    
  } else if (command == "0") {
    filter_type = 0;
    reset_filters();
    Serial.println("FILTRO: BYPASS activado");
    Serial.println("COMUNICACION OK");  // Confirmación para Python
    
  } else if (command == "1") {
    filter_type = 1;
    reset_filters();
    Serial.println("FILTRO: FIR activado (51 coeficientes)");
    Serial.println("COMUNICACION OK");  // Confirmación para Python
    
  } else if (command == "2") {
    filter_type = 2;
    reset_filters();
    Serial.println("FILTRO: IIR Butterworth activado (orden 8)");
    Serial.println("COMUNICACION OK");  // Confirmación para Python
    
  } else if (command == "3") {
    filter_type = 3;
    adaptive_mode = true;
    reset_filters();
    Serial.println("FILTRO: ADAPTATIVO activado");
    Serial.println("COMUNICACION OK");  // Confirmación para Python
    
  } else if (command == "c" || command == "C") {
    start_capture_advanced();
    
  } else if (command == "s" || command == "S") {
    send_data_compressed();
    
  } else if (command == "p" || command == "P") {
    show_performance_stats();
    
  } else if (command == "m" || command == "M") {
    show_memory_info();
    
  } else if (command.startsWith("DATA:")) {
    int sample = command.substring(5).toInt();
    process_audio_sample_advanced(sample);
    
  } else if (command == "PROCESS:") {
    // Nuevo comando para procesamiento directo muestra por muestra
    int sample = command.substring(8).toInt();
    process_single_sample(sample);
    
  } else if (command == "test_filter" || command == "tf") {
    test_filter_functionality();
    
  } else if (command == "debug_filter" || command == "df") {
    debug_filter_state();
    
  } else {
    Serial.println("COMANDO NO RECONOCIDO");
    Serial.println("Comandos ESP32: t, r, 0-3, c, s, p, m, DATA:xxx, PROCESS:xxx, tf, df");
  }
}

// ========================================
// TEST DEL SISTEMA
// ========================================
void test_system_advanced() {
  Serial.println("\n=== TEST AVANZADO ESP32 ===");
  
  // Información del chip
  esp_chip_info_t chip_info;
  esp_chip_info(&chip_info);
  
  Serial.print("Chip: ESP32 rev ");
  Serial.println(chip_info.revision);
  Serial.print("Cores CPU: ");
  Serial.println(chip_info.cores);
  Serial.print("Frecuencia: ");
  Serial.print(ESP.getCpuFreqMHz());
  Serial.println(" MHz");
  
  // Test de rendimiento
  Serial.println("\nTest de rendimiento:");
  unsigned long start_time = micros();
  
  for(int i = 0; i < 1000; i++) {
    apply_fir_filter_optimized(512);
  }
  unsigned long fir_time = micros() - start_time;
  
  start_time = micros();
  for(int i = 0; i < 1000; i++) {
    apply_iir_filter_optimized(512);
  }
  unsigned long iir_time = micros() - start_time;
  
  Serial.print("FIR (1000 muestras): ");
  Serial.print(fir_time);
  Serial.println(" μs");
  Serial.print("IIR (1000 muestras): ");
  Serial.print(iir_time);
  Serial.println(" μs");
  Serial.print("Ventaja IIR: ");
  Serial.print((float)fir_time / iir_time, 2);
  Serial.println("x más rápido");
  
  Serial.println("TEST COMPLETADO");
}

// ========================================
// RESET CON ESTADÍSTICAS
// ========================================
void reset_system_with_stats() {
  Serial.println("\n=== RESET CON ESTADÍSTICAS ===");
  
  if(samples_processed > 0) {
    Serial.print("Muestras procesadas: ");
    Serial.println(samples_processed);
    Serial.print("Tiempo promedio: ");
    Serial.print(average_processing_time, 3);
    Serial.println(" ms/muestra");
    Serial.print("Throughput: ");
    Serial.print(1000.0 / average_processing_time, 1);
    Serial.println(" muestras/s");
  }
  
  // Reset variables
  buffer_index = 0;
  buffer_ready = false;
  buffer_processed = false;  // NUEVO: resetear flag de procesado
  collecting_data = false;
  filter_type = 0;
  adaptive_mode = false;
  samples_processed = 0;
  total_processing_time = 0;
  average_processing_time = 0;
  
  // Limpiar buffers
  memset(input_buffer, 0, sizeof(input_buffer));
  memset(output_buffer, 0, sizeof(output_buffer));
  reset_filters();
  
  dacWrite(AUDIO_OUT_PIN, 127);
  Serial.println("Sistema reiniciado");
  show_memory_info();
}

// ========================================
// RESET DE FILTROS
// ========================================
void reset_filters() {
  // Reset FIR
  for (int i = 0; i < FIR_TAPS; i++) {
    fir_buffer[i] = 0;
  }
  
  // Reset IIR
  for (int i = 0; i <= IIR_ORDER; i++) {
    iir_x[i] = 0;
    iir_y[i] = 0;
  }
  
  // Reset adaptativo
  for (int i = 0; i < ADAPTIVE_TAPS; i++) {
    adaptive_coeffs[i] = 0;
  }
}

// ========================================
// INICIAR CAPTURA
// ========================================
void start_capture_advanced() {
  Serial.println("INICIANDO CAPTURA AVANZADA ESP32");
  Serial.print("Filtro seleccionado: ");
  
  switch(filter_type) {
    case 0: Serial.println("Bypass"); break;
    case 1: Serial.println("FIR optimizado (51 coef)"); break;
    case 2: Serial.println("IIR superior (orden 8)"); break;
    case 3: Serial.println("Adaptativo experimental"); break;
  }
  
  if(xSemaphoreTake(buffer_semaphore, portMAX_DELAY)) {
    buffer_index = 0;
    buffer_ready = false;
    buffer_processed = false;  // NUEVO: resetear flag de procesado
    collecting_data = true;
    xSemaphoreGive(buffer_semaphore);
  }
  
  Serial.print("Buffer expandido preparado para ");
  Serial.print(BUFFER_SIZE);
  Serial.println(" muestras");
  Serial.println("LISTO PARA RECIBIR DATOS");
}

// ========================================
// PROCESAR MUESTRA DE AUDIO
// ========================================
void process_audio_sample_advanced(int input_sample) {
  if (buffer_index >= BUFFER_SIZE) {
    if (collecting_data) {
      collecting_data = false;
      buffer_ready = true;
      Serial.println("BUFFER COMPLETO");
    }
    return;
  }
  
  input_sample = constrain(input_sample, 0, 1023);
  
  // CORRECCION: Aplicar filtro INMEDIATAMENTE y almacenar resultado
  int filtered_sample = apply_selected_filter(input_sample);
  
  input_buffer[buffer_index] = input_sample;
  output_buffer[buffer_index] = filtered_sample;  // Almacenar ya filtrado
  buffer_index++;
  
  // Salida DAC con señal filtrada
  int dac_value = map(filtered_sample, 0, 1023, 0, 255);
  dacWrite(AUDIO_OUT_PIN, dac_value);
  
  // Progreso cada 200 muestras
  if (buffer_index % 200 == 0) {
    Serial.print("Progreso: ");
    Serial.print(buffer_index);
    Serial.print("/");
    Serial.print(BUFFER_SIZE);
    Serial.print(" (");
    Serial.print((float)buffer_index / BUFFER_SIZE * 100, 1);
    Serial.println("%)");
  }
  
  if (buffer_index >= BUFFER_SIZE) {
    collecting_data = false;
    buffer_ready = true;
    buffer_processed = true;  // NUEVO: Marcar como ya procesado
    Serial.println("PROCESAMIENTO COMPLETADO");
  }
}

// ========================================
// APLICAR FILTRO SELECCIONADO
// ========================================
int apply_selected_filter(int input) {
  switch(filter_type) {
    case 0: return input;
    case 1: return apply_fir_filter_optimized(input);
    case 2: return apply_iir_filter_optimized(input);
    case 3: return apply_adaptive_filter(input);
    default: return input;
  }
}

// ========================================
// FILTRO FIR OPTIMIZADO Y CORREGIDO
// ========================================
int apply_fir_filter_optimized(int input) {
  // Desplazar buffer (método más eficiente)
  for(int i = FIR_TAPS - 1; i > 0; i--) {
    fir_buffer[i] = fir_buffer[i-1];
  }
  fir_buffer[0] = (float)input;
  
  // Convolución
  float output = 0.0;
  for (int i = 0; i < FIR_TAPS; i++) {
    output += fir_coeffs[i] * fir_buffer[i];
  }
  
  // Asegurar que la salida esté en rango válido
  int result = (int)output;
  return constrain(result, 0, 1023);
}

// ========================================
// FILTRO IIR OPTIMIZADO Y CORREGIDO
// ========================================
int apply_iir_filter_optimized(int input) {
  // Desplazar buffers de entrada
  for(int i = IIR_ORDER; i > 0; i--) {
    iir_x[i] = iir_x[i-1];
  }
  iir_x[0] = (float)input;
  
  // Desplazar buffers de salida
  for(int i = IIR_ORDER; i > 0; i--) {
    iir_y[i] = iir_y[i-1];
  }
  
  // Calcular salida (ecuación en diferencias)
  float output = 0.0;
  
  // Parte feedforward (numerador)
  for (int i = 0; i <= IIR_ORDER; i++) {
    output += iir_b[i] * iir_x[i];
  }
  
  // Parte feedback (denominador, sin a[0] que es 1.0)
  for (int i = 1; i <= IIR_ORDER; i++) {
    output -= iir_a[i] * iir_y[i];
  }
  
  // Almacenar nueva salida
  iir_y[0] = output;
  
  // Convertir a entero y limitar rango
  int result = (int)output;
  return constrain(result, 0, 1023);
}

// ========================================
// FILTRO ADAPTATIVO LMS
// ========================================
int apply_adaptive_filter(int input) {
  static float adaptive_buffer[ADAPTIVE_TAPS] = {0};
  static float error_signal = 0;
  static float desired_output = input * 0.7;
  
  // Desplazar buffer
  memmove(&adaptive_buffer[1], &adaptive_buffer[0], (ADAPTIVE_TAPS-1) * sizeof(float));
  adaptive_buffer[0] = input;
  
  // Calcular salida
  float output = 0;
  for(int i = 0; i < ADAPTIVE_TAPS; i++) {
    output += adaptive_coeffs[i] * adaptive_buffer[i];
  }
  
  // Calcular error y actualizar coeficientes
  error_signal = desired_output - output;
  for(int i = 0; i < ADAPTIVE_TAPS; i++) {
    adaptive_coeffs[i] += adaptation_rate * error_signal * adaptive_buffer[i];
  }
  
  return constrain((int)output, 0, 1023);
}

// ========================================
// ENVIAR DATOS COMPRIMIDOS
// ========================================
void send_data_compressed() {
  // Verificar que tenemos datos para enviar
  if (buffer_index == 0) {
    Serial.println("ERROR: No hay datos en buffer");
    return;
  }
  
  // Si los datos no están procesados, procesarlos ahora
  if (!buffer_processed) {
    Serial.println("Aplicando filtros a los datos...");
    for(int i = 0; i < buffer_index; i++) {
      output_buffer[i] = apply_selected_filter(input_buffer[i]);
    }
    buffer_processed = true;
    Serial.println("Filtrado completado");
  }
  
  // Verificar que realmente se aplicó el filtro
  bool filtro_aplicado = false;
  for(int i = 0; i < min(100, buffer_index); i++) {
    if(input_buffer[i] != output_buffer[i]) {
      filtro_aplicado = true;
      break;
    }
  }
  
  if(filtro_aplicado) {
    Serial.println("FILTRO CONFIRMADO APLICADO");
  } else {
    Serial.println("ADVERTENCIA: Filtro parece no aplicado");
  }
  
  // Asegurarse de que el búfer de salida esté listo
  Serial.flush();
  delay(100);

  Serial.println("INICIO_DATOS_ESP32");
  Serial.println("index,input,output,timestamp");
  
  unsigned long timestamp_base = millis();
  
  for (int i = 0; i < buffer_index; i++) {
    Serial.print(i);
    Serial.print(",");
    Serial.print(input_buffer[i]);
    Serial.print(",");
    Serial.print(output_buffer[i]);
    Serial.print(",");
    Serial.println(timestamp_base + i);
    
    // Flush cada 100 muestras para mayor velocidad
    if ((i + 1) % 100 == 0) {
      Serial.flush();
      delay(5);  // Reducir delay para mayor velocidad
    }
  }
  
  Serial.println("FIN_DATOS_ESP32");
  Serial.println("ENVÍO COMPLETADO");
  show_advanced_stats();
}

// ========================================
// ESTADÍSTICAS AVANZADAS
// ========================================
void show_advanced_stats() {
  long sum_input = 0, sum_output = 0;
  int min_input = 1023, max_input = 0;
  int min_output = 1023, max_output = 0;
  
  for (int i = 0; i < buffer_index; i++) {
    sum_input += input_buffer[i];
    sum_output += output_buffer[i];
    
    min_input = min(min_input, input_buffer[i]);
    max_input = max(max_input, input_buffer[i]);
    min_output = min(min_output, output_buffer[i]);
    max_output = max(max_output, output_buffer[i]);
  }
  
  Serial.println("\n=== ESTADÍSTICAS ===");
  Serial.print("Promedio entrada: ");
  Serial.print(sum_input / buffer_index);
  Serial.print(" (");
  Serial.print(min_input);
  Serial.print("-");
  Serial.print(max_input);
  Serial.println(")");
  
  Serial.print("Promedio salida: ");
  Serial.print(sum_output / buffer_index);
  Serial.print(" (");
  Serial.print(min_output);
  Serial.print("-");
  Serial.print(max_output);
  Serial.println(")");
  
  Serial.print("Atenuación: ");
  Serial.print((float)(sum_input - sum_output) / buffer_index, 2);
  Serial.println(" LSB");
}

// ========================================
// ESTADÍSTICAS DE RENDIMIENTO
// ========================================
void show_performance_stats() {
  Serial.println("\n=== RENDIMIENTO ESP32 ===");
  
  Serial.print("Muestras procesadas: ");
  Serial.println(samples_processed);
  
  if(samples_processed > 0) {
    Serial.print("Tiempo promedio: ");
    Serial.print(average_processing_time, 3);
    Serial.println(" ms");
    
    Serial.print("Throughput: ");
    Serial.print(1000.0 / average_processing_time, 1);
    Serial.println(" muestras/s");
    
    Serial.print("Capacidad vs 8kHz: ");
    Serial.print((1000.0 / average_processing_time) / 8000.0 * 100, 1);
    Serial.println("%");
  }
  
  Serial.print("Filtro activo: ");
  switch(filter_type) {
    case 0: Serial.println("Bypass"); break;
    case 1: Serial.println("FIR (alta carga)"); break;
    case 2: Serial.println("IIR (carga media)"); break;
    case 3: Serial.println("Adaptativo"); break;
  }
  
  Serial.print("Procesamiento paralelo: ");
  Serial.println(ProcessingTask != NULL ? "Activo" : "Inactivo");
  
  Serial.print("Core actual: ");
  Serial.println(xPortGetCoreID());
  
  // Información educativa
  Serial.println("\nEficiencia computacional:");
  Serial.print("- FIR (");
  Serial.print(FIR_TAPS);
  Serial.print(" coef): ~");
  Serial.print(FIR_TAPS + 1);
  Serial.println(" ops/muestra");
  
  Serial.print("- IIR (orden ");
  Serial.print(IIR_ORDER);
  Serial.print("): ~");
  Serial.print((IIR_ORDER + 1) * 2);
  Serial.println(" ops/muestra");
  
  Serial.println("- Adaptativo: ~65 ops/muestra");
  Serial.println("Nota: IIR es más eficiente que FIR equivalente");
}

// ========================================
// INFORMACIÓN DE MEMORIA
// ========================================
void show_memory_info() {
  Serial.println("\n=== MEMORIA ESP32 ===");
  
  Serial.print("Total: ");
  Serial.print(ESP.getHeapSize());
  Serial.println(" bytes");
  
  Serial.print("Libre: ");
  Serial.print(ESP.getFreeHeap());
  Serial.println(" bytes");
  
  Serial.print("Mínima: ");
  Serial.print(ESP.getMinFreeHeap());
  Serial.println(" bytes");
  
  Serial.print("Usada: ");
  Serial.print(ESP.getHeapSize() - ESP.getFreeHeap());
  Serial.println(" bytes");
  
  Serial.print("Uso: ");
  Serial.print((float)(ESP.getHeapSize() - ESP.getFreeHeap()) / ESP.getHeapSize() * 100, 1);
  Serial.println("%");
  
  Serial.print("Buffers principales: ");
  Serial.print(BUFFER_SIZE * sizeof(int) * 2);
  Serial.println(" bytes");
  
  Serial.print("Buffers filtros: ");
  Serial.print(FIR_TAPS * sizeof(float) + (IIR_ORDER + 1) * sizeof(float) * 2);
  Serial.println(" bytes");
  
  if(ESP.getFreeHeap() < 50000) {
    Serial.println("Memoria baja");
  } else {
    Serial.println("Memoria OK");
  }
}

// ========================================
// ACTUALIZAR INDICADORES LED
// ========================================
void update_status_indicators() {
  unsigned long current_time = millis();
  
  if (collecting_data) {
    // Parpadeo rápido durante captura
    if (current_time - last_led_update > 50) {
      digitalWrite(STATUS_LED, !digitalRead(STATUS_LED));
      last_led_update = current_time;
    }
  } else if (buffer_ready || buffer_processed) {
    // Encendido fijo cuando datos listos
    digitalWrite(STATUS_LED, HIGH);
    digitalWrite(PROCESSING_LED, ProcessingTask != NULL);
  } else {
    // Parpadeo lento en espera
    if (current_time - last_led_update > 2000) {
      digitalWrite(STATUS_LED, !digitalRead(STATUS_LED));
      last_led_update = current_time;
    }
  }
}

// ========================================
// MENSAJE DE BIENVENIDA
// ========================================
void print_welcome_message() {
  Serial.println("\n==================================================");
  Serial.println("   ESP32 - PROCESADOR FILTROS DIGITALES");
  Serial.println("   Para estudiantes de Telecomunicaciones");
  Serial.println("   Dual-Core + 320KB RAM + DAC 8-bit");
  Serial.println("==================================================");
}

// ========================================
// INFORMACIÓN DEL SISTEMA
// ========================================
void print_system_info() {
  Serial.print("RAM total: ");
  Serial.print(ESP.getHeapSize());
  Serial.println(" bytes");
  
  Serial.print("RAM libre: ");
  Serial.print(ESP.getFreeHeap());
  Serial.println(" bytes");
  
  Serial.print("CPU: ");
  Serial.print(ESP.getCpuFreqMHz());
  Serial.println(" MHz");
  
  Serial.print("Buffer: ");
  Serial.print(BUFFER_SIZE);
  Serial.println(" muestras");
  
  Serial.println("\nFILTROS DISPONIBLES:");
  Serial.println("  0 = Bypass");
  Serial.println("  1 = FIR pasa-bajas (51 coef)");
  Serial.println("  2 = IIR Butterworth (orden 8)");
  Serial.println("  3 = Adaptativo LMS");
  
  Serial.println("\nCOMANDOS:");
  Serial.println("  t = Test sistema");
  Serial.println("  r = Reset con stats");
  Serial.println("  0/1/2/3 = Filtro");
  Serial.println("  c = Captura");
  Serial.println("  s = Envío datos");
  Serial.println("  p = Performance");
  Serial.println("  m = Memoria");
  Serial.println("  DATA:xxx = Muestra");
  Serial.println("  PROCESS:xxx = Procesar muestra");
  Serial.println("==================================================");
}

// ========================================
// COMANDO PARA PROCESAR MUESTRA DIRECTA
// ========================================
void process_single_sample(int sample) {
  // Para procesamiento muestra por muestra sin almacenar en buffer
  sample = constrain(sample, 0, 1023);
  int filtered_sample = apply_selected_filter(sample);
  
  // Enviar resultado inmediato
  Serial.print("SAMPLE_RESULT:");
  Serial.print(sample);
  Serial.print(",");
  Serial.println(filtered_sample);
}

// ========================================
// TEST DE FUNCIONALIDAD DE FILTROS
// ========================================
void test_filter_functionality() {
  Serial.println("\n=== TEST DE FILTROS ===");
  
  // Guardar el tipo de filtro actual
  int filtro_original = filter_type;
  
  // Test solo del filtro actual (no cambiar filter_type)
  Serial.print("FILTRO ACTUAL: ");
  Serial.print(filter_type);
  Serial.print(" (");
  switch(filter_type) {
    case 0: Serial.print("BYPASS"); break;
    case 1: Serial.print("FIR"); break;
    case 2: Serial.print("IIR"); break;
    case 3: Serial.print("ADAPTATIVO"); break;
  }
  Serial.println(")");
  
  // Test con valores específicos
  int test_values[] = {0, 256, 512, 768, 1023};
  int num_tests = 5;
  
  for(int i = 0; i < num_tests; i++) {
    int input = test_values[i];
    int output = apply_selected_filter(input);
    
    Serial.print("  Entrada: ");
    Serial.print(input);
    Serial.print(" -> Salida: ");
    Serial.print(output);
    Serial.print(" (Diferencia: ");
    Serial.print(output - input);
    Serial.println(")");
  }
  
  // Restaurar el filtro original (aunque no debería haber cambiado)
  filter_type = filtro_original;
  
  Serial.println("=== FIN TEST FILTROS ===");
}

// ========================================
// DEBUG DEL ESTADO DEL FILTRO
// ========================================
void debug_filter_state() {
  Serial.println("\n=== DEBUG ESTADO FILTRO ===");
  
  Serial.print("Tipo de filtro actual: ");
  Serial.println(filter_type);
  
  Serial.print("Descripción: ");
  switch(filter_type) {
    case 0: Serial.println("BYPASS (sin filtrado)"); break;
    case 1: Serial.println("FIR pasa-bajas"); break;
    case 2: Serial.println("IIR Butterworth"); break;
    case 3: Serial.println("Adaptativo LMS"); break;
    default: Serial.println("DESCONOCIDO"); break;
  }
  
  // Estado del buffer FIR
  if(filter_type == 1) {
    Serial.println("Estado buffer FIR:");
    Serial.print("  Primeros 5 valores: ");
    for(int i = 0; i < 5 && i < FIR_TAPS; i++) {
      Serial.print(fir_buffer[i]);
      Serial.print(" ");
    }
    Serial.println();
    
    Serial.print("  Suma de coeficientes: ");
    float suma_coef = 0;
    for(int i = 0; i < FIR_TAPS; i++) {
      suma_coef += fir_coeffs[i];
    }
    Serial.println(suma_coef);
  }
  
  // Estado del buffer IIR
  if(filter_type == 2) {
    Serial.println("Estado buffer IIR:");
    Serial.print("  Entrada X: ");
    for(int i = 0; i <= IIR_ORDER && i < 5; i++) {
      Serial.print(iir_x[i]);
      Serial.print(" ");
    }
    Serial.println();
    
    Serial.print("  Salida Y: ");
    for(int i = 0; i <= IIR_ORDER && i < 5; i++) {
      Serial.print(iir_y[i]);
      Serial.print(" ");
    }
    Serial.println();
  }
  
  // Test rápido
  Serial.println("Test rápido:");
  int test_input = 512;
  int test_output = apply_selected_filter(test_input);
  Serial.print("  ");
  Serial.print(test_input);
  Serial.print(" -> ");
  Serial.print(test_output);
  Serial.print(" (diferencia: ");
  Serial.print(test_output - test_input);
  Serial.println(")");
  
  Serial.println("=== FIN DEBUG ===");
}