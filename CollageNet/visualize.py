import plotly.graph_objects as go
import numpy as np

def get_probabilities(transforms):
    if not isinstance(transforms, np.ndarray):
        transforms = transforms.detach().numpy()
    sum = 0
    dets = []
    for t in transforms:
        A = np.array([t[0:3], t[3:6], t[6:9]])
        det = np.abs(np.linalg.det(A))
        sum += det
        dets.append(det)
    
    probs = np.array(dets) / sum
    return probs

def rand_generate(transforms, weights=None, max_iter=1000, x0=np.array([0, 0, 0])):
    if not isinstance(transforms, np.ndarray):
        transforms = transforms.detach().numpy()
    x = x0
    def ifs(pt):
        t = transforms[np.random.choice(len(transforms), p=weights)]
        A = np.array([t[0:3], t[3:6], t[6:9]])
        b = np.array(t[9:12])
        nonlocal x
        x = A@pt + b
        return pt

    return np.array([ifs(x) for _ in range(max_iter)])
    
def plot_3d(points):
    if not isinstance(points, np.ndarray):
        points = points.detach().numpy()
    points = np.transpose(points)
    fig = go.Figure(data=go.Scatter3d(
        x=points[0],
        y=points[1],
        z=points[2],
        mode="markers",
        marker_color = "black",
        marker_size = 2,
    ))
    return fig