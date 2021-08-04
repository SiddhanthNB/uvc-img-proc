from skimage import io
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from flask import Flask, redirect, url_for, render_template, request, jsonify
import json

from image_processing import ImageProc

GPIO.setwarnings(False)
#camera = PiCamera()

app = Flask(__name__)

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
        time = int(request.form["nm"])
        """
        #relay setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        
        #setting uvc light on
        GPIO.output(21, GPIO.LOW)
        sleep(3)
        
        #trigerring camera
        camera.start_preview()
        sleep(5)
        camera.capture("/home/pi/project/flask_app/images/before.jpg")
        camera.stop_preview()
        
        #uvc treatment
        sleep(1200)
        
        #trigerring camera
        camera.start_preview()
        sleep(5)
        camera.capture("/home/pi/project/flask_app/images/after.jpg")
        camera.stop_preview()
        
        #setting uvc light off
        sleep(3)
        GPIO.output(21, GPIO.HIGH)
        GPIO.cleanup()
        """
        return redirect(url_for("output"))
    return render_template("interface.html")


@app.route("/output", methods=['GET', 'POST'])
def output():
    #reading both images 
    #before = io.imread("/home/pi/project/flask_app/images/before.jpg")
    #after = io.imread("/home/pi/project/flask_app/images/after.jpg")
    before = io.imread("https://raw.githubusercontent.com/SiddhanthNB/uvc-img-proc/main/images/IMG%201.jpg")
    after = io.imread("https://raw.githubusercontent.com/SiddhanthNB/uvc-img-proc/main/images/IMG%202.jpg")
    io.imsave("/home/pi/project/flask_app/images/before.jpg", after)
    
    before, after = ImageProc.pre_processing(before, after)
    io.imsave("/home/pi/project/flask_app/images/edge_before.jpg", before)
    io.imsave("/home/pi/project/flask_app/images/edge_after.jpg", after)
    
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
    
    #return f"<h2>{result}</h2>"
    return render_template("dict.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)