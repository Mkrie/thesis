import time
from direct_measurements import DirectMeasurements

start = time.time()
for _ in range(100):
    dir_meas = DirectMeasurements("threemod_2.csv", 0.3)
    meas = dir_meas.direct_measurements_for_profile()
end = time.time()
print((end - start) / 100)
