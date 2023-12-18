import numpy as np
from PIL import Image, ImageDraw
from typing import Optional
from tqdm import tqdm

from affine import Point2D, PointSet2D
from ifs import Ifs2D, apply


def normalize(
        points: Point2D
        ) -> Point2D:
    """
    Normalizes all points to have values in range [0,1]
    """
    p_min = points.min(axis=0)
    p_max = points.max(axis=0)
    return (points-p_min)/(p_max-p_min)

def render_points(
        points: PointSet2D, 
        dim: tuple[int, int] = (200,200), 
        show: bool = False
        ) -> Image.Image:
    normalized: Point2D = normalize(points)
    pixels = normalized*np.asarray(dim)
    floored_pixels = np.floor(pixels).astype(int)
    img = np.zeros(dim)
    for row,col in flip_vert(floored_pixels, dim[1], to_raster=True):
        try:
            img[row, col] = 255
        except:
            pass
            #print((row, col))
    pil_image = Image.fromarray(img)
    if show:
        pil_image.show()
    return pil_image

def render_gif(
        sequence: list[PointSet2D] | Image.Image,
        dim: tuple[int, int] = (200,200),
        show: bool = False,
        fpath: Optional[str] = None,
        duration: int = 5,
        loop: int = 0,
        image_mode: bool = False
        ) -> list[Image.Image]:
    
    if image_mode:
        images = sequence
    else:
        images = []
        for i in tqdm(range(len(sequence)), desc="Rendering..."):
            images.append(render_points(sequence[i], dim=dim))

    if fpath:
        images[0].save(fpath, save_all=True, append_images=images[1:], duration=duration, loop=loop)
        if show:
            gif = Image.open(fpath)
            gif.show()
    
    return images

def render_transforms(
        transforms: Ifs2D, 
        dim: tuple[int, int] = (200,200),
        show: bool = False
        ) -> Image.Image:
    image = Image.new("RGB", dim) 
    draw = ImageDraw.Draw(image)
    half_width, half_height = int(dim[0]/2), int(dim[1]/2)
    unit_sqr = [[0,0],[0,half_width],[half_height,half_width],[half_height,0]]
    draw.polygon(flip_vert(center(unit_sqr, dim),dim[1]),fill="red")
    for t in transforms:
        transformed_sqr = [tuple(apply(t,x).astype(int)) for x in unit_sqr]
        print(transformed_sqr)
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