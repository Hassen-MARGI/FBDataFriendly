from skimage.metrics import structural_similarity as ssim
from skimage import io
import os

def compare_images(image1_path, image2_path, threshold=0.9):
    if not (os.path.exists(image1_path) and os.path.exists(image2_path)):
        return False  # If one of the images does not exist, consider them different.

    image1 = io.imread(image1_path, as_gray=True)
    image2 = io.imread(image2_path, as_gray=True)
    if image1.shape != image2.shape:
        return False
    data_range = max(image1.max(), image2.max()) - min(image1.min(), image2.min())
    similarity, _ = ssim(image1, image2, data_range=data_range, full=True)
    if similarity >= threshold:
        return True
    else:
        return False
