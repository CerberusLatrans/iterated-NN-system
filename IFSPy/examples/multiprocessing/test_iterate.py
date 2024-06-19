from ifs import iterate
from catalogue.leaves import FERN2D
from markov import weighted_random_chooser, MarkovIterator
from visualize import render_points
import time

if __name__ == '__main__':
    #chooser = weighted_random_chooser(FERN2D)
    chooser = MarkovIterator(FERN2D)
    N = 10_000
    # 100k points single processor faster
    # 1mm points multi processing faster
    start = time.time()
    points = iterate(chooser, N, multi=True)
    end = time.time()
    print(end-start)
    render_points(points, show=True, dim=(200,200))

    """start = time.time()
    points = iterate(chooser, N, multi=False)
    end = time.time()
    print(end-start)
    render_points(points, show=True, dim=(1000,1000))"""

