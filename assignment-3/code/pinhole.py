
# code for "Pinhole camera model"
# see utils for read_landmarks function and more general functions

import numpy as np
import torch

import utils


def get_xyz1(G):
    # add ones to coordinates
    return torch.cat((G, torch.ones((np.size(G, 0), 1))), 1).T


def xyzd2xyz(xyzd):
    # divide by d and reshape
    xyz = (xyzd / xyzd[3, :])[:3, :].T
    return xyz


def transform(G, rotation, translation):
    # only transform G
    xyz1 = get_xyz1(G)
    T = get_T(rotation, translation)
    xyzd = T @ xyz1
    xyz = xyzd2xyz(xyzd)
    return xyz


def get_R(angles_deg):
    # Rotation matrix
    # Input: list containing x,y,z Euler angles (degrees)
    angles_rad = utils.deg2rad(angles_deg)
    sin = torch.sin(angles_rad).view(-1, 1, 1)
    cos = torch.cos(angles_rad).view(-1, 1, 1)
    # ! using the following three lines will cause grads to disappear
    # Rx = torch.tensor([[1, 0, 0],  [0, cos[0], -sin[0]],  [0, sin[0], cos[0]]])
    # Ry = torch.tensor([[cos[1], 0, sin[1]],  [0, 1, 0],  [-sin[1], 0, cos[1]]])
    # Rz = torch.tensor([[cos[2], -sin[2], 0],  [sin[2], cos[2], 0],  [0, 0, 1]])
    Rx = torch.cat((torch.tensor([[1., 0., 0.]]),
                    torch.cat((torch.zeros(1, 1), cos[0], -sin[0]), 1),
                    torch.cat((torch.zeros(1, 1), sin[0], cos[0]), 1)))
    Ry = torch.cat((torch.cat((cos[1], torch.zeros(1, 1), sin[1]), 1),
                    torch.tensor([[0., 1., 0.]]),
                    torch.cat((-sin[1], torch.zeros(1, 1), cos[1]), 1)))
    Rz = torch.cat((torch.cat((cos[2], -sin[2], torch.zeros(1, 1)), 1),
                    torch.cat((sin[2], cos[2], torch.zeros(1, 1)), 1),
                    torch.tensor([[0., 0., 1.]])))
    return Rz @ Ry @ Rx


def get_T(angles_deg, t):
    # Transformation matrix
    # Input: lists containing x,y,z Euler angles (degrees), and translation values
    R = get_R(angles_deg)
    Rt = torch.cat((R, t.view(3, 1)), 1)
    return torch.cat((Rt, torch.tensor([[0, 0, 0, 1.]])))


def get_P(FOV=40, n=10., f=1000., aspect_ratio=4/3.):
    # Perspective projection matrix
    # assume symmetrical view volume
    t = torch.tan(torch.tensor([utils.deg2rad(FOV/2)])) * n
    r = t * aspect_ratio
    return torch.tensor([[n/r,  0,    0,            0],
                         [0,    n/t,  0,            0],
                         [0,    0,    -(f+n)/(f-n), -2*f*n/(f-n)],
                         [0,    0,    -1,           0]])


def get_V(h=480., w=640.):
    # simplified matrix, assuming:
    # vl = 0, vr = width, vb = 0, vt = height
    return torch.tensor([[w/2,  0,    0,     w/2],
                         [0,    h/2,  0,     h/2],
                         [0,    0,    1/2.,  1/2.],
                         [0,    0,    0,     1]])


def camera_model(G, rotation, translation, h=480., w=640., FOV=40, n=10., f=1000.):
    # this function combines all matrices to get to a 2d projection of the 3d object
    T = get_T(rotation, translation)
    P = get_P(FOV=FOV, n=n, f=f, aspect_ratio=w/h)
    V = get_V(h=h, w=w)
    xyz1 = get_xyz1(G)
    xyzd = V @ P @ T @ xyz1
    xyz = xyzd2xyz(xyzd)
    return xyz
