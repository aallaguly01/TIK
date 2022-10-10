import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1-x2)**2))

class KMeans:

    def __init__(self, maxK=10, max_iters=100, plot_steps=False):
        self.maxK = maxK
        self.max_iters = max_iters
        self.plot_steps = plot_steps

    
        # mean feature vector for each cluster
        self.centroids = []

    def predict(self, X):
        self.X = X
        self.n_samples, self.n_features = X.shape

        self.D = []

        for K in range(1, self.maxK):
            # list of sample indices for each cluster
            self.clusters = [[] for _ in range(K)]

            #initialize centroids
            random_sample_idxs = np.random.choice(self.n_samples, K, replace=False)
            self.centroids = [self.X[idxs] for idxs in random_sample_idxs]

            # optimization
            for _ in range(self.max_iters):
                # update clusters
                self.clusters = self._create_clusters(self.centroids, K)
            
                # update centroids
                centroids_old = self.centroids
                self.centroids = self._get_centroids(self.clusters, K)

                # check if converged
                if self._is_converged(centroids_old, self.centroids, K):
                    self.plot()
                    self.D.append(self.get_J(K))
                    break

            
            

        return self._get_cluster_labels(self.clusters)
        
    def _get_cluster_labels(self, clusters):
        labels = np.empty(self.n_samples)
        for cluster_idx, cluster in enumerate(clusters):
            for sample_idx in cluster:
                labels[sample_idx] = cluster_idx
        return labels


    def _create_clusters(self, centroids, K):
        clusters = [[] for _ in range(K)]
        for idx, sample in enumerate(self.X):
            centroid_idx = self._closest_centroid(sample, centroids)
            clusters[centroid_idx].append(idx)
        return clusters
    
    def _closest_centroid(self, sample, centroids):
        distances = [euclidean_distance(sample, point) for point in centroids]
        closest_idx = np.argmin(distances)
        return closest_idx

    def _get_centroids(self, clusters, K):
        centroids = np.zeros((K, self.n_features))
        for cluster_idx, cluster in enumerate(clusters):
            cluster_mean = np.mean(self.X[cluster], axis=0)
            centroids[cluster_idx] = cluster_mean
        return centroids

    def _is_converged(self, centroids_old, centroids, K):
        distances = [euclidean_distance(centroids_old[i], centroids[i]) for i in range(K)]
        return sum(distances) == 0

    def plot(self):
        fig, ax = plt.subplots(figsize=(12, 8))

        for i, index in enumerate(self.clusters):
            point = self.X[index].T
            ax.scatter(*point)

        for point in self.centroids:
            ax.scatter(*point, marker="x", color="black", linewidth=2)

        plt.show()



    def get_J(self, j):
        sum = 0

        for i in range(j):
            for j in range(len(self.clusters[i])):
                sum += np.sqrt((self.X[self.clusters[i]][j][0] - self.centroids[i][0]) **2 + (self.X[self.clusters[i]][j][0] - self.centroids[i][1])**2)
        return sum

    def get_D(self, array):
        res = []
        for i in range(1, len(array) - 1):
            res.append(np.abs(array[i] - array[i+1]) / np.abs(array[i-1] - array[i]))

        for i in range(res):
            if res[i] == np.min(res):
                return i
        

