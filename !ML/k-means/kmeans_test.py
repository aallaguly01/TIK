import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from kmeans import KMeans

X, y = make_blobs(centers=7, n_samples=500, n_features=2, shuffle=True, random_state=42)

plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()

clusters = input("Enter cluster number:")

print(clusters)

k = KMeans(maxK=int(clusters), max_iters=150, plot_steps=False)
y_pred = k.predict(X)

k.plot()