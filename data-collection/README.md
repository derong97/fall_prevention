# data-collection

There are 2 different kinds of posture positions to be collected:
1. sit
2. stand 

Each script, once executed, will:
1. capture 10 frames in a row 
2. save as a file (e.g. "sit_001.npy") in the corresponding folder sit or stand in the rpi desktop 
3. repeat steps 1 - 2, unless there is a keyboard interrupt
