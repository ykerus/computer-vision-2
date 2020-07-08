
# this file contains the more general functions (read-file functions, visualizations, etc.)

import os
import torch
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from supplemental_code import *


def deg2rad(angle):
    # converts degrees to radians
    return angle * np.pi / 180.


def build_structure(dirs):
    # build file structure
    for d in dirs:
        subs = d.split("/")[1:-1]
        for i, sub in enumerate(subs):
            if i == 0:
                path = "../" + sub
            else:
                path += "/" + sub
            if not os.path.exists(path):
                os.mkdir(path)


def read_bfm(bfm, id_comps=30, exp_comps=20):
    # Select weights from BFM and resize/reshape
    mu_id = torch.from_numpy(np.reshape(np.asarray(bfm["shape/model/mean"], dtype=np.float32), (-1, 3)))
    mu_exp = torch.from_numpy(np.reshape(np.asarray(bfm["expression/model/mean"], dtype=np.float32), (-1, 3)))
    E_id = torch.from_numpy(np.reshape(np.asarray(bfm["shape/model/pcaBasis"], dtype=np.float32)[:, :id_comps], (-1, 3, id_comps)))
    E_exp = torch.from_numpy(np.reshape(np.asarray(bfm["expression/model/pcaBasis"], dtype=np.float32)[:, :exp_comps], (-1, 3, exp_comps)))
    sig_id = torch.from_numpy(np.sqrt(np.asarray(bfm["shape/model/pcaVariance"], dtype=np.float32))[:id_comps])
    sig_exp = torch.from_numpy(np.sqrt(np.asarray(bfm["expression/model/pcaVariance"], dtype=np.float32))[:exp_comps])
    color = np.reshape(np.asarray(bfm["color/model/mean"], dtype=np.float32), (-1, 3))
    triangles = np.asarray(bfm["shape/representer/cells"], dtype=np.float32).T
    return (mu_id, mu_exp, E_id, E_exp, sig_id, sig_exp), color, triangles


def read_landmarks(fname):
    # read landmark indices
    with open(fname, "r") as f:
        lms = [int(lm[:-1]) if "\n" in lm else int(lm) for lm in f]
    return lms


def get_landmarks(uv, lm_annotations):
    # select landmark vertices
    return uv[lm_annotations, :]


def get_image(xyz, color, triangles, h=480, w=640):
    # render image after pinhole model
    xyz = np.array(xyz)
    return np.uint8(render(xyz, color, triangles, H=h, W=w) * 255)


def show_face(img, white_background=True):
    # show image
    if white_background:
        img[img == 0] = 255
    plt.imshow(img)


def show_landmarks(shape, indices=True, label=""):
    # scatter landmarks
    plt.scatter(shape[:, 0], shape[:, 1], s=5, label=label)
    if indices:
        for i in range(len(shape[:, 0])):
            plt.text(shape[i, 0], shape[i, 1], str(i), fontsize=4)
    plt.legend()


def read_image(fname):
    # read image from file
    return np.asarray(Image.open(fname))[:, :, :3]


def flip_y():
    # flip image y axis
    plt.gca().invert_yaxis()


def flip_ycoords(coords, H=480):
    # given a height, flip y coords over half that height
    flipped = torch.zeros(coords.size())
    for i, coord in enumerate(coords):
        flipped[i] = torch.tensor([coord[0]*2, H]) - coord
    return flipped


def save_loss(loss, title="Loss", save_fname="loss.pdf", loss_path="../losses/"):
    # save loss plot
    plt.title(title)
    plt.plot(loss)
    plt.xlabel("Step", fontsize=12)
    plt.ylabel("Loss")
    plt.savefig(loss_path + save_fname)
    plt.close()


def clean_folders(folders):
    # remove all files in given folders
    for folder in folders:
        for fname in os.listdir(folder):
            os.remove(folder + fname)


def print_stats(alpha, delta, rotation, translation):
    # print latent parameters stats
    print(
        "    alpha: mean = {:<4.2}, std = {:<4.2}, min = {:<4.2}, max = {:<4.2}".format(torch.mean(alpha), torch.std(alpha),
                                                                                    torch.min(alpha), torch.max(alpha)))
    print(
        "    delta: mean = {:<4.2}, std = {:<4.2}, min = {:<4.2}, max = {:<4.2}".format(torch.mean(delta), torch.std(delta),
                                                                                    torch.min(delta), torch.max(delta)))
    print(f"    rotation: {' '.join(['{:<5.4}'.format(r.item()) for r in rotation])}")
    print(f"    translation: {' '.join(['{:<5.4}'.format(t.item()) for t in translation])}")

