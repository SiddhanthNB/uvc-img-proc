import cv2
from time import sleep
from skimage.metrics import structural_similarity as ssim
import numpy as np
from scipy.linalg import norm
from scipy import average
from PIL import Image
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage import img_as_ubyte, img_as_float
from matplotlib import pyplot as plt

class ImageProc:
    Image.MAX_IMAGE_PIXELS = None

    def uniform_dim(imageA, imageB):
        h1, w1 = imageA.shape
        h2, w2 = imageB.shape
        if (h1 != h2) or (w1 != w2):
            imageA = cv2.resize(imageA, (min(w1,w2), min(h1,h2)))
            imageB = cv2.resize(imageB, (min(w1,w2), min(h1,h2)))
        return imageA, imageB
    
    def pre_processing(imageA, imageB):
        def de_noise(img):
            float_img = img_as_float(img)
            sigma_est = np.mean(estimate_sigma(float_img, multichannel=True))
            denoise_img = denoise_nl_means(float_img, h=1.15 * sigma_est, fast_mode=True, 
                                           patch_size=5, patch_distance=3, multichannel=True)                               
            return img_as_ubyte(denoise_img)
        # noise removal
        imageA = de_noise(imageA)
        imageB = de_noise(imageB)
        
        #clr to grey
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        
        #edge detetction
        imageA = cv2.Canny(imageA, 100, 200)
        imageB = cv2.Canny(imageB, 100, 200)
        
        #uniform dimensions
        imageA, imageB = ImageProc.uniform_dim(imageA, imageB)
        
        #sharpening the images
        kernel = np.array([ [-1,-1,-1],
                            [-1,5,-1],
                            [-1,-1,-1] ])
        imageA = cv2.filter2D(imageA, -1, kernel)
        imageB = cv2.filter2D(imageB, -1, kernel)
        
        return (imageA, imageB)

    def compare(imageA, imageB):   
        s = ssim(imageA, imageB, multichannel=True)
        m = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        m /= float(imageA.shape[0] * imageA.shape[1])
        #m,s=(round(m,2),round(s,2))
        return (m,s)

    def compare_images(img1, img2):
        def normalize(arr):
            rng = arr.max()-arr.min()
            amin = arr.min()
            return (arr-amin)*255/rng
        # normalising pixels 
        img1 = normalize(img1)
        img2 = normalize(img2)
        
        # to find norm0 and norm1
        diff = img1 - img2 
        m_norm = np.sum(abs(diff))
        z_norm = norm(diff.ravel(), 0)  
        return (m_norm, z_norm)

    def hist_compare(before, after):
        diff =0.0
        h1,b1 = np.histogram(before)
        h2,b2 = np.histogram(after)
        
        """plt.hist(h1,b1) 
        plt.title("before UVC") 
        plt.savefig('before_hist.jpg')
        
        plt.hist(h2,b2) 
        plt.title("after UVC") 
        plt.savefig('after_hist.jpg')"""
        
        for i in range(len(h1)):
          diff += abs(h1[i] - h2[i])
        maxSum = max(h1.sum(), h2.sum())
        return (diff/(2*maxSum))

