import plotly.graph_objects as go
import numpy as np
from PIL import Image

def get_probabilities(transforms, dim=3):
    if not isinstance(transforms, np.ndarray):
        transforms = transforms.detach().numpy()
    sum = 0
    dets = []
    for t in transforms:
        A = t[:-dim].reshape(dim, dim)
        det = np.abs(np.linalg.det(A))
        sum += det
        dets.append(det)
    
    probs = np.array(dets) / sum
    return probs

def rand_generate(transforms, weights=None, max_iter=1000, dim=3):
    if not isinstance(transforms, np.ndarray):
        transforms = transforms.detach().numpy()   
    #initialize at origin
    x = np.full(dim, 0)
    def ifs(pt):
        t = transforms[np.random.choice(len(transforms), p=weights)]
        A = t[:-dim].reshape(dim, dim)
        b = t[-dim:]
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

def plot_2d(points):
    if not isinstance(points, np.ndarray):
        points = points.detach().numpy()
    points = np.transpose(points)
    fig = go.Figure(data=go.Scatter(
        x=points[0],
        y=points[1],
        mode="markers",
        marker_color = "black",
        marker_size = 2,
    ))
    return fig

def plot_2d_pil(points, dim: tuple[int, int]) -> Image:
    print(points.shape)
    [xs, ys] = np.transpose(points)
    xs = (xs - xs.min()) / (xs.max() - xs.min())
    ys = (ys - ys.min()) / (ys.max() - ys.min())
    regularized_points = np.transpose([xs*dim[0], ys*dim[1]])
    print(regularized_points[:5])
    floored = np.floor(regularized_points).astype(int)

    img = np.zeros(dim)
    for pt in floored:
        try:
            img[dim[1]-pt[1], pt[0]] = 255
        except:
            print(pt)

    pil_image = Image.fromarray(img)
    pil_image.show()
    return pil_image