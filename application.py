from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import flask
from PIL import Image
import numpy as np

#model = pickle.load(open('model.pkl', 'rb'))
model = load_model('my_model.h5')
model.make_predict_function()
application = Flask(__name__)


#model.make_predict_function()

def predict_label(img_path):
	img = tf.keras.utils.load_img(img_path, target_size=(224,224))
	x = tf.keras.utils.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	images = np.vstack([x])
	p = model.predict(images,batch_size=10)
	return (str(round(p[0][0][0],2)) +" kg/m2 , "+ str(round(p[1][0][0],2))+ " yrs")


# routes
@application.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@application.route("/about")
def about_page():
	return "Please subscribe  Artificial Intelligence Hub..!!!"

@application.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	application.run(debug = True)
