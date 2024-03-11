import numpy as np
import matplotlib as mpl
from PIL import Image, ImageDraw
from typing import Optional
from tqdm import tqdm
from enum import Enum, auto

from affine import PointSet2D
from ifs import Ifs2D, apply

class ColorScheme(Enum):
    BINARY = auto()
    TIME = auto()
    TRANSFORM = auto()
    TRANSITION = auto()

def normalize(
        points: PointSet2D
        ) -> PointSet2D:
    """
    Normalizes all points to have values in range [0,1]
    """
    p_min = points.min(axis=0)
    p_max = points.max(axis=0)
    return (points-p_min)/(p_max-p_min)

def render_points(
        points: PointSet2D, 
        dim: tuple[int, int] = (200,200), 
        show: bool = False,
        color_scheme: ColorScheme = ColorScheme.BINARY,
        indices: list[int] = None,
        cmap: "Colormap" = mpl.colormaps['viridis']
        ) -> Image.Image:
    normalized: PointSet2D = normalize(points)
    pixels = normalized*np.asarray(dim)
    floored_pixels = np.floor(pixels).astype(int)
    img = np.zeros((*dim,3))
    colors = render_colors(points, color_scheme, indices=indices, cmap=cmap)
    for i,(row,col) in enumerate(flip_vert(floored_pixels, dim[1], to_raster=True)):
        try:
            img[row, col] = colors[i]
        except Exception as e:
            pass
            #print((row, col))
    pil_image = Image.fromarray(img.astype(np.uint8), mode="RGB")
    if show:
        pil_image.show()
    return pil_image

def render_colors(
        points: PointSet2D,
        color_scheme: ColorScheme,
        indices: list[int] = None,
        cmap: "Colormap" = None
    ) -> list[list[int]]:
    if color_scheme==ColorScheme.BINARY:
        return np.full((len(points),3), 255)
    if not cmap:
        raise Exception("Colormap Undefined")
    if color_scheme==ColorScheme.TIME:
        return [np.array(cmap(i/len(points))[:3])*255 for i in range(len(points))]
    if not indices:
        raise Exception("Indices Undefined")
    if color_scheme==ColorScheme.TRANSFORM:
        pcts = np.linspace(0,1,np.max(indices)+1)
        return [np.array([0,0,0])]+[np.array(cmap(pcts[i])[:3])*255 for i in indices]
    if color_scheme==ColorScheme.TRANSITION:
        raise Exception("Not Implemented")
    
def render_gif(
        sequence: list[PointSet2D] | Image.Image,
        show: bool = False,
        fpath: Optional[str] = None,
        duration: int = 5,
        loop: int = 0,
        image_mode: bool = False,
        indices_sequence: list[list[int]] = None,
        **kwargs
        ) -> list[Image.Image]:
    
    if image_mode:
        images = sequence
    else:
        images = []
        for i in tqdm(range(len(sequence)), desc="Rendering..."):
            images.append(render_points(sequence[i], indices=indices_sequence[i], **kwargs))

    if fpath:
        images[0].save(fpath, save_all=True, append_images=images[1:], duration=duration, loop=loop)
        if show:
            gif = Image.open(fpath)
            gif.show()
    
    return images

def render_transforms(
        transforms: Ifs2D, 
        dim: tuple[int, int] = (200,200),
        scale: int = 0.5,
        show: bool = False
        ) -> Image.Image:
    image = Image.new("RGB", dim) 
    draw = ImageDraw.Draw(image)
    scale_factors = [int(dim[0]*scale), int(dim[1]*scale)]
    scaled_width, scaled_height = scale_factors
    unit_sqr = [[0,0],[0,1],[1,1],[1,0]]
    unit_sqr = [np.multiply(pt,scale_factors) for pt in unit_sqr]
    draw.polygon(flip_vert(center(np.array(unit_sqr), dim),dim[1]),fill="red")
    for t in transforms:
        transformed_sqr = [apply(t,x).astype(int) for x in unit_sqr]
        print(transformed_sqr)
        #scaled_sqr = [tuple((pt*scale_factors).astype(int)) for pt in transformed_sqr] 
        #print(scaled_sqr)
        centered_sqr = center(transformed_sqr, dim)
        draw.polygon(flip_vert(centered_sqr, dim[1]))

    if show:
        image.show()
    return image

def center(
        pts: PointSet2D,
        dim: tuple[int, int]
        ) -> PointSet2D:
    return [(pt[0]+int(dim[1]/4), pt[1]+int(dim[0]/4)) for pt in pts]

def flip_vert(
        coords: PointSet2D, 
        height:int, 
        to_raster: bool = False
        ) -> PointSet2D:
    """pixels in (x,y)

    Args:
        pixels (list[tuple[int,int]]): _description_
        height (int): _description_

    Returns:
        list[tuple[int,int]]: _description_
    """
    if to_raster:    
        return [(height-p[1], p[0]) for p in coords]
    return [(p[0], height-p[1],) for p in coords]