const int analogPin = A0;     // Pin analógico de entrada
const int ledPin = 9;         // Pin PWM para visualización (opcional)


const unsigned long SAMPLE_PERIOD = 5000;  
const int BUFFER_SIZE = 128;               
const unsigned long BUFFER_FILL_TIME = 10000; 

// Buffers para almacenar muestras
int sample_buffer[BUFFER_SIZE];           
int filtered_buffer[BUFFER_SIZE];         
int buffer_index = 0;                     
bool buffer_full = false;                 
bool collecting_data = false;             // Estado de recolección

// Parámetros para filtro FIR paso-bajas CORREGIDOS
const int FIR_ORDER = 10;
float fir_coeffs[FIR_ORDER + 1] = {
  0.0087, 0.0279, 0.0741, 0.1348, 0.1932, 0.2123, 
  0.1932, 0.1348, 0.0741, 0.0279, 0.0087
};
float fir_buffer[FIR_ORDER + 1] = {0};  

// Variable para seleccionar tipo de filtro
int filter_type = 0;  // 0: Sin filtro, 1: FIR

// Variables de control de tiempo
unsigned long collection_start_time = 0;

void setup() {
  Serial.begin(115200);       
  pinMode(ledPin, OUTPUT);    
  
  Serial.println("=== Sistema de Adquisición y Filtrado Digital ===");
  Serial.println("Comandos disponibles:");
  Serial.println("0: Sin filtro");
  Serial.println("1: Filtro FIR");
  Serial.println("s: Iniciar recolección de datos");
  Serial.println("r: Reset buffer");
  Serial.println("========================================");
  
  analogReference(DEFAULT);
  delay(1000);                
}

void loop() {
  static unsigned long last_sample = 0;
  unsigned long current_time = micros();
  
  // Verificar comandos seriales
  handle_serial_commands();
  
  // Solo muestrear si estamos recolectando datos
  if (collecting_data && (current_time - last_sample >= SAMPLE_PERIOD)) {
    
    // Leer valor analógico
    int sensor_value = analogRead(analogPin);
    
    // Aplicar filtro según tipo seleccionado
    int filtered_value = apply_selected_filter(sensor_value);
    
    // Visualización opcional mediante PWM
    analogWrite(ledPin, map(filtered_value, 0, 1023, 0, 255));
    
    // Guardar en buffer
    if (buffer_index < BUFFER_SIZE) {
      sample_buffer[buffer_index] = sensor_value;
      filtered_buffer[buffer_index] = filtered_value;
      buffer_index++;
      
      // Mostrar progreso cada 16 muestras
      if (buffer_index % 16 == 0) {
        Serial.print("Progreso: ");
        Serial.print((buffer_index * 100) / BUFFER_SIZE);
        Serial.println("%");
      }
      
      if (buffer_index >= BUFFER_SIZE) {
        buffer_full = true;
        collecting_data = false;
        Serial.println("*** BUFFER COMPLETO ***");
        Serial.println("Envie 's' para obtener los datos");
        Serial.println("Envie 'r' para reiniciar y recolectar nuevamente");
      }
    }
    
    last_sample = current_time;
  }
  
  // Timeout para recolección
  if (collecting_data && (millis() - collection_start_time > BUFFER_FILL_TIME)) {
    Serial.println("Timeout: Parando recolección");
    collecting_data = false;
    if (buffer_index > 0) {
      Serial.print("Muestras recolectadas: ");
      Serial.println(buffer_index);
      Serial.println("Envie 's' para obtener los datos parciales");
    }
  }
}

void handle_serial_commands() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    
    switch(cmd) {
      case '0':
        filter_type = 0;
        Serial.println(">>> Filtro: DESACTIVADO");
        break;
        
      case '1':
        filter_type = 1;
        Serial.println(">>> Filtro: FIR ACTIVADO");
        break;
        
      case 's':
      case 'S':
        if (buffer_full || buffer_index > 0) {
          send_buffer();
        } else if (!collecting_data) {
          start_data_collection();
        } else {
          Serial.println("Ya recolectando datos...");
        }
        break;
        
      case 'r':
      case 'R':
        reset_buffer();
        break;
        
      default:
        // Ignorar otros caracteres
        break;
    }
  }
}

