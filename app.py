from flask import Flask, render_template
from flask_wtf import Form
from flask_restful import Resource
from wtforms.fields.html5 import DateField

import numpy as np
from flask import request, url_for, abort, jsonify
import cPickle as pickle

#import ssl
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain('/etc/httpd/ssl/nkn-san.crt', '/etc/httpd/ssl/nkn-san.key')

app = Flask(__name__)
app.secret_key = 'erich'


class ExampleForm(Form):
    dt = DateField('DatePicker', format='%Y-%m-%d')


@app.route('/', methods=['POST','GET'])
def form_first():
    form = ExampleForm()
    if form.validate_on_submit():
        return form.dt.data.strftime('%Y-%m-%d')
    return render_template('map.html', form=form)

def handle_data():
    if request.method == 'POST':
        startdate = request.form.get('startdate')
	enddate = request.form.get('enddate')
        userlatlong = request.form.get('UserLatLong')
        print userlatlong
        #your code



@app.route('/landslides', methods=['POST'])
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

