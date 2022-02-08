import real_time_tools as rt
import time

freq = 1000 # Hz
spinner = rt.FrequencyManager(freq)

while(True):
    print("Spinning: ", spinner.wait())
    # time.sleep(1/freq*1.1)
