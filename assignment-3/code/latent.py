
# code for "Latent parameters estimation"
# see utils for more general functions

import torch
from torch.autograd import Variable

import morph
import pinhole
import utils


def loss_fn(p, l, a, d, reg_a=10., reg_d=10.):
    # Loss function as specified in the assignment
    # input: p = predicted landmarks, l = ground truth
    #        a = alpha, d = delta
    Llan = torch.mean(torch.norm(p - l, dim=1)**2)
    Lreg = reg_a * torch.sum(a**2) + reg_d * torch.sum(d**2)
    return Llan + Lreg


def estimate_params(bfm_all, lms, lm_real, id_comps=30, exp_comps=20, reg_a=10., reg_d=10., h=480., w=640.,
                    steps=10000, lr=.1, threshold=1., R_init=None):
    bfm_params, color, triangles = bfm_all

    # define parameters to be optimized
    alpha, delta = morph.sample_alpha_delta(id_comps=id_comps, exp_comps=exp_comps)
    alpha, delta = Variable(alpha, requires_grad=True), Variable(delta, requires_grad=True)

    rotation = Variable(torch.rand(3)*2-1, requires_grad=True) if R_init is None else Variable(R_init, requires_grad=True)
    translation = Variable(torch.cat((torch.rand(2)*2-1, torch.tensor([-500.]))), requires_grad=True)

    optimizer = torch.optim.Adam([alpha, delta, rotation, translation], lr=lr)
    losses = []

    print("Optimizing...")
    # optimize for the specified loss function
    for i in range(steps):
        optimizer.zero_grad()
        G = morph.compute_G(bfm_params, alpha=alpha, delta=delta)
        G_pinhole = pinhole.camera_model(G, rotation, translation, h=h, w=w)
        lm_pred = utils.get_landmarks(G_pinhole[:, :2], lms)
        loss = loss_fn(lm_pred, lm_real, alpha, delta, reg_a=reg_a, reg_d=reg_d)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        if i > 0 and losses[-2] - loss < threshold:
            # stop if difference with prev loss is less than threshold
            print(f"... stopping early at iteration {i}")
            break

    return alpha.detach(), delta.detach(), rotation.detach(), translation.detach(), losses
