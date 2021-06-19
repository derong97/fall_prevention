
# Calculate the rate of use

INTERVAL int = 60; // in seconds

void setup() {
   bidet_temp_arr int[INTERVAL];
   paper_temp_arr int[INTERVAL];
   idx = 0;
}


void loop() {
   idx = idx % INTERVAL 
   
   bidet_count = 0
   paper_count = 0

   bidet_prev = 0
   paper_prev = 0

   # loop 1 second, fill in value in the right tempArr slot
   start_timer = time.Now()
   while time.Now() - start_timer < 1000:
      if bidet_now > 0 && bidet_prev == 0:
          bidet_count ++
      bidet_prev = bidet_now

      if paper_now > 0 && paper_prev == 0:
          paper_count ++
      paper_prev= paper_now

   bidet_temp_arr[idx] = bidet_count
   paper_temp_arr[idx] = paper_count
   
   idx ++   
}