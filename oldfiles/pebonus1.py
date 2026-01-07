from project_euler import Measure, Progress, validation, solution
import numpy as np
from functools import partial
from scipy.special import comb
from scipy.ndimage import convolve
import json
with Measure("import pyplot"):
    import matplotlib.pyplot as plt

N = 10 ** 12
MOD = 7
SIZE = (975//5, 585//5)

ncr = partial(comb, exact=True)

def paths(n, x, y):
    if (n+x+y)%2 == 0:
        return 0
    return ncr(n, (n-x-y)//2)*ncr(n, (n+x-y)//2)


# Constants
IMAGE_PATH = "/home/bar_an/projects/retro/improc/cartoon.png"
N = 35
K_SIZE = 2*N

def main():
    # 1. Load image
    img = plt.imread(IMAGE_PATH)  # Normalize to 0-1 range
    # import pdb; pdb.set_trace()

    # 2. Generate and normalize matrix
    kernel = np.fromfunction(np.vectorize(lambda y, x: paths(N, x, y)), (K_SIZE, K_SIZE), dtype=float).astype(float)
    kernel /= kernel.sum()

    # 3. Apply filter
    # Works for both Grayscale (2D) and RGB (3D)
    # import pdb; pdb.set_trace()
    if img.ndim == 3:
        filtered = np.stack([convolve(img[:,:,i], kernel) for i in range(img.shape[2])], axis=2)
    else:
        filtered = convolve(img, kernel)
    import pdb; pdb.set_trace()

    # 4. Save result
    res = np.clip(filtered, 0, 1)
    plt.imshow(img)
    plt.show()
    plt.imshow(res)
    plt.show()
    print("Done!")

if __name__ == "__main__":
    main()