void start_data_collection() {
  Serial.println(">>> INICIANDO RECOLECCIÓN DE DATOS <<<");
  Serial.print("Tipo de filtro: ");
  Serial.println(filter_type == 0 ? "Sin filtro" : "FIR");
  Serial.print("Muestras a recolectar: ");
  Serial.println(BUFFER_SIZE);
  Serial.print("Frecuencia de muestreo: ");
  Serial.print(1000000.0 / SAMPLE_PERIOD);
  Serial.println(" Hz");
  Serial.println("Recolectando...");
  
  reset_buffer();
  collecting_data = true;
  collection_start_time = millis();
}

int apply_selected_filter(int new_sample) {
  switch(filter_type) {
    case 0:  // Sin filtro
      return new_sample;
      
    case 1:  // Filtro FIR
      return apply_fir_filter(new_sample);
      
    default:
      return new_sample;
  }
}

int apply_fir_filter(int new_sample) {
  // Desplazar valores en el buffer circular
  for (int i = FIR_ORDER; i > 0; i--) {
    fir_buffer[i] = fir_buffer[i-1];
  }
  
  // Añadir nueva muestra
  fir_buffer[0] = new_sample;
  
  // Aplicar convolución
  float result = 0;
  for (int i = 0; i <= FIR_ORDER; i++) {
    result += fir_coeffs[i] * fir_buffer[i];
  }
  
  // Limitar resultado a rango válido
  if (result < 0) result = 0;
  if (result > 1023) result = 1023;
  
  return (int)result;
}

void send_buffer() {
  int samples_to_send = buffer_full ? BUFFER_SIZE : buffer_index;
  
  if (samples_to_send == 0) {
    Serial.println("ERROR: Buffer vacío");
    return;
  }
  
  Serial.println(">>> ENVIANDO DATOS <<<");
  Serial.print("Muestras: ");
  Serial.println(samples_to_send);
  
  // Pequeña pausa para sincronización
  delay(100);
  
  // Enviar encabezado CSV
  Serial.println("index,original,filtered");
  
  // Enviar datos
  for (int i = 0; i < samples_to_send; i++) {
    Serial.print(i);
    Serial.print(",");
    Serial.print(sample_buffer[i]);
    Serial.print(",");
    Serial.println(filtered_buffer[i]);
    
    // Pequeña pausa cada 10 líneas para evitar overflow del buffer serie
    if ((i + 1) % 10 == 0) {
      delay(10);
    }
  }
  
  Serial.println(">>> FIN DE DATOS <<<");
  
  // Estadísticas básicas
  print_statistics(samples_to_send);
}

void print_statistics(int count) {
  if (count == 0) return;
  
  long sum_orig = 0, sum_filt = 0;
  int min_orig = 1023, max_orig = 0;
  int min_filt = 1023, max_filt = 0;
  
  for (int i = 0; i < count; i++) {
    sum_orig += sample_buffer[i];
    sum_filt += filtered_buffer[i];
    
    if (sample_buffer[i] < min_orig) min_orig = sample_buffer[i];
    if (sample_buffer[i] > max_orig) max_orig = sample_buffer[i];
    if (filtered_buffer[i] < min_filt) min_filt = filtered_buffer[i];
    if (filtered_buffer[i] > max_filt) max_filt = filtered_buffer[i];
  }
  
  Serial.println("=== ESTADÍSTICAS ===");
  Serial.print("Original - Min: "); Serial.print(min_orig);
  Serial.print(", Max: "); Serial.print(max_orig);
  Serial.print(", Promedio: "); Serial.println(sum_orig / count);
  
  Serial.print("Filtrada - Min: "); Serial.print(min_filt);
  Serial.print(", Max: "); Serial.print(max_filt);
  Serial.print(", Promedio: "); Serial.println(sum_filt / count);
  Serial.println("==================");
}

void reset_buffer() {
  buffer_index = 0;
  buffer_full = false;
  collecting_data = false;
  
  // Limpiar buffers
  for (int i = 0; i < BUFFER_SIZE; i++) {
    sample_buffer[i] = 0;
    filtered_buffer[i] = 0;
  }
  
  // Limpiar buffer del filtro FIR
  for (int i = 0; i <= FIR_ORDER; i++) {
    fir_buffer[i] = 0;
  }
  
  Serial.println(">>> BUFFER REINICIADO <<<");
}