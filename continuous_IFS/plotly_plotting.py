from plotly import graph_objects as go
import numpy as np

def plot_ifs_2d(points):
    points = np.transpose(points)
    fig = go.Figure(data=go.Scatter(
        x=points[0],
        y=points[1],
        mode="markers",
        marker_color = "black",
        marker_size = 2,
    ))

    fig.show()

def plot_ifs_2d_widget(generator):
    fig = go.FigureWidget()
    
    xs = []
    ys = []
    for x in generator:
        xs.append(x[0])
        ys.append(x[1])
        fig.data = [go.Scatter(
        x=xs,
        y=ys,
        mode="lines+markers",
        marker_color = "black",
        marker_size = 2,
    )]

def plot_ifs_2d_slider(generator):
    fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
    }

    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": False}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None]],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "up",
            "showactive": True,
            "type": "buttons",
            "x": 1,
            "xanchor": "right",
            "y": 1,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Year:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    # make data
    x0 = next(generator)
    data_dict = {
            "x": [x0[0]],
            "y": [x0[1]],
            "mode": "markers",
            "marker_color": "black",
            "marker_size": 10,
        }
    fig_dict["data"].append(data_dict)
    print(fig_dict["data"])

    # make frames
    frame = {"data": [], "name": ""}
    for i,x in enumerate(generator):
        
        data_dict = {
                "x": [x[0]],
                "y": [x[1]],
                "mode": "lines+markers",
                "marker_color": "black",
                "marker_size": 10,
            }
        frame["data"].append(data_dict)
        print(frame["data"][-1])
        frame["name"] = "Iteration: {}".format(i)
        fig_dict["frames"].append(frame)


    #fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)
    print("CHECK")

    fig.show()
    #fig.write_html('fig.html', auto_open=True)

def plot_ifs_3d(generator):
    points = [x for x in generator]
    #points = np.fromiter(generator, np.dtype((float, 2)))
    points = np.transpose(points)
    fig = go.Figure(data=go.Scatter3d(
        x=points[0],
        y=points[1],
        z=points[2],
        mode="markers",
        marker_color = "black",
        marker_size = 2,
    ))
    fig.show()