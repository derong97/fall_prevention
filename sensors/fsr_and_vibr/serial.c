/* 

Need to install SimpleKalmanFilter Arduino Library by Denys Sene

*/

#include <SimpleKalmanFilter.h>

const long SERIAL_REFRESH_TIME = 100;

SimpleKalmanFilter simpleKalmanFilterA(2, 2, 0.01);
SimpleKalmanFilter simpleKalmanFilterB(2, 2, 0.01);
SimpleKalmanFilter simpleKalmanFilterC(2, 2, 0.01);
SimpleKalmanFilter simpleKalmanFilterD(2, 2, 0.01);

//FOR A BLUE
int fsrAnalogPinA = 0; // FSR is connected to analog 0
int fsrReadingA;      // the analog reading from the FSR resistor divider
float fsrReadingKalmanA;

//FOR B RED
int fsrAnalogPinB = 1; // FSR is connected to analog 0
int fsrReadingB;      // the analog reading from the FSR resistor divider
float fsrReadingKalmanB;

//FOR C GREEN
int fsrAnalogPinC = 2; // FSR is connected to analog 0
int fsrReadingC;     // the analog reading from the FSR resistor divider
float fsrReadingKalmanC;

//FOR D ORANGE
int fsrAnalogPinD = 3; // FSR is connected to analog 0
int fsrReadingD;      // the analog reading from the FSR resistor divider
float fsrReadingKalmanD;

//FOR VIBRATION SENSOR 
int vibr_tissue = 6;
int vibr_bidet = 4;

// rate of use
const int interval = 50;
int bidet_temp_arr[interval];
int tissue_temp_arr[interval];
int idx = 0;

int prev_value_bidet = 0;
int prev_value_tissue = 0;

void setup(void) {
  Serial.begin(9600);   // We'll send debugging information via the Serial monitor
}
 
void loop(void) {
  delay(SERIAL_REFRESH_TIME);
  
  int vibration_value_tissue = pulseIn(vibr_tissue, HIGH, SERIAL_REFRESH_TIME * 1000); // SERIAL_REFRESH_TIME*1000
  int vibration_value_bidet = pulseIn(vibr_bidet, HIGH, SERIAL_REFRESH_TIME * 1000); // SERIAL_REFRESH_TIME*1000

  idx = idx % interval;
  long start_timer = millis();

  int counter_bidet = 0;
  int counter_tissue = 0;
  
  while (millis() - start_timer < 600) {     //200 
    if (vibration_value_tissue != 0 && prev_value_tissue == 0) {
        counter_tissue += 1;
    }
    prev_value_tissue = vibration_value_tissue;

    if (vibration_value_bidet != 0 && prev_value_bidet == 0) {
      counter_bidet += 1;
    }
    prev_value_bidet = vibration_value_bidet;   
  }
  
  tissue_temp_arr[idx] = counter_tissue;
  bidet_temp_arr[idx] = counter_bidet;

  idx ++;
  
  fsrReadingA = analogRead(fsrAnalogPinA);
  fsrReadingB = analogRead(fsrAnalogPinB);
  fsrReadingC = analogRead(fsrAnalogPinC);
  fsrReadingD = analogRead(fsrAnalogPinD);

  float fsrReadingKalmanA = simpleKalmanFilterA.updateEstimate(fsrReadingA);
  float fsrReadingKalmanB = simpleKalmanFilterB.updateEstimate(fsrReadingB);
  float fsrReadingKalmanC = simpleKalmanFilterC.updateEstimate(fsrReadingC);
  float fsrReadingKalmanD = simpleKalmanFilterD.updateEstimate(fsrReadingD);

  int sum_bidet = 0;
  int sum_tissue = 0;
  for (int i = 0; i < interval; i++){
    sum_bidet += bidet_temp_arr[i];
    sum_tissue += tissue_temp_arr[i];
  }
  
  Serial.print(fsrReadingKalmanA);
  Serial.print(",");
  Serial.print(fsrReadingKalmanB);
  Serial.print(",");
  Serial.print(fsrReadingKalmanC);
  Serial.print(",");
  Serial.print(fsrReadingKalmanD);
  Serial.print(",");
  Serial.print(sum_bidet);
  Serial.print(",");
  Serial.println(sum_tissue);
}
