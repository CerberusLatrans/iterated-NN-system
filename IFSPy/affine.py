import numpy as np
import torch
from ifs_typing import Affine2D, Point2D, PointSet2D

"""
A module for creating, applying, and interpolating between affine transformations.
"""

def apply(
        transform: Affine2D, 
        point: Point2D
        ) -> Point2D:
    """ Applies an affine transformation to a point.

    Args:
        transform (Affine2D): A 2D affine tranformation.
        point (Point2D): A 2D cartesian coordinate.

    Returns:
        Point2D: The resulting post-transformation point.
    """
    point = np.append(point, 1)
    return (transform@point)[:2]

def apply_set(
        transform: Affine2D,
        points: PointSet2D,
        grad: bool = True,
        ) -> PointSet2D:
    """ Applies an affine transformation to a set of points.

    Args:
        transform (Affine2D): A 2D affine tranformation.
        points (PointSet2D): A set of 2D cartesian coordinates.
        grad (bool): Use PyTorch for autograd.

    Returns:
        PointSet2D: The resulting post-transformation set of points.
    """
    if grad:
        points = torch.cat((points.T, torch.ones((1, len(points)))))
        return (transform@points)[:-1].T
    else:
        points = np.append(points, np.full((len(points),1),1), axis=-1)
        return (transform@points.T)[:-1].T

def affine_morph(
        source: Affine2D, 
        target: Affine2D
        ) -> Affine2D:
    """
    Quaternions?
    """
    return np.linalg.solve(source,target)

def affine_interpolate(
        source: Affine2D, 
        target: Affine2D, 
        t: int = 10,
        target_start: float = 0,
        target_end: float = 1,
        ) -> list[Affine2D]:
    """Linearly interpolates between the two transformations with t timeteps.

    Args:
        source (Affine2D): The initial affine transformation.
        target (Affine2D): The final affine transformation.
        t (int, optional): The number of steps between. Defaults to 10.
        target_start (float, optional): The initial weight of the target. Defaults to 0.
        target_end (float, optional): The final weight of the target. Defaults to 1.

    Returns:
        list[Affine2D]: A series of t interpolated transformations from source to target.
    """
    #return [source + (target-source)*i/t for i in range(t)]
    step = abs(target_end - target_start) / (t-1)
    return [affine_weighted_sum([source, target],
                                [1-(target_start+(i*step)),
                                 target_start+(i*step)]) for i in range(t)]

def affine_weighted_sum(
        transforms: list[Affine2D], 
        weights: list[float] = None
        ) -> Affine2D:
    """ Computes the linearly weighted sum of multiple transformations.

    Args:
        transforms (list[Affine2D]): The set of transformations to combine.
        weights (list[float]): Corresponding linear weights for each transformation.

    Returns:
        Affine2D: The resulting linearly weighted affine transformation.
    """
    weights = weights if weights else np.full(len(transforms), 1/len(transforms))
    normalized_weights = weights/np.sum(weights)
    return np.average(transforms, weights=normalized_weights, axis=0)

def affine_norm(
        t: Affine2D, 
        ord: str = None
        ) -> float:
    """Computes the matrix norm of the A component of the transformation.

    Args:
        t (Affine2D): An affine transformation (Ax+b).
        ord (str, optional): Matrix norm order. Defaults to None.

    Returns:
        float: The matrix norm value.
    """
    return np.linalg.norm(t[:-1, :-1], ord=ord)

class Transformations:
    """ A class packaging together elementary affine transformations:
    Translation, reflection, scaling, rotation, shearing.
    Can also be applied to affine transformations to modify them.
    """
    identity_affine: Affine2D = np.identity(3)

    def translate(
            t: Affine2D = identity_affine, 
            shift: tuple[float, float] = (0, 0)
            ) -> Affine2D:
        """Translates a transformation.

        Args:
            t (Affine2D, optional): The affine transformation to translate. Defaults to identity_affine.
            shift (tuple[float, float], optional): The (x,y) values to shift along the axis of. Defaults to (0, 0).

        Returns:
            Affine2D: The translated affine transformation.
        """
        trans_mat = np.array([[1, 0, shift[0]],
                            [0, 1, shift[1]],
                            [0, 0 ,1]])
        return trans_mat@t

    def reflect(
            t: Affine2D = identity_affine,
            axes: tuple[bool, bool] = (False, False)
            ) -> Affine2D:
        """Reflects a transformation.

        Args:
            t (Affine2D, optional): The affine transformation to reflect. Defaults to identity_affine.
            axes (tuple[bool, bool], optional): Whether to reflect across the (y,x) axes. Defaults to (False, False).

        Returns:
            Affine2D: The reflected affine transformation.
        """
        """trans_mat = np.array([[-1 if axes[0] else 1, 0, 0],
                            [0, -1 if axes[1] else 1, 0],
                            [0, 0 ,1]])
        return trans_mat@t"""
        return Transformations.scale(t, factor=(-1 if axes[0] else 1, -1 if axes[1] else 1))

    def scale(
            t: Affine2D = identity_affine,
            factor: tuple[float, float] = (1, 1)
            ) -> Affine2D:
        """Scales a transformation.

        Args:
            t (Affine2D, optional): The affine transformation to scale. Defaults to identity_affine.
            factor (tuple[float, float], optional): Scaling factor along the (x,y) axes. Defaults to (1, 1).

        Returns:
            Affine2D: The scaled affine transformation.
        """
        scale_mat = np.array([[factor[0], 0, 0],
                            [0, factor[1], 0],
                            [0, 0 ,1]])
        return scale_mat@t

    def rotate(
            t: Affine2D = identity_affine,
            degrees: float = 0
            ) -> Affine2D:
        """Rotates a transformation.

        Args:
            t (Affine2D, optional): The affine transformation to rotate. Defaults to identity_affine.
            degrees (float, optional): The degrees to rotate in the counter-clockwise direction. Defaults to 0.

        Returns:
            Affine2D: The rotated affine transformation.
        """
        scale_mat = np.array([[np.cos(degrees), -np.sin(degrees), 0],
                            [np.sin(degrees), np.cos(degrees), 0],
                            [0, 0 ,1]])
        return scale_mat@t

    def shear(
            t: Affine2D = identity_affine,
            factor: tuple[float, float] = (0, 0)
            ) -> Affine2D:
        """Shears a transformation.

        Args:
            t (Affine2D, optional): The affine transformation to shear. Defaults to identity_affine.
            factor (tuple[float, float], optional): Shearing factor in the (x,y) direction. Defaults to (0, 0).

        Returns:
            Affine2D: The sheared affine transformation.
        """
        shear_mat = np.array([[1, factor[0], 0],
                            [factor[1], 1, 0],
                            [0, 0 ,1]])
        return shear_mat@t