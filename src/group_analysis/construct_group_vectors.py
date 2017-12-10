################################################
# Construct Group Vectors
################################################ 
from __future__ import division
import sys
sys.path.append("../lib")
sys.path.append("..")
from util.plotter import *
from util import num_ops 
from GTD_Config import *
from collections import defaultdict 
from itertools import combinations
import pandas as pd
from plotly.graph_objs import *
import plotly.plotly as py
import numpy as np
from numpy import sign 
from tabulate import tabulate 
import pickle 
from dataframe_preprocessor import DataframePreprocessor


features = ["lethality", "peak_year", "attack_type", "target_type", "weapon_type", "h2a", "log", "lat"]

top_k = 100
if top_k == 10:
    fig_path = "../../out/fig/group_similarity.png"
    sim_pkl = "../../out/data/similarity.pkl" 
else:
    fig_path = "../../out/fig/group_similarity_100.png"
    sim_pkl = "../../out/data/similarity_{}.pkl".format(top_k) 

with open("../../out/data/attack_type.pkl", "rb") as f:
    attack_dict = pickle.load(f, encoding="latin1")

with open("../../out/data/h2a.pkl", "rb") as f:
    h2a_dict = pickle.load(f, encoding="latin1")

with open("../../out/data/peak_year.pkl", "rb") as f:
    year_dict = pickle.load(f, encoding="latin1")

with open("../../out/data/target_type.pkl", "rb") as f:
    target_dict = pickle.load(f, encoding="latin1")

with open("../../out/data/weapon_type.pkl", "rb") as f:
    weapon_dict = pickle.load(f, encoding="latin1")

with open("../../out/data/top_lethality_group.pkl", "rb") as f:
    lethality_arr = pickle.load(f, encoding="latin1")
    lethality_arr = lethality_arr[:top_k]

with open("../../out/data/geo_location.pkl", "rb") as f:
    location_dic = pickle.load(f, encoding="latin1")

group_vectors = {} # {gname: [...]}
n_group = len(lethality_arr)

for v in lethality_arr:
    name = v[0]
    lethality = v[-1]
    attack_type = attack_dict[name]
    target_type = target_dict[name]
    weapon_type = weapon_dict[name]
    h2a = h2a_dict[name][-1]
    year = year_dict[name]
    lotlat = location_dic[name] 
    log = lotlat[0]
    lat = lotlat[1]
    group_vectors[name] = [lethality, year, attack_type, target_type, weapon_type, h2a, log, lat]

if top_k == 10:
    group_names = ['Al-Qaida', 'Al-Shabaab', 'Tehrik-i-Taliban Pakistan (TTP)', 'Taliban', 'Al-Qaida in Iraq','Boko Haram',  'Liberation Tigers of Tamil Eelam (LTTE)', 'Shining Path (SL)','Islamic State of Iraq and the Levant (ISIL)',  'Farabundo Marti National Liberation Front (FMLN)']
else:
    group_names = [x[0] for x in lethality_arr]

def group_similarity(v1, v2):
    """return similarity score of two groups
    Args:
        v1: 
        v2: 

    Return: 
    """
    v1, v2 = np.array(v1), np.array(v2)

    score = 0
    i = 0
    # lethality 
    score += min(v1[0], v2[0])/max(v1[0], v2[0])
    i += 1

    # year  
    score += np.exp(-abs(v1[1] - v2[1]))
    i += 1

    # attack type 
    score += v1[2] == v2[2]
    i += 1

    # target type 
    score += v1[i] == v2[i]
    i += 1

    # weapon type 
    score += v1[i] == v2[i]
    i += 1

    # h2a 
    score += min(v1[i], v2[i])/max(v1[i], v2[i])

    # geo distance
    dis = np.linalg.norm(v1[-2:] - v2[-2:])
    score += np.exp(-dis)

    return score 
   

similarity_matrix = np.zeros((n_group, n_group))
for i, v in enumerate(group_names):
    v1 = group_vectors[v]
    for j in range(i, n_group):
        v2 = group_vectors[group_names[j]]
        similarity_matrix[i][j] = group_similarity(v1, v2)

similarity_matrix = similarity_matrix + similarity_matrix.T - np.diag(np.diag(similarity_matrix))
print(np.min(similarity_matrix))
print(np.max(similarity_matrix))

simple_group_names = simplity_gnames(group_names)

sns_heatmap(similarity_matrix, 
            title = "Group Similarity Matrix",
            xtick_rot = 45,
            ytick_rot = 45,
            xticklabels=simple_group_names, 
            yticklabels=simple_group_names, 
            save_path = fig_path)

# save group vectors 
with open("../../out/data/group_vectors.pkl", "wb") as f:
    pickle.dump(group_vectors, f)

# save similarity_matrix 
with open(sim_pkl, "wb") as f:
    dic = {"group": group_names, "matrix": similarity_matrix}
    pickle.dump(dic, f)
