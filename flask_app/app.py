from skimage import io
import cv2
from time import sleep
import RPi.GPIO as GPIO
from flask import Flask, redirect, url_for, render_template, request, jsonify, session
#from picamera import PiCamera

from image_processing import ImageProc

GPIO.setwarnings(False)
#camera = PiCamera()

app = Flask(__name__)

def my_capture(img_name):
    """camera.start_preview()
    sleep(5)
    camera.capture("/home/pi/project/images/{}.jpg".format(img_name))
    camera.stop_preview()"""
    
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        img_name = "/home/pi/project/images/{}.jpg".format(img_name)
        cv2.imwrite(img_name, frame)
        #print("{} written!".format(img_name))
        break
    cam.release()
    cv2.destroyAllWindows()  

@app.route("/", methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'uvc' or request.form['password'] != 'kleitece':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('input'))
    return render_template('login.html', error=error)

@app.route("/input", methods=["POST", "GET"])
def input():
    if request.method == "POST":
        time = float(request.form["nm"])
        #session["t"] = time
        
        #relay setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        
        #setting uvc light on
        GPIO.output(21, GPIO.LOW)
        sleep(3)
        
        #trigerring camera
        my_capture("before")
        
        
        #uvc treatment
        sleep(time*60)
        
        #trigerring camera
        my_capture("after")
        
        #setting uvc light off
        sleep(3)
        GPIO.output(21, GPIO.HIGH)
        GPIO.cleanup()
        
        return redirect(url_for("output"))
    return render_template("interface.html")


@app.route("/output", methods=['GET', 'POST'])
def output():
    #reading both images
    before = io.imread("/home/pi/project/images/before.jpg")
    after = io.imread("/home/pi/project/images/after.jpg")
    
    before, after = ImageProc.pre_processing(before, after)
    
    io.imsave("/home/pi/project/images/edge_before_final.jpg", before)
    io.imsave("/home/pi/project/images/edge_after_final.jpg", after)
    
    mse, ssi =  ImageProc.compare(before, after)
    h_diff = ImageProc.hist_compare(before, after)
    n_m, n_0 = ImageProc.compare_images(before, after)
    
    if ssi == 1.00:
        result = { "status" : "Failure",
            "SSI Value" : ssi,
            "MSE Value" :  mse,
            "Histogram diff": h_diff,
            "Zero norm/pixel": n_0*1.0/after.size,
            "Manhattan norm/pixel": n_m/before.size
            }
         
    else:
        result = { "status" : "Success",
            "SSI Value" : ssi,
            "MSE Value" :  mse,
            "Histogram diff": h_diff,
            "Zero norm/pixel": n_0*1.0/after.size,
            "Manhattan norm/pixel": n_m/before.size
            }
        #res = json.dumps(res)

    if request.method == "POST":
        #if yes:    
        return redirect(url_for("images"))
        
    #return f"<h2>{result}</h2>"   
    return render_template("dict.html", result=result)

@app.route("/images", methods=['GET', 'POST'])
def images():
    return render_template("tmp.html")


if __name__ == "__main__":
    app.run(debug=True)
