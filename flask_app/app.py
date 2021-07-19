from flask import Flask, redirect, url_for, render_template, request

"""from skimage import io
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
# from turnon import relay_on
# from turnof import relay_off
from image_processing import ImageProc

GPIO.setwarnings(False)

camera = PiCamera()"""

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    #return redirect(url_for("login"))
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
        res = { "label1": time,
        "label2": 2,
        "label3": 3
                }
        
        """GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21, GPIO.LOW)
        sleep(3)
        camera.start_preview()
        sleep(5)
        camera.capture("/home/pi/project/images/test1.jpg")
        camera.stop_preview()


        sleep(time)

        camera.start_preview()
        sleep(5)
        camera.capture("/home/pi/project/images/test2.jpg")
        camera.stop_preview()
        sleep(3)
        GPIO.output(21, GPIO.HIGH)
        GPIO.cleanup()


        before = io.imread("/home/pi/project/images/test1.jpg")
        after = io.imread("/home/pi/project/images/test2.jpg")

        before, after = ImageProc.pre_processing(before, after)
        mse, ssi =  ImageProc.compare(before, after)
        if ssi == 1.00 or mse == 0.00:
            res = { "status" : "Success",
                "MSE Value" :  mse ,
                "SSI Value" : ssi
                }
        else:
            res = { "status" : "Failure",
                    "MSE Value" :  mse,
                    "SSI Value" : ssi
            }"""
        return redirect(url_for("days", result=res ))
    else:
        return render_template("interface.html")


@app.route("/<result>")
def days(result):
    return f"<h2>{result}</h2>"

if __name__ == "__main__":
    app.run(debug=True)
