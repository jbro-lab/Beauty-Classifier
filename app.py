
from flask import Flask, request, render_template
from deepface import DeepFace
import numpy as np
import keras.models as models
import keras.utils as image
import pandas as pd
from collections import defaultdict
from scipy import stats
import os
from werkzeug.utils import secure_filename

key = os.urandom(24)
b'key'

PATH = os.getcwd() + '/mysite' if 'jbrolab' in os.getcwd() else os.getcwd()


UPLOAD_FOLDER = PATH +'/photos'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = '_your_random_secret_key_here_'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = models.load_model(PATH + '/models/attractiveNet_mnv2.h5')

df = pd.read_csv(PATH + '/data/All_Ratings.csv')
all_images = defaultdict(list)
for filename, rating in df[['Filename', 'Rating']].values:
    all_images[filename].append(rating)

ys = []
for filename, ratings in all_images.items():
    ys.append(np.mean(ratings))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detectAnzie(img_path):
    directory = PATH + '/photos/anzie'
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
          verify = DeepFace.verify(os.path.join(directory, filename), img2_path = img_path, distance_metric="euclidean_l2", enforce_detection=False)
          if verify["verified"] == True:
            return True
    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/celebrities')
def celebrities():
    return render_template('celebrities.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/predict',methods=['POST'])
def predict():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            print(request.files)
            if 'img' not in request.files:
                error_message = 'No file part'
                return render_template('index.html', error=error_message)
            
            file = request.files['img']
            print('file: ', file)
            # if user does not select file, browser also
            # submit an empty part without a filename
            if file.filename == '':
                error_message = 'No selected file'
                return render_template('index.html', error=error_message)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                print('file_path: ', file_path)
                file.save(file_path)
                try:
                    img = DeepFace.extract_faces(img_path = file_path)
                    if len(img) > 1:
                        error_message = 'More than one face detected'
                        return render_template('index.html', error=error_message)
                    img = img[0]['face'].astype(np.float64)
                    isAnzie = detectAnzie(file_path)
                    files_list = os.listdir(UPLOAD_FOLDER)
                    num_files = len(files_list)
                    new_img_file = image.array_to_img(img)
                    new_img_file.save(os.path.join(UPLOAD_FOLDER, f'img-{num_files + 1}.png'))
                    if not isAnzie:
                        img = image.load_img(file_path)
                        img = image.img_to_array(img)
                        os.remove(file_path)
                        prediction = model.predict(img.reshape((1,) + img.shape))
                        print(prediction)
                        rating = round(prediction[0][0] * 2,2)
                        percentile = round(stats.percentileofscore(ys, prediction[0][0]),2)
                        result = (rating, percentile)
                        return render_template('index.html', prediction=result)
                    else:
                        rating = 10
                        percentile = stats.percentileofscore(ys, 10)
                        result = (rating, percentile)
                        return render_template('index.html', prediction=result, anzie=True)
                except Exception as e:
                    print("error:   ", e)
                    error_message = 'No face detected'
                    return render_template('index.html', error=error_message)
    except:
        error_message = 'Something went wrong, please try again'
        return render_template('index.html', error=error_message)
            

if __name__ == "__main__":
    app.run()
