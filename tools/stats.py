import numpy as np
import random

def permute_correlation_mtx(matrix):

    if matrix.shape[0] != matrix.shape[1]:
        raise NotImplementedError("Matrix is not square.")

    nVals = matrix.shape[0]

    indices = [i for i in range(nVals)]
    random.shuffle(indices)

    new_mtx = np.zeros((nVals, nVals))

    for i in range(nVals):
        for j in range(nVals):
            new_mtx[i, j] = matrix[indices[i], indices[j]]

    assert np.isclose(np.sum(matrix), np.sum(new_mtx))

    return new_mtx

def calc_diff_norm(mtx1, mtx2):
    return np.linalg.norm(mtx1 - mtx2)

def calc_avg_permuted_norm(sound_mtx, color_mtx, nReps):
    assert sound_mtx.shape == color_mtx.shape

    norms = []
    for _ in range(nReps):
        sound_mtx_permuted = permute_correlation_mtx(sound_mtx)
        norm = calc_diff_norm(sound_mtx_permuted, color_mtx)
        norms.append(norm)

    avg_norm = sum(norms) / len(norms)
    return avg_norm


def hopkins(dist_mtx):
    pass