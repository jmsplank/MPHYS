import numpy as np
import matplotlib.pyplot as plt

a = np.array([300, 345, 355, 7, 22, 40])
a = np.radians(a)
mean_a = np.mean(a)

S = 1./len(a) * np.sum(np.sin(a))
C = 1./len(a) * np.sum(np.cos(a))

fig = plt.figure(figsize=[3,3])
ax = plt.subplot(projection='polar')
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')

bad_r = np.sqrt(np.sum(np.power(a,2)))
R = np.sqrt(S**2+C**2)

print(np.degrees(mean_a))
print(360+np.degrees(np.arctan2(S,C)))

ax.scatter(mean_a, 1, c='b')
ax.scatter(np.arctan2(S,C), 1, c='r')
ax.scatter(a, np.ones(len(a)), c='k')

plt.show()
