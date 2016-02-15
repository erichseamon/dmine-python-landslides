import numpy as np
#need to 'conda install flask' for this to work
from flask import Flask, abort, jsonify, request, render_template
from flask.ext.googlemaps import GoogleMaps
from flask_googlemaps import Map
import cPickle as pickle
from pymongo import MongoClient
import StringIO
import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

landslide_model = pickle.load(open("/git/data/landslides/models/climate-landslide.pkl", "rb"))

app = Flask(__name__)

GoogleMaps(app)

#@app.route('/')
#def home():
#     return render_template('landslide2.html')

@app.route('/')

@app.route('/form', methods=['POST'])
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )

    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':[(37.4419, -122.1419)],
                 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png':[(37.4300, -122.1400)]}
    )
    geology = request.form['geology']
    return render_template('newmap3.html', mymap=mymap, sndmap=sndmap)

# def handle_data():
#     projectpath = request.form.projectFilePath
#     return jsonify(results=projectpath)

def connect_mongo(text):
    client = MongoClient()
    db = client['mydb']
    collection = db['vload']
    b = list()
    a = list(collection.find())
    for i in range(len(a)):
        b.append(a[i][text])
        return b


@app.route('/plot', methods=['POST'])
def plot_perf_metric():

        if(request.form['submit_plot'] == "Send"):
                text = request.form['perf_metric']
                #return render_template('plot.html')
            
                #all kinds of error checking should go here
    		data = request.get_json(force=True)
    		#convert our json to a numpy array
    		predict_request = [data['GEOLOGIC_1'],data['gradient_cat'],data['reacch_soi'],data['LANDSLIDE1'],data['SLOPE_MORP'],data['LAND_USE']]
    		predict_request = np.array(predict_request)
    		y_hat = landslide_model.predict(predict_request)
    		#return our prediction
    		output = [y_hat[0]]
    		return jsonify(results=output)


@app.route('/entry', methods=['GET', 'POST'])
def entry_page():
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['blog_title']
        post = request.form['blog_main']
        post_entry = models.BlogPost(date = date, title = title, post = post)
        db.session.add(post_entry)
        db.session.commit()
        return redirect(url_for('database'))
    else:
        return render_template('entry.html')

@app.route('/database', methods=['GET', 'POST'])        
def database():
    query = []
    for i in session.query(models.BlogPost):
        query.append((i.title, i.post, i.date))
    return render_template('database.html', query = query)




@app.route('/output')
def output_plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    b=connect_mongo(plot_perf_metric.text)
    fig = axis.plot(b)
    output = StringIO.StringIO()
    response = make_response(output.getvaluest())
    response.mimetype = 'image/png'
    fig.savefig(output)
    output.seek(0)
    return send_file(output, mimetype='image/png')


@app.route('/api', methods=['POST'])
def make_predict():
    #all kinds of error checking should go here
    data = request.get_json(force=True)
    #convert our json to a numpy array
    predict_request = [data['GEOLOGIC_1'],data['gradient_cat'],data['reacch_soi'],data['LANDSLIDE1'],data['SLOPE_MORP'],data['LAND_USE']] 
    predict_request = np.array(predict_request)
    y_hat = landslide_model.predict(predict_request)
    #return our prediction
    output = [y_hat[0]]
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(host='129.101.160.58', port = 5000, debug = True)
