'''
Band 1 → Green   (B3 / SR_B3)
Band 2 → Red     (B4 / SR_B4)
Band 3 → NIR     (B8 / SR_B5)
Band 4 → SWIR    (B11 / SR_B6)

'''

import rasterio
import numpy as np
import pandas as pd

# -------- INPUT --------
tiff_path = "curr.tiff"

with rasterio.open(tiff_path) as src:
    green = src.read(1).astype(np.float32)
    red   = src.read(2).astype(np.float32)
    nir   = src.read(3).astype(np.float32)
    swir  = src.read(4).astype(np.float32)

# Avoid divide-by-zero warnings
np.seterr(divide='ignore', invalid='ignore')

# -------- COMPUTE INDEXES --------
ndvi = (nir - red) / (nir + red)
ndwi = (green - nir) / (green + nir)
ndbi = (swir - nir) / (swir + nir)

# -------- FUNCTION TO PRINT STATS --------
def print_stats(name, arr):
    valid = arr[np.isfinite(arr)]
    print(f"\n{name}")
    print(" Min :", np.min(valid))
    print(" Max :", np.max(valid))
    print(" Mean:", np.mean(valid))

print_stats("NDVI", ndvi)
print_stats("NDWI", ndwi)
print_stats("NDBI", ndbi)

# -------- SHOW SAMPLE PIXEL VALUES --------
# print("\nSample pixel values (first 10 pixels):")
# for i in range(10):
#     print(
#         f"Pixel {i+1}: "
#         f"NDVI={ndvi.flat[i]:.3f}, "
#         f"NDWI={ndwi.flat[i]:.3f}, "
#         f"NDBI={ndbi.flat[i]:.3f}"
#     )