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

    char* token = strtok(buf, " ");
    // char[]* command = token;

    digitalWrite(LED_BUILTIN, LOW);
    delay(250);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(250);

    Serial.write("DONE\n");


  }
}