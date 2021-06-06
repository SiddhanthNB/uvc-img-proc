from skimage import io
from image_processing import ImageProc

before = io.imread("https://raw.githubusercontent.com/SiddhanthNB/uvc-img-proc/main/images/IMAG%201.jpg")
#before = io.imread("https://raw.githubusercontent.com/SiddhanthNB/uvc-img-proc/main/images/IMG%201.jpg")

#uv_treatment(input("time for uv-treatment in sec"))

after = io.imread("https://raw.githubusercontent.com/SiddhanthNB/uvc-img-proc/main/images/IMAG%202.jpg")
#after = io.imread("https://raw.githubusercontent.com/SiddhanthNB/uvc-img-proc/main/images/IMG%202.jpg")

before, after = ImageProc.pre_processing(before, after)
mse, ssi =  ImageProc.compare(before, after)
if ssi == 1.00:
    print("no effect of UV", (mse, ssi))
    #uv_treatment(input("once more"))
else:
    print("success")
    print(f"SSI value: {ssi}")
    print(f"MSE value: {mse}")