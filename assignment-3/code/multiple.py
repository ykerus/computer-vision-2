
# code for "Energy optimization using multiple frames"
# see utils for more general functions

import torch
from torch.autograd import Variable

import morph
import pinhole
import utils


def loss_fn(ps, ls, a, ds, reg_a=10., reg_d=10.):
    # input: p = predicted landmarks, l = ground truth
    #        a = alpha, d = delta
    L = 0.
    for i in range(len(ps)):
        Llan = torch.mean(torch.norm(ps[i] - ls[i], dim=1)**2)
        Lreg = reg_a * torch.sum(a**2) + reg_d * torch.sum(ds[i]**2)
        L += Llan + Lreg
    return L


def estimate_params(bfm_all, lms, lms_real, id_comps=30, exp_comps=20, reg_a=10., reg_d=10., hs=480., ws=640.,
                    steps=10000, lr=.1, threshold=1.):
    bfm_params, color, triangles = bfm_all

    lms_real = lms_real if isinstance(lms_real, list) else [lms_real]
    hs = hs if isinstance(hs, list) else [hs]
    ws = ws if isinstance(ws, list) else [ws]
    N = len(lms_real)

    deltas = []
    for i in range(N):
        alpha, delta = morph.sample_alpha_delta(id_comps=id_comps, exp_comps=exp_comps)
        deltas.append(delta)
    alpha = Variable(alpha, requires_grad=True)
    deltas = [Variable(delta, requires_grad=True) for delta in deltas]

    rotations = [Variable(torch.rand(3)*2-1, requires_grad=True) for i in range(N)]
    translations = [Variable(torch.cat((torch.rand(2)*2-1, torch.tensor([-500.]))), requires_grad=True) for i in range(N)]

    optimizer = torch.optim.Adam([alpha] + deltas + rotations + translations, lr=lr)
    losses = []

    print("Optimizing...")
    # optimize for the specified loss function
    for i in range(steps):
        optimizer.zero_grad()
        Gs = [morph.compute_G(bfm_params, alpha=alpha, delta=delta) for delta in deltas]
        Gs_pinhole = [pinhole.camera_model(Gs[i], rotations[i], translations[i], h=hs[i], w=ws[i]) for i in range(N)]
        lms_pred = [utils.get_landmarks(G_pinhole[:, :2], lms) for G_pinhole in Gs_pinhole]
        loss = loss_fn(lms_pred, lms_real, alpha, deltas, reg_a=reg_a, reg_d=reg_d)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
        if i > 0 and losses[-2] - loss < threshold:
            # stop if difference with prev loss is less than threshold
            print(f"... stopping early at iteration {i}")
            break

    return alpha.detach(), [delta.detach() for delta in deltas], \
           [rotation.detach() for rotation in rotations], \
           [translation.detach() for translation in translations], \
           losses