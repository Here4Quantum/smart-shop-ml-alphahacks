from flask import Flask, render_template, request, redirect
import os, pytesseract, cv2
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

photos = UploadSet('photos', IMAGES)

app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = '/Users/priya/Desktop/TEMP/visual code_python/Alpha/images/'

class GetText(object):

    def __init__(self, file):
        self.file = pytesseract.image_to_string(Image.open(project_dir + '/images/' + file))

@app.route('/', methods=['GET', 'POST'])
def home():
    pyParScore = ""
    text_to_print = ""
    if request.method == 'POST':
        if 'photo' not in request.files:
            return 'There is NO photo in the Form Submitted'
        name = request.form['img-name'] + '.jpg'
        photo = request.files['photo']
        path  = os.path.join(app.config['UPLOAD_FOLDER'], name)
        photo.save(path)

        textObject = GetText(name)

        output = textObject.file
        bad_chars = [';', ':', '!', '=', ')', '(', '}', '{', ']', '[', ',', '', '.', '|', 'Ingredients']
        for i in bad_chars :
            output = output.replace(i, '')

        output_list = output.split(" ")
        healthy = ['peanuts', 'almonds', 'wheat', 'walnuts', 'raisins', 'eggs', 'soy', 'milk', 'vegetable', 'water', 'antioxidants', 'minerals', 'seeds', 'pulses', 'cereals', 'honey', 'grain', 'bread', 'starch', 'carrot', 'beef', 'curry', 'spices', 'meat', 'protein', 'water', 'rice', 'Peanuts', 'Almonds', 'Wheat', 'Walnuts', 'Raisins', 'Eggs', 'Soy', 'Milk', 'Vegetable', 'Water', 'Antioxidants', 'Minerals', 'Seeds', 'Pulses', 'Cereals', 'Honey', 'Grain', 'Bread', 'Starch', 'Carrot', 'Beef', 'Curry', 'Spices', 'Meat', 'Protein', 'Water', 'Rice']
        healthy_match = set(output_list)&set(healthy)
        heaMat_number = len(healthy_match)

        unhealthy = ['Cheese', 'cheese', 'emulsifiers', 'additives', 'oils', 'fats', 'syrup', 'sugar', 'preservatives', 'processed', 'salt', 'margarine', 'preservative', 'flavour', 'colours', 'glutamate', 'cheese', 'Cheese', 'Emulsifiers', 'Additives', 'Oils', 'Fats', 'Syrup', 'Sugar', 'Preservatives', 'Processed', 'Salt', 'Margarine', 'Preservative', 'Flavour', 'Colours', 'Glutamate', 'caremal', 'Caremal']
        unhealthy_match = set(output_list)&set(unhealthy)
        unheaMat_number = len(unhealthy_match)
        mean_score = (unheaMat_number+heaMat_number)/2
        heaMat_number_str = str(heaMat_number)
        unheaMat_number_str = str(unheaMat_number)
        mean_score_str = str(mean_score)
        extracted_text_str = ' '.join([str(elem) for elem in output_list])
        sum_score = unheaMat_number + heaMat_number

        # return textObject.file
        if heaMat_number > unheaMat_number and sum_score > mean_score:
            pyParScore = heaMat_number_str
            print(extracted_text_str)
            text_to_print = "Hooray! This product's Healthy Score has overpowered the Unhealthy score, therefore we predict this product to be Healthy! We also predicted that this product is Sustainable."
            return render_template('predict.html', prediction_text = text_to_print, particular_score = pyParScore, dis_mean_score = mean_score_str, dis_extracted_text = extracted_text_str)
        elif heaMat_number > unheaMat_number and sum_score < mean_score:
            pyParScore = heaMat_number_str
            text_to_print = "Hooray! This product's Healthy Score has overpowered the Unhealthy score, therefore we predict this product to be Healthy! We also predicted that this product is Unsustainable."
            return render_template('predict.html', prediction_text = text_to_print, particular_score = pyParScore, dis_mean_score = mean_score_str, dis_extracted_text = extracted_text_str)
        elif heaMat_number < unheaMat_number and sum_score > mean_score:
            pyParScore = unheaMat_number_str
            print(extracted_text_str)
            text_to_print = "Unfortunately, this product's Unhealthy score has overpowered the Healthy score, therefore we predict this product to be Unhealthy. It would be recommended to not consume it. However, this product is sustainable."
            return render_template('predict.html', prediction_text = text_to_print, particular_score = pyParScore, dis_mean_score = mean_score_str, dis_extracted_text = extracted_text_str)
        else:
            pyParScore = unheaMat_number_str
            print(extracted_text_str)
            text_to_print = "Unfortunately, this product's Unhealthy score has overpowered the Healthy score, therefore we predict this product to be Unhealthy. It would be recommended to not consume it. Moreover, this product isn't even sustainable."
            return render_template('predict.html', prediction_text = text_to_print, particular_score = pyParScore, dis_mean_score = mean_score_str, dis_extracted_text = extracted_text_str)
        
    return render_template('index.html')



@app.route('/about-us')
def aboutUS():
    return render_template('about-us.html')

if __name__ == '__main__':
    app.run()

