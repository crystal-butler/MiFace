import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
import os

# Read in lists of scores and labels, converting scores to a distance array and labels to a label array.
def make_arrays(scores_path, labels_path):
    """Read scores and labels in from files. Convert them to ndarrays for clustering."""

