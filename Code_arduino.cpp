#include <Servo.h>

const int trigPin = 9;
const int echoPin = 10;
const int servoPin = 7;      // пин управления сервомотором

Servo myServo;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myServo.attach(servoPin);
  myServo.write(15);          // стартовый угол
  delay(1000);                // пауза для стабилизации
}

void loop() {
  // Поворачиваем сервомотор от 15 до 165 градусов
  for (int angle = 15; angle <= 165; angle++) {
    myServo.write(angle);
    delay(50);                // время для поворота

    long distance = getDistance();

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }

  // Возвращаем серво обратно от 165 до 15 градусов
  for (int angle = 165; angle >= 15; angle--) {
    myServo.write(angle);
    delay(50);

    long distance = getDistance();

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }
}

long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // максимум 30мс ожидания

  if (duration == 0) {
    // возвращаем -1 если нет эхо
    return -1;
  }

  long distance = duration * 0.034 / 2;
  return distance;
}
