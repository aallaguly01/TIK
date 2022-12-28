import numpy as np
import matplotlib.pyplot as plt

def dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def cluster(k, x_cc, y_cc, x, y):
    clust = []
    for i in range(len(x)):
        r = dist(x[i], y[i], x_cc[0], y_cc[0])
        num = 0
        for j in range(1, k):
            if r > dist(x[i], y[i], x_cc[j], y_cc[j]):
                r = dist(x[i], y[i], x_cc[j], y_cc[j])
                num = j
        clust.append(num)
    return clust

def draw(x, y, clust, x_cc, y_cc):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    for i in range(0, len(x)):
        plt.scatter(x[i], y[i], c=colors[clust[i]])

    plt.scatter(x_cc, y_cc)
    plt.show()

def recalc_centers(x, y, x_cc, y_cc, clust, k):
    for i in range(k):
        n = 0
        for j in clust:
            if j == i:
                n = n + 1
        sum_x = 0
        for j in range(len(clust)):
            if clust[j] == i:
                sum_x = sum_x + x[j]
        sum_y = 0
        for j in range(len(clust)):
            if clust[j] == i:
                sum_y = sum_y + y[j]
        if n != 0:
            x_cc[i] = sum_x / n
            y_cc[i] = sum_y / n
        else:
            x_cc[i] = 0
            y_cc[i] = 0

def k_means(k, x, y):
    n = 100
    x_c = np.mean(x)
    y_c = np.mean(y)

    R = max(dist(x[i], y[i], x_c, y_c) for i in range(n))

    x_cc = [R * np.cos(2 * np.pi * i / k) + x_c for i in range(k)]
    y_cc = [R * np.cos(2 * np.pi * i / k) + y_c for i in range(k)]

    clustIterator = []
    while True:
        clust = cluster(k, x_cc, y_cc, x, y)
        if np.array_equal(clust, clustIterator):
            clustIterator = clust
            break
        else:
            clustIterator = clust
            recalc_centers(x, y, x_cc, y_cc, clust, k)
            draw(x, y, clust, x_cc, y_cc)
    return clustIterator, x_cc, y_cc


def get_by_formula(k, clusters, x_cc, y_cc, x, y):
    j = 0

    for clusterIndex in range(k):
        for i in range(len(x_cc)):
            if clusters[i] == clusterIndex:
                j += dist(x[i], y[i], x_cc[clusterIndex], y_cc[clusterIndex]) ** 2
    return j


def get_optimal(x, y):
    clustIterator, x_cc, y_cc = k_means(1, x, y)
    j_minus_2 = get_by_formula(1, clustIterator, x_cc, y_cc, x, y)

    clustIterator, x_cc, y_cc = k_means(2, x, y)
    j_minus_1 = get_by_formula(2, clustIterator, x_cc, y_cc, x, y)

    for k in range(3, len(x)):
        clustIterator, x_cc, y_cc = k_means(k, x, y)
        j = get_by_formula(k, clustIterator, x_cc, y_cc, x, y)
        if np.abs((j_minus_1 - j) / (j_minus_2 - j_minus_1)) < 0.5:
            k = k - 1
            break
        j_minus_2 = j_minus_1
        j_minus_1 = j
    return k


n = 100
x1 = np.random.randint(1, 100, n)
y2 = np.random.randint(1, 100, n)
optimal = get_optimal(x1, y2)
print('Оптимальное количество: ' + str(optimal))

clustIterator1, x_cc1, y_cc1 = k_means(optimal, x1, y2)
draw(x1, y2, clustIterator1, x_cc1, y_cc1)