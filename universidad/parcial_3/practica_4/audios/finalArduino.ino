

// Configuración del sistema
const int AUDIO_OUT = 9;        // Salida PWM para audio
const int STATUS_LED = 13;      // LED de estado
const int BUFFER_SIZE = 600;    // Buffer optimizado para lotes

// Buffers para procesamiento
int input_buffer[BUFFER_SIZE];
int output_buffer[BUFFER_SIZE];
int buffer_index = 0;
bool buffer_ready = false;
bool collecting_data = false;

// Control de filtros
int filter_type = 0;  // 0=Bypass, 1=FIR, 2=IIR
unsigned long last_led_update = 0;

// Filtro FIR optimizado (orden 20)
const int FIR_TAPS = 21;
float fir_coeffs[FIR_TAPS] = {
  -0.0018, -0.0052, -0.0095, -0.0108, -0.0037,
   0.0152,  0.0499,  0.0963,  0.1453,  0.1858,
   0.2078,  0.1858,  0.1453,  0.0963,  0.0499,
   0.0152, -0.0037, -0.0108, -0.0095, -0.0052, -0.0018
};
float fir_buffer[FIR_TAPS] = {0};

// Filtro IIR Butterworth (orden 4)
float iir_b[5] = {0.0067, 0.0268, 0.0402, 0.0268, 0.0067};
float iir_a[5] = {1.0000, -2.3695, 2.3140, -1.0547, 0.1874};
float iir_x[5] = {0, 0, 0, 0, 0};
float iir_y[5] = {0, 0, 0, 0, 0};

void setup() {
  Serial.begin(115200);
  pinMode(AUDIO_OUT, OUTPUT);
  pinMode(STATUS_LED, OUTPUT);
  
  // Mensaje de inicio
  Serial.println("=========================================");
  Serial.println("  ARDUINO MEGA - FILTROS DIGITALES");
  Serial.println("  Para clase de 150 minutos");
  Serial.println("=========================================");
  Serial.print("Buffer size: ");
  Serial.print(BUFFER_SIZE);
  Serial.println(" muestras");
  Serial.println("Filtros disponibles:");
  Serial.println("  0 = Bypass (sin filtro)");
  Serial.println("  1 = FIR pasa-bajas (fc=800Hz)");
  Serial.println("  2 = IIR Butterworth (fc=800Hz)");
  Serial.println("");
  Serial.println("COMANDOS:");
  Serial.println("  t = Test de comunicación");
  Serial.println("  r = Reset completo");
  Serial.println("  0/1/2 = Seleccionar filtro");
  Serial.println("  c = Iniciar captura");
  Serial.println("  s = Enviar datos");
  Serial.println("  DATA:xxx = Enviar muestra");
  Serial.println("=========================================");
  
  // Parpadeo inicial del LED
  for(int i = 0; i < 5; i++) {
    digitalWrite(STATUS_LED, HIGH);
    delay(100);
    digitalWrite(STATUS_LED, LOW);
    delay(100);
  }
  
  Serial.println("SISTEMA LISTO - Esperando comandos...");
}

void loop() {
  // Procesar comandos serie
  if (Serial.available() > 0) {
    handle_serial_command();
  }
  
  // Actualizar LED de estado
  update_status_led();
  
  // Pequeña pausa para estabilidad
  delay(1);
}

void handle_serial_command() {
  String command = Serial.readStringUntil('\n');
  command.trim();
  
  if (command == "t" || command == "T") {
    // Test de comunicación
    test_communication();
    
  } else if (command == "r" || command == "R") {
    // Reset completo
    reset_system();
    
  } else if (command == "0") {
    // Filtro Bypass
    filter_type = 0;
    reset_filters();
    Serial.println("FILTRO: BYPASS activado");
    
  } else if (command == "1") {
    // Filtro FIR
    filter_type = 1;
    reset_filters();
    Serial.println("FILTRO: FIR pasa-bajas activado (fc=800Hz)");
    Serial.print("Orden del filtro: ");
    Serial.println(FIR_TAPS - 1);
    
  } else if (command == "2") {
    // Filtro IIR
    filter_type = 2;
    reset_filters();
    Serial.println("FILTRO: IIR Butterworth activado (fc=800Hz)");
    Serial.print("Orden del filtro: ");
    Serial.println(4);
    
  } else if (command == "c" || command == "C") {
    // Iniciar captura
    start_capture();
    
  } else if (command == "s" || command == "S") {
    // Enviar datos
    send_data();
    
  } else if (command.startsWith("DATA:")) {
    // Procesar muestra de audio
    int sample = command.substring(5).toInt();
    process_audio_sample(sample);
    
  } else {
    Serial.println("COMANDO NO RECONOCIDO");
    Serial.println("Comandos válidos: t, r, 0, 1, 2, c, s, DATA:xxx");
  }
}

