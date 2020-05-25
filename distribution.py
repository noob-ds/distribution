import pandas as pd
from sklearn.cluster import KMeans
from csv import reader
from csv import reader

import sys
import csv

def cluster(df, col):
    clean_data=[]
    for x in df[col]:
        if "UNDISCLOSED" != str(x) and "0" != str(x):
            clean_data.append(x)
    df_clean = pd.DataFrame(clean_data)
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(df_clean)
    centroids = kmeans.cluster_centers_
    centroids_list = []
    for x in centroids:
        centroids_list.append((x[0]))
    centroids_list.sort()
    dic = {}
    group = 1
    for i in centroids_list:
        dic[i] = group
        group = group + 1
    print("cluster centroids:" + str(dic))

    data = []
    for row in df[col]:
        if "UNDISCLOSED" == row:
            data.append([row] + [1])
            continue
        if 0 >= int(row):
            data.append([row] + [0])
            continue
        winner_cent = centroids_list[0]
        dis = abs(int(winner_cent) - int(row))
        for j in centroids_list:
            temp = abs(int(j) - int(row))
            if dis > temp:
                dis = temp
                winner_cent = j
        data.append([row] + [dic[winner_cent]])


    res = pd.DataFrame(data, columns=[col, 'cluster'])
    return res



if __name__ == '__main__':
    input_file_path = sys.argv[1]
    output_path=sys.argv[2]
    df = pd.read_csv(input_file_path, skipinitialspace=True)
    col = list(df.columns.values)
    df_outputs =[]
    for x in col:
        df_res = cluster(df, x)
        df_outputs.append(df_res)
        print("output is stored in" + output_path + str(x) + ".csv")
    result = pd.concat(df_outputs,axis=1, sort=False)
    print(result)
    result.to_csv(output_path, index=False)