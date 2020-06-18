import numpy as np
import time
tomb = (1,2)

start = time.time()
layer1 = np.array(tomb)
end = time.time()
print("array:",end-start)
print(type(layer1))

start = time.time()
layer2 = np.asarray(tomb)
end = time.time()
print("asarray:",end-start)
print(type(layer2))