void test_communication() {
  Serial.println("TEST DE COMUNICACIÓN");
  Serial.println("====================");
  Serial.print("Arduino Mega conectado en puerto serie ");
  Serial.println("COM4");
  Serial.print("Velocidad: ");
  Serial.print(115200);
  Serial.println(" bps");
  Serial.print("Buffer disponible: ");
  Serial.print(BUFFER_SIZE);
  Serial.println(" muestras");
  Serial.print("Memoria libre (aprox): ");
  Serial.print(freeRam());
  Serial.println(" bytes");
  Serial.print("Filtro actual: ");
  
  switch(filter_type) {
    case 0: Serial.println("Bypass"); break;
    case 1: Serial.println("FIR"); break;
    case 2: Serial.println("IIR"); break;
  }
  
  Serial.println("COMUNICACIÓN OK");
}

void reset_system() {
  Serial.println("RESET COMPLETO DEL SISTEMA");
  
  // Reset variables
  buffer_index = 0;
  buffer_ready = false;
  collecting_data = false;
  filter_type = 0;
  
  // Limpiar buffers
  memset(input_buffer, 0, sizeof(input_buffer));
  memset(output_buffer, 0, sizeof(output_buffer));
  
  // Reset filtros
  reset_filters();
  
  // Salida PWM neutral
  analogWrite(AUDIO_OUT, 127);
  
  Serial.println("Sistema reiniciado correctamente");
}

void reset_filters() {
  // Reset FIR
  for (int i = 0; i < FIR_TAPS; i++) {
    fir_buffer[i] = 0;
  }
  
  // Reset IIR
  for (int i = 0; i < 5; i++) {
    iir_x[i] = 0;
    iir_y[i] = 0;
  }
}

void start_capture() {
  Serial.println("INICIANDO CAPTURA DE AUDIO");
  Serial.print("Filtro seleccionado: ");
  
  switch(filter_type) {
    case 0: Serial.println("Bypass"); break;
    case 1: Serial.println("FIR pasa-bajas"); break;
    case 2: Serial.println("IIR Butterworth"); break;
  }
  
  // Reset buffer
  buffer_index = 0;
  buffer_ready = false;
  collecting_data = true;
  
  Serial.print("Buffer preparado para ");
  Serial.print(BUFFER_SIZE);
  Serial.println(" muestras");
  Serial.println("LISTO PARA RECIBIR DATOS");
}

void process_audio_sample(int input_sample) {
  // Verificar si hay espacio en buffer
  if (buffer_index >= BUFFER_SIZE) {
    if (collecting_data) {
      collecting_data = false;
      buffer_ready = true;
      Serial.println("BUFFER COMPLETO - Listo para envío");
    }
    return;
  }
  
  // Validar entrada (0-1023 para ADC de 10 bits)
  input_sample = constrain(input_sample, 0, 1023);
  
  // Aplicar filtro seleccionado
  int output_sample;
  
  switch(filter_type) {
    case 0:
      // Bypass - sin filtrado
      output_sample = input_sample;
      break;
      
    case 1:
      // Filtro FIR
      output_sample = apply_fir_filter(input_sample);
      break;
      
    case 2:
      // Filtro IIR
      output_sample = apply_iir_filter(input_sample);
      break;
      
    default:
      output_sample = input_sample;
  }
  
  // Guardar en buffers
  input_buffer[buffer_index] = input_sample;
  output_buffer[buffer_index] = output_sample;
  buffer_index++;
  
  // Salida PWM (opcional, para monitoreo)
  int pwm_value = map(output_sample, 0, 1023, 0, 255);
  analogWrite(AUDIO_OUT, pwm_value);
  
  // Indicar progreso cada 100 muestras
  if (buffer_index % 100 == 0) {
    Serial.print("Muestras procesadas: ");
    Serial.print(buffer_index);
    Serial.print("/");
    Serial.println(BUFFER_SIZE);
  }
  
  // Verificar si buffer está completo
  if (buffer_index >= BUFFER_SIZE) {
    collecting_data = false;
    buffer_ready = true;
    Serial.println("PROCESAMIENTO COMPLETADO");
  }
}

