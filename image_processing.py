import cv2
from time import sleep
import skimage.metrics
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class ImageProc:
    Image.MAX_IMAGE_PIXELS = None

    def uniform_dim(imageA, imageB):
        h1, w1 = imageA.shape
        h2, w2 = imageB.shape
        if (h1 != h2) or (w1 != w2):
            imageA = cv2.resize(imageA, (min(w1,w2), min(h1,h2)))
            imageB = cv2.resize(imageB, (min(w1,w2), min(h1,h2)))
        return imageA, imageB

    def compare(imageA, imageB):   
        s = skimage.metrics.structural_similarity(imageA, imageB, multichannel=True)
        m = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        m /= float(imageA.shape[0] * imageA.shape[1])
        m,s=(round(m,2),round(s,2))
        return (m,s)

    def pre_processing(imageA, imageB): #NOT SURE BC!
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        imageA = cv2.Canny(imageA, 100, 200)
        imageB = cv2.Canny(imageB, 100, 200)
        imageA, imageB = ImageProc.uniform_dim(imageA, imageB)
        return (imageA, imageB) #can also be changed!

    def display_images(imageA, imageB):
        fig = plt.figure()
        ax = fig.add_subplot(1, 2, 1)
        plt.imshow(imageA, cmap = plt.cm.gray)
        plt.axis("off")
        ax = fig.add_subplot(1, 2, 2)
        plt.imshow(imageB, cmap = plt.cm.gray)
        plt.axis("off")
        plt.show()

