from flask import Flask, render_template, request, jsonify
from load_data import DataModel

app = Flask(__name__)
data_model = DataModel()

@app.route('/')
def home():
    #current_fires = data_model.get_top_fires()
    return render_template('home.html')

@app.route('/index.html')
def index():
    current_fires = data_model.get_top_fires()
    return render_template('index.html', current_fires=current_fires)

@app.route('/about.html')
def charts():
    return render_template('about.html')

@app.route('/map.html')
def map():
    return render_template('map.html')

@app.route('/fires.html')
def fires():
    return render_template('fires.html')

@app.route('/model.html')
def model():
    return render_template('model.html')

@app.route('/results.html')
def results():
    return render_template('results.html')

@app.route('/aboutme.html')
def aboutme():
    return render_template('aboutme.html')

@app.route('/data.html')
def data():
    return render_template('data.html')

@app.route("/predict_single", methods=["POST"])
def predict_single():
    data = request.json
    result = data_model.predict_single(data)
    print(result)
    return jsonify(result[0])
    #noun, adjective = str(data['noun']), str(data['adjective'])
    #print (noun, adjective)
    #noun_s, adjective_s = _translate_spanish(noun, adjective)
    #print (noun_s, adjective_s)
    #return jsonify({'noun_s': noun_s, 'adjective_s': adjective_s})


#def _translate_spanish(noun, adjective):
    #noun_s = noun + 'o'
    #adjective_s = adjective + 'o'
    #return noun_s, adjective_s

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=False)