int apply_fir_filter(int input) {
  // Desplazar buffer FIR
  for (int i = FIR_TAPS - 1; i > 0; i--) {
    fir_buffer[i] = fir_buffer[i - 1];
  }
  fir_buffer[0] = input;
  
  // Calcular convolución
  float output = 0;
  for (int i = 0; i < FIR_TAPS; i++) {
    output += fir_coeffs[i] * fir_buffer[i];
  }
  
  // Asegurar rango válido
  return constrain((int)output, 0, 1023);
}

int apply_iir_filter(int input) {
  // Desplazar buffers de entrada
  for (int i = 4; i > 0; i--) {
    iir_x[i] = iir_x[i - 1];
  }
  iir_x[0] = input;
  
  // Desplazar buffers de salida
  for (int i = 4; i > 0; i--) {
    iir_y[i] = iir_y[i - 1];
  }
  
  // Calcular ecuación en diferencias
  iir_y[0] = 0;
  
  // Parte numerador (feedforward)
  for (int i = 0; i < 5; i++) {
    iir_y[0] += iir_b[i] * iir_x[i];
  }
  
  // Parte denominador (feedback)
  for (int i = 1; i < 5; i++) {
    iir_y[0] -= iir_a[i] * iir_y[i];
  }
  
  // Asegurar rango válido
  return constrain((int)iir_y[0], 0, 1023);
}

void send_data() {
  if (!buffer_ready) {
    Serial.println("ERROR: Buffer no está listo");
    Serial.println("Primero ejecuta captura (comando 'c')");
    return;
  }
  
  Serial.println("ENVIANDO DATOS PROCESADOS");
  Serial.print("Filtro usado: ");
  
  switch(filter_type) {
    case 0: Serial.println("Bypass"); break;
    case 1: Serial.println("FIR"); break;
    case 2: Serial.println("IIR"); break;
  }
  
  Serial.print("Muestras: ");
  Serial.println(buffer_index);
  
  // Enviar marcador de inicio
  Serial.println("INICIO_DATOS");
  
  // Enviar header CSV
  Serial.println("index,input,output");
  
  // Enviar datos
  for (int i = 0; i < buffer_index; i++) {
    Serial.print(i);
    Serial.print(",");
    Serial.print(input_buffer[i]);
    Serial.print(",");
    Serial.println(output_buffer[i]);
    
    // Pausa pequeña cada 50 líneas para evitar overflow
    if ((i + 1) % 50 == 0) {
      delay(10);
    }
  }
  
  // Enviar marcador de fin
  Serial.println("FIN_DATOS");
  Serial.println("ENVÍO COMPLETADO");
  
  // Calcular estadísticas básicas
  long sum_input = 0, sum_output = 0;
  for (int i = 0; i < buffer_index; i++) {
    sum_input += input_buffer[i];
    sum_output += output_buffer[i];
  }
  
  Serial.print("Promedio entrada: ");
  Serial.println(sum_input / buffer_index);
  Serial.print("Promedio salida: ");
  Serial.println(sum_output / buffer_index);
}

void update_status_led() {
  unsigned long current_time = millis();
  
  if (collecting_data) {
    // Parpadeo rápido durante captura
    if (current_time - last_led_update > 100) {
      digitalWrite(STATUS_LED, !digitalRead(STATUS_LED));
      last_led_update = current_time;
    }
  } else if (buffer_ready) {
    // Encendido fijo cuando datos listos
    digitalWrite(STATUS_LED, HIGH);
  } else {
    // Parpadeo lento en espera
    if (current_time - last_led_update > 1000) {
      digitalWrite(STATUS_LED, !digitalRead(STATUS_LED));
      last_led_update = current_time;
    }
  }
}

int freeRam() {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}