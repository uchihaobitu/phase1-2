# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 20:00:04 2022

@author: 61995
"""

import os
import numpy as np
import torch

from tua import plot_estimated_graph_v2
from models.cgru_error import CRVAE, VRAE4E, train_phase1,train_phase2,train_phase3,train_phase4

# 这里可以设置使用的GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
torch.backends.cudnn.enabled = False

# device = torch.device('cuda')
device = torch.device("cpu" if not torch.cuda.is_available() else "cuda")

# X_np = np.load("henon.npy").T
# X_np = np.load("train_use_A2.npy")
X_np = np.load("fse-ss/carts_cpu/1/norm_data.npy")
# X_np = np.load("db_003.npy")

X_np = X_np.astype(np.float32)

print(X_np.shape)
print(X_np)

dim = X_np.shape[-1]
GC = np.zeros([dim, dim])
for i in range(dim):
    GC[i, i] = 1
    if i != 0:
        GC[i, i - 1] = 1
X = torch.tensor(X_np[np.newaxis], dtype=torch.float32, device=device)


full_connect = np.ones(GC.shape)
# full_connect = np.load('W_est.npy')
# full_connect = torch.tensor(full_connect,device=device,dtype=torch.float64)
print(full_connect.shape)
cgru = CRVAE(X.shape[-1], full_connect, hidden=64).to(device=device)
vrae = VRAE4E(X.shape[-1], hidden=64).to(device=device)

# # %%
#
#
# train_loss_list = train_phase1(
#     cgru, X, context=20, lam=0.1, lam_ridge=0, lr=5e-2, max_iter=1000, check_every=50, batch_size=32
# )  # 0.1
train_loss_list = train_phase3(
    cgru, X, context=20, lam=0.1, lam_ridge=0, lr=5e-2, max_iter=1000, check_every=50, batch_size=128
)  # 0.1


# %%no
GC_est = cgru.GC().cpu().data.numpy()
np.save('GC_henon_A2.npy', GC_est)

# # Make figures
# fig, axarr = plt.subplots(1, 2, figsize=(10, 5))
# axarr[0].imshow(GC, cmap='Blues')
# axarr[0].set_title('Causal-effect matrix')
# axarr[0].set_ylabel('Effect series')
# axarr[0].set_xlabel('Causal series')
# axarr[0].set_xticks([])
# axarr[0].set_yticks([])

# axarr[1].imshow(GC_est, cmap='Blues', vmin=0, vmax=1, extent=(0, len(GC_est), len(GC_est), 0))
# axarr[1].set_ylabel('Effect series')
# axarr[1].set_xlabel('Causal series')
# axarr[1].set_xticks([])
# axarr[1].set_yticks([])

# # Mark disagreements
# for i in range(len(GC_est)):
#     for j in range(len(GC_est)):
#         if GC[i, j] != GC_est[i, j]:
#             rect = plt.Rectangle((j, i-0.05), 1, 1, facecolor='none', edgecolor='red', linewidth=1)
#             axarr[1].add_patch(rect)

# # plt.show()
# plt.savefig('GC_henon.png')
#
# #np.save('GC_henon.npy', GC_est)
full_connect = np.load('carts_cpu_1.npy')
threshold = 0.55
full_connect = (full_connect > threshold).astype(int)
np.save('carts_cpu_1_true.npy',full_connect)

#
#
# #%%
# cgru = CRVAE(X.shape[-1], full_connect, hidden=64).cuda(device=device)
cgru = CRVAE(X.shape[-1], full_connect, hidden=64).to(device=device)
vrae = VRAE4E(X.shape[-1], hidden=64).cuda(device=device)
#
#
train_loss_list = train_phase2(
    cgru, vrae, X, context=20, lam=0., lam_ridge=0, lr=5e-2, max_iter=1000,
    check_every=50,batch_size=128)
GC_new = cgru.GC_gai().cpu().data.numpy()
np.save('GC_henon_A2new.npy', GC_new)

W1 = np.load('carts_cpu_1.npy')
W2 = np.load('carts_cpu_1new.npy')
plot_estimated_graph_v2(W1, W2)
