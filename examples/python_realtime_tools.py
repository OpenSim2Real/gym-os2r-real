import real_time_tools as rt

freq = .1 # Hz
spinner = rt.FrequencyManager(freq)

while(True):
    print("Spinning \n")
    spinner.wait()
