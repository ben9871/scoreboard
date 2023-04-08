#include <Arduino.h>
#include <stdlib.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  int hit_counter = 0;
  int min_hm = 1;
  int max_hm = random(1,5);
  int play_counter = 0;
  int hitz = 0;
  int tunnel_counter = 0;
  int score = 0;

  for (int i = 0; i < 100000; i++) {
    int hm = min_hm + max_hm;
    play_counter++;

    String data = random(2) == 0 ? "Hit" : "Miss";

    if (data == "Hit") {
      hit_counter++;
      hitz++;
      score++;
    }

    if (hit_counter == hm) {
      data = "Hit & Miss";
      hit_counter = 0;
      score += 3;
      max_hm = random(1,5);
      tunnel_counter++;
    }

    if (play_counter == 15) {
      play_counter = 0;
    }

    Serial.println(data);
    delay(1000); // simulate time between shots
  }
}
