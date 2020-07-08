
# code for "Morphable model"
# see utils.py for read_bfm function

import torch


def sample_alpha_delta(id_comps=30, exp_comps=20):
    # Sample alpha and delta uniformly
    alpha = torch.rand(id_comps) * 2 - 1  # ~ U(-1, 1)
    delta = torch.rand(exp_comps) * 2 - 1  # ~ U(-1, 1)
    return alpha, delta


def compute_G(params, alpha=None, delta=None, id_comps=30, exp_comps=20):
    (mu_id, mu_exp, E_id, E_exp, sig_id, sig_exp) = params
    if alpha is None or delta is None:
        alpha, delta = sample_alpha_delta(id_comps=id_comps, exp_comps=exp_comps)

    # Compute pcd
    G = mu_id + E_id @ (alpha * sig_id) + mu_exp + E_exp @ (delta * sig_exp)
    return G
