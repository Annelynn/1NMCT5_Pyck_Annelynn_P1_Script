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
int right_place;
int detected_place;

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
    Serial.println(received);

    // check first number that was received --> righ_place
    if (firstTransmission == true and received.toInt() != 0) {
      // clear strip
      clear_strip();
      // convert received string to integer
      right_place = received.toInt();
      // show place
      rainbow_drops(right_place);
      // set boolean to false so second part can be executed
      firstTransmission = false;
    }
    // check second number that was received --> detected_place
    else {
      if (firstTransmission == false and received.toInt() != 0) {
        // clear strip
        clear_strip();
        // convert received string to integer
        detected_place = received.toInt();
        // if right place
        if (detected_place == 9) {
          light_up_a_place(right_place, green);
        }
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
        // when a second value was received, another value can be read
        if (detected_place != right_place) {
          firstTransmission = true;
        }
      }

      // if no number was received, clear strip
      else {
        clear_strip();
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

// indicate where book should be placed
void rainbow_drops(int place) {
  for (int i = 0; i < 7; i ++) {
    for (int j = 0; j < places[place][0] - 1; j++) {
      strip.setPixelColor(j, colours[i]);
      //strip.setPixelColor(j-1, 0);
      strip.show();
      delay(25);
    }
    strip.setPixelColor(places[place][0], white);
    strip.setPixelColor(places[place][1], white);
    strip.setPixelColor(places[place][2], white);
  }
}

// shut all leds down
void clear_strip() {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, 0);
    strip.show();
  }
}

