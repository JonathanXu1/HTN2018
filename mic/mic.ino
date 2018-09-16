#include <Filter.h>
#include <math.h>
#include <CurieBLE.h>

const int mic1 = A0;
const int mic2 = A1;
const int mic3 = A2;
ExponentialFilter<long> FilteredNoise1(3, 0);
ExponentialFilter<long> FilteredNoise2(3, 0);
ExponentialFilter<long> FilteredNoise3(3, 0);
long diff1, diff2, diff3;

void setup()
{
    Serial.begin(9600);
    long sum1 = 0;
    long sum2 = 0;
    long sum3 = 0;
    for(int i = 0; i < 1000; i++){
       sum1 += analogRead(mic1);
       sum2 += analogRead(mic2);
       sum3 += analogRead(mic3);
       delay(1);
    }
    diff1 = sum1/1000;
    diff2 = sum2/1000;
    diff3 = sum3/1000;
}

void loop()
{
//    long noise1 = analogRead(mic1);
//    FilteredNoise1.Filter(noise1);
//    long smoothNoise1 = FilteredNoise1.Current()-diff1;
//
//    long noise2 = analogRead(mic2);
//    FilteredNoise2.Filter(noise2);
//    long smoothNoise2 = FilteredNoise2.Current()-diff2;
//    
//    long noise3 = analogRead(mic3);
//    FilteredNoise3.Filter(noise3);
//    long smoothNoise3 = FilteredNoise3.Current()-diff3;
    long sum1, sum2, sum3;
    sum1 = sum2 = sum3 = 0;
    for(int i = 0; i < 30; i++){
       sum1 += analogRead(mic1);
       sum2 += analogRead(mic2);
       sum3 += analogRead(mic3);
       delay(1);
    }
    long smoothNoise1 = sum1/30 - diff1;
    long smoothNoise2 = sum2/30 - diff2;
    long smoothNoise3 = sum3/30 - diff3;

    //Calculates angle
    long N2X = sin(1.0472)*smoothNoise2; //60 90
    long N2Y = cos(1.0472)*smoothNoise2;

    long N3X = sin(1.0472)*smoothNoise3; //60 90
    long N3Y = cos(1.0472)*smoothNoise3;

    long X = N3X-N2X;
//    Serial.print("x: ");
//    Serial.println(X);
    long Y = smoothNoise1 - N2Y - N3Y;
//    Serial.print("y: ");
//    Serial.println(Y);

    long H = sqrt(pow(abs(X),2) + pow(abs(Y),2));
//    Serial.print("Hype");
//    Serial.println(H);     
    
    long AR = atan2(abs(Y),abs(X))*180/3.14;
    if(Y >= 0 && X >= 0){
        AR = 90-AR;
    } else if(Y >= 0 && X < 0){
        AR += 270;
    } else if(Y < 0 && X < 0){
        AR = 270 - AR;
    } else if(Y < 0 && X >= 0){
        AR += 90;
    }

    if(AR < 0){
      AR += 360;
    }
    AR = AR % 360;
    
  
//    Serial.print("Relative angle: ");
//    Serial.println(AR);
    
    long angle;
   
    if(Y>0){ //ar =180
       //Q1
      if(X<0){
        angle = 180+AR;
      }

      //Q2
      else{
        angle = 90+AR;
      }
    }

    else{ //ar=0
       //Q1
      if(X<0){
        angle = 270-AR;
      }

      //Q2
      else{
        angle = 90+AR;
      }
    }
    
    Serial.print(X);
    Serial.print(",");
    Serial.print(Y);
    //Serial.print(angle);
    Serial.print(",");
    Serial.print(smoothNoise1);
    Serial.print(","); 
    Serial.print(smoothNoise2);
    Serial.print(","); 
    Serial.println(smoothNoise3);
    delay(50);
}

