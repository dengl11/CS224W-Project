import snap
import pickle as pkl
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
import os


def 

def main():
	with open("../../data/pkl/related_groups.p", "rb") as f:
		related_groups = pkl.load(f)

	with open("../../data/pkl/related_groups_weighted.p", "rb") as f:
		related_groups_weighted = pkl.load(f)

