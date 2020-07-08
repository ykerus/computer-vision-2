
# code for "Texturing"
# see utils for more general functions

import numpy as np

import utils


def interpolate(img, u, v):
    # use bilinear interpolation to determine the color for given uv coords
    ufloor, uceil = int(u.floor()), int((u+1.).floor())  # u.ceil() sometimes causes black patches in final result
    vfloor, vceil = int(v.floor()), int((v+1.).floor())

    tl = img[vfloor, ufloor, :]
    tr = img[vfloor, uceil, :]
    bl = img[vceil, ufloor, :]
    br = img[vceil, uceil, :]

    t_interp = (uceil - u) * tl + (u - ufloor) * tr
    b_interp = (uceil - u) * bl + (u - ufloor) * br
    c_interp = (vceil - v) * t_interp + (v - vfloor) * b_interp

    return c_interp / 255.


def get_color(img, uv):
    # iterate over uv coords and find corresponding colors
    h, w, _ = np.shape(img)
    uv = utils.flip_ycoords(uv, H=h)
    color = np.zeros((uv.size(0), 3))
    for i, (u, v) in enumerate(uv):
        color[i] = interpolate(img, u, v)
    return color


