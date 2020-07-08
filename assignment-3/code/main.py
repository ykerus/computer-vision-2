import h5py
import sys
import torch
import numpy as np
import matplotlib.pyplot as plt

import morph
import pinhole
import latent
import texture
import multiple
import utils
from supplemental_code import *


# start with ".." and end with "/"
MODELS_PATH = "../models/"
OBJ_2D_PATH = "../obj/2d/"
OBJ_3D_PATH = "../obj/3d/"
PINHOLE_PATH = "../2d/"
IMAGE_PATH = "../images/"
LOSS_PATH = "../losses/"

BFM_FNAME = "model2017-1_face12_nomouth.h5"
LM_FNAME = "Landmarks68_model2017-1_face12_nomouth.anl"


def morph_demo(save_fname="morph", idx=0):
    # assignment: section 2
    bfm = h5py.File(MODELS_PATH + BFM_FNAME, "r")
    bfm_params, color, triangles = utils.read_bfm(bfm)

    G = morph.compute_G(bfm_params)

    save_obj(OBJ_3D_PATH + save_fname + str(idx) + ".obj", G, color, triangles)


def pinhole_demo(rotation=None, translation=None, save_fname="pinhole", idx=0):
    # assignment: section 3
    bfm = h5py.File(MODELS_PATH + BFM_FNAME, "r")
    bfm_params, color, triangles = utils.read_bfm(bfm)
    lms = utils.read_landmarks(MODELS_PATH + LM_FNAME)  # landmark annotations

    rotation = torch.tensor([0., 0., 0.]) if rotation is None else torch.tensor(rotation)
    translation = torch.tensor([0., 0., -500.]) if translation is None else torch.tensor(translation)

    G = morph.compute_G(bfm_params)
    G_transformed = pinhole.transform(G, rotation, translation)
    G_pinhole = pinhole.camera_model(G, rotation, translation)

    save_obj(OBJ_3D_PATH + save_fname + str(idx) + "_3d.obj", G_transformed, color, triangles)
    save_obj(OBJ_2D_PATH + save_fname + str(idx) + "_2d.obj", G_pinhole, color, triangles)

    print("Rendering...")
    img_2d = utils.get_image(G_pinhole, color, triangles)  # render img
    img_lm = utils.get_landmarks(G_pinhole[:, :2], lms)  # landmark coords

    utils.show_face(img_2d)
    utils.flip_y()
    plt.savefig(PINHOLE_PATH + save_fname + str(idx) + ".pdf")

    utils.show_landmarks(img_lm, indices=True)  # overlays landmarks on image
    plt.savefig(PINHOLE_PATH + save_fname + str(idx) + "_lm.pdf")
    plt.close()


def latent_demo(load_fname="yke_neutral.jpeg", save_fname="latent", reg_a=10., reg_d=10., idx=0):
    # assignment: section 4
    bfm = h5py.File(MODELS_PATH + BFM_FNAME, "r")
    bfm_params, color, triangles = utils.read_bfm(bfm)
    lms = utils.read_landmarks(MODELS_PATH + LM_FNAME)  # landmark annotations

    img_real = utils.read_image(IMAGE_PATH + load_fname)  # load image of face we want to reconstruct
    h, w, _ = np.shape(img_real)
    lm_real = torch.from_numpy(detect_landmark(img_real))  # detect ground-truth landmarks
    lm_real_flip = utils.flip_ycoords(lm_real, H=h)  # flip y axis because img is upside down compared to pinhole output

    alpha, delta, rotation, translation, loss = latent.estimate_params((bfm_params, color, triangles),
                                                                       lms, lm_real_flip, h=h, w=w,
                                                                       reg_a=reg_a, reg_d=reg_d)
    utils.print_stats(alpha, delta, rotation, translation)  # latent params statistics

    utils.save_loss(loss, save_fname=save_fname + str(idx) + "_loss.pdf")

    G = morph.compute_G(bfm_params, alpha=alpha, delta=delta)
    G_pinhole = pinhole.camera_model(G, rotation, translation, h=h, w=w)

    save_obj(OBJ_3D_PATH + save_fname + str(idx) + "_3d.obj", G, color, triangles)
    save_obj(OBJ_2D_PATH + save_fname + str(idx) + "_2d.obj", G_pinhole, color, triangles)

    lm_pred_flip = utils.get_landmarks(G_pinhole[:, :2], lms)
    lm_pred = utils.flip_ycoords(lm_pred_flip, H=h)  # flip y back to match with image

    utils.show_face(img_real, white_background=False)
    utils.show_landmarks(lm_real, indices=False, label="ground-truth")
    try:
        utils.show_landmarks(lm_pred, indices=False, label="model")
    except TypeError:
        print("... unable to show predicted landmarks")
    plt.savefig(PINHOLE_PATH + save_fname + str(idx)  + "_lm.pdf")
    plt.close()

    utils.show_face(img_real, white_background=False)
    utils.show_landmarks(lm_real, indices=True, label="ground-truth")
    try:
        utils.show_landmarks(lm_pred, indices=True, label="model")
    except TypeError:
        print("... unable to show predicted landmarks")
    plt.savefig(PINHOLE_PATH + save_fname + str(idx) + "_lm_ind.pdf")
    plt.close()


