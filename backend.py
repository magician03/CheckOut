from flask import Flask, render_template, request
import cv2

app = Flask(__name__,template_folder='templates')

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/index2')
def index2():
	return render_template('index2.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/barcode')
def barcode():
	return render_template('Reader.html')

@app.route('/api')
def run():
	# from object_detection import HINT as hint
	# info = hint.run()
	# print(info)
	return render_template('api.html')

@app.route('/getimage/<imageData>')
def get_javascript_data(imageData):
	print (imageData)
    # return imageData

@app.route('/postimage', methods = ['POST'])
def get_post_javascript_data():
	print ('hello')
	# print (request.data)
	#print (request.files.keys())
	file = request.data
	# cv2.imwrite("data.png",file)
	with open('data.jpg',"wb+") as f:
		f.write(file)
	#if file:
	#	file.save(os.path.join(os.getcwd(), 'data.png'))
	#imageData = request.files['cameraInput']

	#print (imageData)

	#print (imageData)
	#print ('hello')"""
	return render_template('home.html')
    # return imageData


if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 1346, debug = True, threaded= True)