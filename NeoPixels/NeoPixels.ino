// import library
#include <Adafruit_NeoPixel.h>

// declare pin + number of leds
#define PIN      2
#define N_LEDS 36

// create instance
Adafruit_NeoPixel strip = Adafruit_NeoPixel(N_LEDS, PIN, NEO_GRB + NEO_KHZ800);

// colours
uint32_t red = strip.Color(255, 0, 0);
uint32_t orange = strip.Color(255, 165, 0);
uint32_t yellow = strip.Color(255, 255, 0);
uint32_t green = strip.Color(0, 255, 0);
uint32_t cyan = strip.Color(0, 255, 255);
uint32_t blue = strip.Color(0, 0, 255);
uint32_t magenta = strip.Color(255, 0, 255);
uint32_t white = strip.Color(255, 255, 255);
// save colours to an array
uint32_t colours[] = {red, orange, yellow, green, cyan, blue, magenta};

// indexes of leds at places of books
int places[][3] = {
  {13, 14, 15}, // book 0
  {16, 17, 18}, // book 1
  {19, 20, 21}, // book 2
  {22, 23, 24}, // book 3
  {25, 26, 27}, // book 4
  {28, 29, 30}, // book 5
  {31, 32, 33}, // book 6
  {34, 35, 36}  // book 7
};

// initialise place variables
int right_place = 10;
int detected_place = 10;

// boolean to register what number got send through
bool firstTransmission = true;

void setup() {
  // start serial monitor
  Serial.begin(9600);
  // start strip
  strip.begin();
  // make strip empty
  strip.show();
}

void loop() {

  if (Serial.available() > 0) {
    // read place
    String received = Serial.readString();
    received.trim();
    
    // check first number that was received --> righ_place
    // if received can be converted to an integer, it is an integer
    // but if string "0" gets converted, it will return 0 even if it is an integer
    // when right_place=10 and detected_place=10 the program has been reseted
    if ((received.toInt() != 0 or received == "0") and right_place==10 and detected_place==10) {
      // clear strip
      clear_strip();
      // convert received string to integer
      right_place = received.toInt();
      // show place
      light_up_a_place(right_place, white);
      strip.show();
    }
    // check second number that was received --> detected_place
    else {
      // when right_place!=10 and detected_place=10 the if-part of the condition has been executed
      if ((received.toInt() != 0 or received == "0") and right_place != 10 and detected_place==10) {
        // clear strip
        clear_strip();
        // convert received string to integer
        detected_place = received.toInt();
        
        // if right place
        if (detected_place == 9) {
          light_up_a_place(right_place, green);
        }
        // if not right place
        else
        {
          // if borrowed
          if (detected_place == 8) {
            light_up_a_place(right_place, blue);
          }
          else {
            // if wrong place
            light_up_a_place(detected_place, red);
          }
        }
      
        // wait three seconds
        delay(3000);
      }

      // if no number was received, clear strip
      else {
        clear_strip();
        right_place = 10;
        detected_place = 10;
      }

    }
  }
}

// show a place in a certain colour
void light_up_a_place(int place, uint32_t colour) {
  for (int i = 0; i < 3; i++) {
    strip.setPixelColor(places[place][i], colour);
    strip.show();
  }
  delay(500);
}

// shut all leds down
void clear_strip() {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, 0);
    strip.show();
  }
}

