import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(10, 10)

plt.imshow(data, cmap='coolwarm', interpolation='nearest')
plt.colorbar()
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        plt.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center', color='white')

plt.xlabel('I/O jobs')
plt.ylabel('bs')
plt.show()
