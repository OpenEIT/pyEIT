""" demo on forward 2D """

import numpy as np
import matplotlib.pyplot as plt

import pyeit.mesh as mesh
from pyeit.mesh import quality
from pyeit.eit.fem import forward
from pyeit.eit.utils import eit_scan_lines

""" 0. build mesh """
ms, elPos = mesh.create(16, h0=0.06)

# extract node, element, alpha
no2xy = ms['node']
el2no = ms['element']

# report the status of the 2D mesh
quality.fstats(no2xy, el2no)

""" 1. FEM forward simulations """
# setup EIT scan conditions
elDist, step = 7, 1
exMtx = eit_scan_lines(16, elDist)

# calculate simulated data
fwd = forward(ms, elPos)

# in python, index start from 0
exLine = exMtx[0].ravel()

# change alpha
anomaly = [{'x': 0.50, 'y': 0.50, 'd': 0.20, 'alpha': 10.0}]
ms_test = mesh.set_alpha(ms, anom=anomaly, background=1.0)
tri_perm = ms_test['alpha']

# solving once using fem
f, _ = fwd.solve_once(exLine, tri_perm)
f = np.real(f)
vf = np.linspace(min(f), max(f), 32)

# plot
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.tricontour(no2xy[:, 0], no2xy[:, 1], el2no, f, vf,
               linewidth=0.5, cmap=plt.cm.viridis)
ax1.tripcolor(no2xy[:, 0], no2xy[:, 1], el2no, np.real(tri_perm),
              edgecolors='k', shading='flat', alpha=0.5,
              cmap=plt.cm.Greys)
ax1.plot(no2xy[elPos, 0], no2xy[elPos, 1], 'ro')
ax1.set_title('equi-potential lines')
ax1.axis('equal')
fig.set_size_inches(6, 4)
# fig.savefig('demo_bp.png', dpi=96)
plt.show()
