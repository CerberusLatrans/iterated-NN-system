import numpy as np
from PIL import Image, ImageDraw
from affine import Point2D, PointSet2D, Affine2D
from ifs import apply, ifs_interpolate
from typing import Optional

def normalize(points: Point2D) -> Point2D:
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
    for px in floored_pixels:
        try:
            img[dim[1]-px[1], px[0]] = 255
        except:
            print(px)
    pil_image = Image.fromarray(img)
    if show:
        pil_image.show()
    return pil_image

def render_points_sequence(
        sequence: list[PointSet2D],
        dim: tuple[int, int] = (200,200),
        show: bool = False,
        fpath: Optional[str] = None,
        duration: int = 5,
        loop: int = 0) -> list[Image.Image]:
    images = [render_points(pt_set, dim=dim) for pt_set in sequence]

    if fpath:
        images[0].save(fpath, save_all=True, append_images=images[1:], duration=duration, loop=loop)
        if show:
            gif = Image.open(fpath)
            gif.show()
    
    return images

def render_transforms(
        transforms: list[Affine2D], 
        dim: tuple[int, int] = (200,200),
        show: bool = False) -> Image.Image:
    points = []
    image = Image.new("RGB", dim) 
    draw = ImageDraw.Draw(image)
    unit_sqr = np.array([[0,0],[0,dim[1]],[dim[0],dim[1]],[dim[0],0]])
    draw.polygon(unit_sqr,fill="red")
    transformed_sqrs = []
    for t in transforms:
        transformed_sqr = [apply(t,x).astype(int) for x in unit_sqr]
        points.extend(transformed_sqr)
        transformed_sqrs.append(transformed_sqr)
        draw.polygon(transformed_sqr)

    if show:
        image.show()
    return image