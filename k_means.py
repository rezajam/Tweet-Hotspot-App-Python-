import numpy.matlib
import numpy as np
import sys
from copy import deepcopy
import matplotlib.pyplot as plt
import scipy
import random
import logging
from random import randint
import csv
import pandas as pd
import math
from scipy.spatial.distance import pdist, squareform


def dist(X, Y):
    distance = ((X[0] - Y[0])**2 + (X[1] - Y[1])**2)**0.5
    return distance

def plot_data(X, centeroids, clusters):
    print("plotting the data")
    colors = ['orange', 'blue', 'green']
    markers = ['D', 'x', 'P']
    for i in range(len(X)):
        plt.scatter(X[i, 0], X[i, 1], marker=markers[int(
            clusters[i])], s=7, color=colors[int(clusters[i])])
    plt.scatter(centeroids[:, 0], centeroids[:, 1], marker='*', c='g', s=150)
    plt.show()

# create the clusters and attribute each point to a cluster
def k_means(X, k=3):
    n = X.shape[0]
    d = X.shape[1]
    max_dist = 0
    max_dist_1 = 0
    max_dist_2 = 0
    distances = np.zeros((n, k))

    logging.basicConfig(level=logging.INFO)
    logging.info('the number of features is: %d', d)
    # manually picking the centeriods
    # new_centers = np.array([[-1.28, -1.9], [3.5, 1.7], [3.34, 6]])
    # new_centers = np.array([[0, 5], [10, 3], [-1.5, 4]])
    # randomly picking the centeroids
    # new_centers = X[np.random.choice(n, 3, replace= False)]
    # picking the furthest distanced centers
    # A = np.random.uniform(np.min(X), np.max(X), size=(1, d))
    A = X[np.random.randint(0, 10)]
    for i in range(n):
        temp = dist(X[i], A)
        if temp > max_dist:
            max_dist = temp
            B = X[i]
    for i in range(n):
        temp1 = dist(X[i], A)
        temp2 = dist(X[i], B)
        if temp1 + temp2 > max_dist_1 + max_dist_2:
            max_dist_1 = temp1
            max_dist_2 = temp2
            C = X[i]
    print("A is:", A)
    print("B is:", B)
    print("C is:", C)
    new_centers = np.array([A, B, C])

    # print("centers is:",new_centers)
    old_centers = np.zeros(new_centers.shape)

    clusters = np.zeros(n)

    error = np.linalg.norm(new_centers - old_centers)
    # print (error)

    for i in range(k):
        # distances = dist(X[i], new_centers)
        distances[:, i] = np.linalg.norm(X - new_centers[i], axis=1)
        clusters = np.argmin(distances, axis=1)
    # plotting of initial clustered data
    # plot_data(X, new_centers, clusters)
    while error != 0:
        for i in range(k):
            # distances = dist(X[i], new_centers)
            distances[:, i] = np.linalg.norm(X - new_centers[i], axis=1)
            clusters = np.argmin(distances, axis=1)

        # clusters[i] = cluster

        old_centers = deepcopy(new_centers)

        for i in range(k):
            # points = [X[j] for j in range(len(X)) if clusters[j] == i]
            # new_centers[i] = np.mean(points, axis=0)
            new_centers[i] = np.mean(X[clusters == i], axis=0)

        error = np.linalg.norm(new_centers - old_centers)

    return clusters, new_centers

def main():
    # load datasets
    df = pd.read_csv("OutputStreaming5.csv")
    coordinates = df[['Long', 'Lat']]

    input_data = coordinates.values

    # compute the clusters and centeriods
    (clusters, new_centers) = k_means(input_data)
    plot_data(input_data, new_centers, clusters)


if __name__ == '__main__':
    main()
