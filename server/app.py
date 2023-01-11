import json
from flask import Flask, render_template, jsonify, request
import numpy as np
import random
from fairpy.items.bidding_for_envy_freeness import bidding_for_envy_freeness

class DictEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dict):
            return obj
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return super(DictEncoder, self).default(obj)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/biddings', methods=['POST'])
def my_form_post():
    print(f'Recieved size: {request.form["size"]}')
    size = int(request.form['size'])
    return render_template('biddings.html', size=size)

@app.route('/random', methods=['POST'])
def random_bids():
    print(request.form)
    size = int(request.form['size'])
    biddings = [[random.randrange(30, 60, 5) for j in range(size)] for i in range(size)]    
    return render_template('biddings.html', size=size, biddings=biddings)
    

@app.route('/bfef', methods=['POST'])
def bfef():
    size = int(request.form['size'])
    data = []
    for i in range(size):
        data.append([int(request.form[f'player{i + 1}_bundle{j + 1}']) for j in range(size)])
    # data = request.get_json()
    print(f'Recieved Bidding matrix: {data}')
    bfef = bidding_for_envy_freeness(data)
    # # for debugging
    # bfef = bidding_for_envy_freeness([[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]])
    print(bfef)
    return render_template('results.html', bfef=bfef)



if __name__ == '__main__':
    app.run(debug=True, port=5269)