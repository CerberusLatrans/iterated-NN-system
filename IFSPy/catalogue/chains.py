import numpy as np
from markov import determinant_probabilities

EHRENFEST = np.array([
    [0, 1, 0, 0],
    [1/3, 0, 2/3, 0],
    [0, 2/3, 0, 1/3],
    [0, 0, 1, 0]
])

EHRENFEST2 = np.array([
    [0.01, 0.97, 0.01, 0.01],
    [0.34, 0.01, 0.64, 0.01],
    [0.01, 0.64, 0.01, 0.34],
    [0.01, 0.01, 0.97, 0.01]
])

ABSORBING = np.array([
    [1,0,0,0],
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.25, 0.25]
])
UNIFORM = np.full((4,4), 0.25)

ERG_REG_1 = np.array([[.1, .4, .4, .1],
                     [.2, .4, .3, .1],
                     [.6, 0, .1, .3],
                     [.25, .25, .25, .25]])

ERG_REG_SUM_1 = np.array([[.4,.2,.2,.2],
                         [0,.4,.2,.4],
                         [.2,.4,.2,.2],
                         [.4,0,.4,.2]])

AREA_WEIGHTED = lambda transforms: np.full((n:=len(transforms), n), determinant_probabilities(transforms))

IDENTITY = np.identity

RIGHT_TO_MAIN_MISSING = np.array([[.4,.2,.2,.2],
                         [.2,.2,.2,.4],
                         [.2,.4,.2,.2],
                         [.4,0,.4,.2]])
MAIN_TO_RIGHT_MISSING = np.array([[.4,.2,.2,.2],
                         [.3,.4,.3,0],
                         [.2,.4,.2,.2],
                         [.3,.2,.3,.2]])

MAIN_TO_MAIN_MISSING = np.array([[0, 0.86, 0.07, 0.07],
                                 [0.01, 0.85, 0.07, 0.07],
                                 [0.01, 0.85, 0, 0.14],
                                 [0.01, 0.85, 0.14, 0]])