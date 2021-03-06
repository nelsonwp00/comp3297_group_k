import numpy as np
from sklearn.cluster import DBSCAN
import math

#clustering functions
def custom_metric(q, p, space_eps, time_eps, extraData):
    dist = 0
    for i in range(2):
        dist += (q[i] - p[i])**2
    spatial_dist = math.sqrt(dist)

    time_dist = math.sqrt((q[2]-p[2])**2)

    if time_dist/time_eps <= 1 and spatial_dist/space_eps <= 1 and extraData[int(p[3])][0] != extraData[int(q[3])][0]:
        return 1
    else:
        return 2


def doClustering(vector_4d, distance, time, minimum_cluster, extraData):

    params = {"space_eps": distance, "time_eps": time, "extraData": extraData}
    db = DBSCAN(eps=1, min_samples=minimum_cluster-1, metric=custom_metric, metric_params=params).fit_predict(vector_4d)

    unique_labels = set(db)
    total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) -1

    result=[]

    #print("Total clusters:", total_clusters)

    total_noise = list(db).count(-1)

    #print("Total un-clustered:", total_noise)

    for k in unique_labels:
        if k != -1:

            labels_k = db == k
            cluster_k = vector_4d[labels_k]
            row=[]

            #print("Cluster", k, " size:", len(cluster_k))

            for pt in cluster_k:
                row.append({'x':pt[0], 'y':pt[1], 'date':extraData[int(pt[3])][2], 'caseNo':extraData[int(pt[3])][0], 'location':extraData[int(pt[3])][1]})

            result.append(row)

    return result


# 5. manipulate the cluster function to print give the exact output the tasksheet requires.

