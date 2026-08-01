const char* RETURN_DONE = "DONE\n";
const char* RETURN_PONG = "PONG!\n";
const char* RETURN_INVALID_COMMAND = "ERROR_INVALID_COMMAND\n";
const char* RETURN_BAD_ARGS = "ERROR_BAD_ARGUMENT_COUNT\n";
const char* RETURN_BAD_ARGVAL = "ERROR_BAD_ARGUMENT_VALUE\n";

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();

    char buf[64];
    message.toCharArray(buf, sizeof(buf));

    char* command = strtok(buf, " ");



    if (strcmp(command, "PING") == 0) {
      for (int i = 0; i < 5; i++) {
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
      }
      Serial.write(RETURN_PONG);
    }
    else if (strcmp(command, "MOVE") == 0) {
      Serial.write(RETURN_DONE);
    }
    else if (strcmp(command, "WAIT") == 0) {
      char* var1 = strtok(NULL, " ");
      int time = atoi(var1);

      delay(time);
      
      Serial.write(RETURN_DONE);
    }
    else {
      Serial.write(RETURN_INVALID_COMMAND);
    }
  }
}