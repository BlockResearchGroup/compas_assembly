from numpy import asarray
from scipy.spatial import cKDTree


def find_nearest_neighbours(cloud, nmax, dims=3):
    cloud = asarray(cloud)[:, :dims]
    tree = cKDTree(cloud)
    nnbrs = [tree.query(root, nmax) for root in cloud]
    nnbrs = [(d.flatten().tolist(), n.flatten().tolist()) for d, n in nnbrs]
    return nnbrs