def texture_demo(load_fname="yke_neutral.jpeg", save_fname="texture", reg_a=10., reg_d=10., idx=0):
    # assignment: section 5
    bfm = h5py.File(MODELS_PATH + BFM_FNAME, "r")
    bfm_params, color, triangles = utils.read_bfm(bfm)
    lms = utils.read_landmarks(MODELS_PATH + LM_FNAME)  # landmark annotations

    img_real = utils.read_image(IMAGE_PATH + load_fname)  # load image of face we want to reconstruct
    h, w, _ = np.shape(img_real)

    lm_real = torch.from_numpy(detect_landmark(img_real))  # detect ground-truth landmarks
    lm_real_flip = utils.flip_ycoords(lm_real, H=h)  # flip y axis because img is upside down compared to pinhole output

    alpha, delta, rotation, translation, loss = latent.estimate_params((bfm_params, color, triangles),
                                                                       lms, lm_real_flip, h=h, w=w,
                                                                       reg_a=reg_a, reg_d=reg_d)
    utils.print_stats(alpha, delta, rotation, translation)  # latent params statistics

    utils.save_loss(loss, save_fname=save_fname + str(idx) + "_loss.pdf")

    G = morph.compute_G(bfm_params, alpha=alpha, delta=delta)
    G_pinhole = pinhole.camera_model(G, rotation, translation, h=h, w=w)

    color = texture.get_color(img_real, G_pinhole[:, :2])  # obtain vertex colors from provided image

    save_obj(OBJ_3D_PATH + save_fname + str(idx) + "_3d.obj", G, color, triangles)
    save_obj(OBJ_2D_PATH + save_fname + str(idx) + "_2d.obj", G_pinhole, color, triangles)

    print("Rendering...")
    img_pred = utils.get_image(G_pinhole, color, triangles, h=h, w=w)

    utils.show_face(img_pred)
    utils.flip_y()
    plt.savefig(PINHOLE_PATH + save_fname + str(idx) + ".pdf")
    plt.close()

    lm_pred_flip = utils.get_landmarks(G_pinhole[:, :2], lms)
    lm_pred = utils.flip_ycoords(lm_pred_flip, H=h)

    utils.show_face(img_real, white_background=False)
    utils.show_landmarks(lm_real, indices=False, label="ground-truth")
    try:
        utils.show_landmarks(lm_pred, indices=False, label="model")
    except TypeError:
        print("... unable to show predicted landmarks")
    plt.savefig(PINHOLE_PATH + save_fname + str(idx) + "_lm.pdf")
    plt.close()


