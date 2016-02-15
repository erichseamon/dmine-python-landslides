import numpy as np
from flask import Flask, render_template, request, url_for, abort, jsonify
import cPickle as pickle

yelp_logreg = pickle.load(open("yelplogit.pkl", "rb"))

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/form/', methods=['POST'])
def formaction():
    name=request.form['geology']
    email=request.form['']
    return render_template('form_action.html', name=name, email=email)

# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="129.101.160.58",
        port=int("5000")
  )































app.route('/', methods=['POST'])
def make_form():



@app.route('/api', methods=['POST'])
def make_predict():
    #all kinds of error checking should go here
    data = request.get_json(force=True)
    #convert our json to a numpy array
    predict_request = [data['cool'],data['useful'],data['funny']] 
    predict_request = np.array(predict_request)
    #np array goes into random forest, prediction comes out
    y_hat = yelp_logreg.predict(predict_request)
    #return our prediction
    output = [y_hat[0]]
    return jsonify(results=output)
if __name__ == '__main__':
    app.run(host='129.101.160.58', port = 5000, debug = True)
