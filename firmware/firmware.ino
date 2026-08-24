const char* RETURN_DONE = "DONE\n";
const char* RETURN_PONG = "PONG!\n";
const char* RETURN_INVALID_COMMAND = "ERROR_INVALID_COMMAND\n";
const char* RETURN_BAD_ARGS = "ERROR_BAD_ARGUMENT_COUNT\n";
const char* RETURN_BAD_ARGVAL = "ERROR_BAD_ARGUMENT_VALUE\n";
const char* RETURN_OUT_OF_RANGE = "ERROR_OUT_OF_RANGE\n";

const int MAX_ARGS = 3;

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

    // get the command itself
    char* command = strtok(buf, " ");

    // collect arguments
    char* args[MAX_ARGS];
    int argCount = 0;
    char* tok;
    while ((tok = strtok(NULL, " ")) != NULL && argCount < MAX_ARGS) {
      args[argCount++] = tok;
    }

    // ping
    if (strcmp(command, "PING") == 0) {
      for (int i = 0; i < 5; i++) {
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
      }
      Serial.write(RETURN_PONG);
    }
    // move
    else if (strcmp(command, "MOVE") == 0) {
      if (argCount != 3) {
        Serial.write(RETURN_BAD_ARGS);
        return;
      }
      int x = atoi(args[0]);
      int y = atoi(args[1]);
      int z = atoi(args[2]);
      if (x > 180 || x < 0 || y > 180 || y < 0 || z > 180 || z < 0) {
        Serial.write(RETURN_OUT_OF_RANGE);
        return;
      }

      // do move logic
      Serial.write(RETURN_DONE);
    }
    // wait
    else if (strcmp(command, "WAIT") == 0) {
      if (argCount != 1) {
        Serial.write(RETURN_BAD_ARGS);
        return;
      }

      int time = atoi(args[0]);
      if (time <= 0) {
        Serial.write(RETURN_BAD_ARGVAL);
        return;
      }

      delay(time);
      Serial.write(RETURN_DONE);
    }
    // gripper control
    else if (strcmp(command, "GRIPPER") == 0) {
      if (argCount > 1) {
        Serial.write(RETURN_BAD_ARGS);
        return;
      }

      int arg = atoi(args[0]);

      if (arg != 0 && arg != 1) {
        Serial.write(RETURN_BAD_ARGVAL);
        return;
      }

      // do gripper logic
      Serial.write(RETURN_DONE);
    }
    // fallback
    else {
      Serial.write(RETURN_INVALID_COMMAND);
    }
  }
}