int ledPin = 13; // The pin where your LED is connected
int pin12 = 12;   // Pin 12 will be set high

void setup() {
  pinMode(ledPin, OUTPUT);  // Set LED pin as output
  pinMode(pin12, OUTPUT);   // Set pin 12 as output
  
  digitalWrite(pin12, HIGH);  // Set pin 12 high (it stays high)
  Serial.begin(9600);        // Initialize serial communication
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();  // Read the incoming command from Python
    
    if (command == '1') {
      digitalWrite(ledPin, HIGH);  // Turn the LED on
      Serial.println("LED ON");
    } else if (command == '0') {
      digitalWrite(ledPin, LOW);   // Turn the LED off
      Serial.println("LED OFF");
    }
  }
}