def multiple_demo(load_fnames, save_fname="multi", reg_a=10., reg_d=10.):
    # assignment: section 6
    bfm = h5py.File(MODELS_PATH + BFM_FNAME, "r")
    bfm_params, color, triangles = utils.read_bfm(bfm)
    lms = utils.read_landmarks(MODELS_PATH + LM_FNAME)  # landmark annotations

    N = len(load_fnames)  # number of images to be loaded

    imgs_real = [utils.read_image(IMAGE_PATH + fname) for fname in load_fnames]  # load all images
    hs = [np.size(img, 0) for img in imgs_real]  # store all heights
    ws = [np.size(img, 1) for img in imgs_real]  # store all widths

    lms_real = [torch.from_numpy(detect_landmark(img)) for img in imgs_real]  # detect all ground truth landmarks
    lms_real_flip = [utils.flip_ycoords(lms_real[i], H=hs[i]) for i in range(N)]  # flip y axis

    alpha, deltas, rotations, translations, loss = multiple.estimate_params((bfm_params, color, triangles),
                                                                            lms, lms_real_flip, hs=hs, ws=ws,
                                                                            reg_a=reg_a, reg_d=reg_d)

    utils.save_loss(loss, save_fname=save_fname + "_loss.pdf")

    # save results for each image
    for i in range(N):
        print(load_fnames[i] + ":")  # print stats for each image  (alpha is the same for each img)
        utils.print_stats(alpha, deltas[i], rotations[i], translations[i])

        G = morph.compute_G(bfm_params, alpha=alpha, delta=deltas[i])
        G_transformed = pinhole.transform(G, rotations[i], translations[i])
        G_pinhole = pinhole.camera_model(G, rotations[i], translations[i], h=hs[i], w=ws[i])

        color = texture.get_color(imgs_real[i], G_pinhole[:, :2])

        print("Rendering...")
        img_pred = utils.get_image(G_pinhole, color, triangles, h=hs[i], w=ws[i])
        utils.show_face(img_pred)
        utils.flip_y()
        plt.savefig(PINHOLE_PATH + save_fname + str(i) + ".pdf")
        plt.close()

        save_obj(OBJ_3D_PATH + save_fname + str(i) + "_3d.obj", G_transformed, color, triangles)
        save_obj(OBJ_2D_PATH + save_fname + str(i) + "_2d.obj", G_pinhole, color, triangles)

        lm_pred_flip = utils.get_landmarks(G_pinhole[:, :2], lms)
        lm_pred = utils.flip_ycoords(lm_pred_flip, H=hs[i])

        utils.show_face(imgs_real[i], white_background=False)
        utils.show_landmarks(lms_real[i], indices=False, label="ground-truth")
        try:
            utils.show_landmarks(lm_pred, indices=False, label="model")
        except TypeError:
            print("... unable to show predicted landmarks")
        plt.savefig(PINHOLE_PATH + save_fname + str(i) + "_lm.pdf")
        plt.close()


def main():
    # log = open("logfile.log", "a")
    # sys.stdout = log

    utils.build_structure([MODELS_PATH, OBJ_2D_PATH , OBJ_3D_PATH, PINHOLE_PATH, IMAGE_PATH, LOSS_PATH])
    utils.clean_folders([OBJ_2D_PATH, OBJ_3D_PATH, LOSS_PATH, PINHOLE_PATH])

    # although each section builds upon the previous one
    # we split the work for better overview of the implementation
    print("Running:")

     print("> Morphable model")
     morph_demo(idx=0)
     morph_demo(idx=1)
     morph_demo(idx=2)
    
     print("> Pinhole camera model")
     pinhole_demo(rotation=[0., -10., 0.], translation=[0., 0., 0.], idx=0)
     pinhole_demo(rotation=[0., +10., 0.], translation=[0., 0., 0.], idx=1)
     pinhole_demo(rotation=[0., +10., 0.], translation=[0., 0., -500.], idx=2)
    
     print("> Latent parameters estimation")
     print(f"    reg_a=1., reg_d=1.")
     latent_demo(load_fname="yke_neutral.jpeg", reg_a=1., reg_d=1., idx=0)
     print(f"    reg_a=10., reg_d=10.")
     latent_demo(load_fname="yke_neutral.jpeg", reg_a=10., reg_d=10., idx=1)
     print(f"    reg_a=30., reg_d=30.")
     latent_demo(load_fname="yke_neutral.jpeg", reg_a=30., reg_d=30., idx=2)
     print(f"    reg_a=60., reg_d=60.")
     latent_demo(load_fname="yke_neutral.jpeg", reg_a=60., reg_d=60., idx=3)

    print("> Texturing")
    texture_demo(load_fname="yke_neutral.jpeg", reg_a=15., reg_d=15.)

    print("> Energy optimization using multiple frames")
    multiple_demo(load_fnames=["yke_neutral.jpeg", "yke_happy.jpeg", "yke_serious.jpeg", , "yke_side.jpeg"], reg_a=15., reg_d=15.)
    return 0


if __name__ == "__main__":
    main()
