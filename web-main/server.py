from flask import Flask, jsonify, request, render_template
import requests, json, os, datetime

import urllib2
import logging, sys
logging.basicConfig(stream=sys.stderr)

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, tmpl_dir)

@app.route('/process', methods=['POST'])
def why():
    #data = jsonify(request.get_json(force=True))
    postData = request.get_json(force=True)

    weatherList = []

    for pair in postData.latlng[::30]:
        url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(pair[0]) + "&lon=" + str(pair[1])
        reads = requests.get(url)
        data = json.loads(reads.content)

        weather = data['weather'][0]['main']
        weatherList.append(weather)

    time = datetime.datetime.now()

    url = "http://maps.googleapis.com/maps/api/geocode/output?latlng=" + str(postData[0][0]) + "," + str(postData[0][1]) + "&result_type=locality&key=AIzaSyDDKmoqHCGIum6WrM3P-HZGZe1a7p_jdNg"
    reads = requests.get(url)

    if reads.status == "OK":
        city = reads.results.address_components[0].long_name
    else:
        city = ""
    
    hour = time.hour

    if hour < 7:
        light = "Dawn"
    elif hour < 16:
        light= "Daylight"
    elif hour < 20:
        light = "Dusk"
    else:
        light = "Dark"
        
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

#    for (
    data =  {
                "Id": "score00001",
                "Instance": {
                    "FeatureVector": {
                        "Sex": postData.userSex,
                        "City": city,
                        "Day": weekdays[time.weekday()],
                        "Hour": time.hour,
                        "Month": time.month,
                        "Lat": postData.latlng[0][0],
                        "Lon": postData.latlng[0][1],
                        "Light": light,
                        "Weather": weatherList[0],
                    },
                    "GlobalParameters": 
                            {
                                                    }
                }
            }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/f69f3211aea242aeb448222e541a7107/services/44d4a67e695b457bb809be1b33a2e03c/score'
    api_key = '2Gi+pEQHRapXVEDsRzJFeff2vqO/cXbFHp/SNCExoSqlFAVZ3vc/s69fx+AQZsoDpEbz3fASUsx8QDY+GA0Rvw==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib2.Request(url, body, headers) 
    response = urllib2.urlopen(req)
    result = response.read()

    r = ['Possible Injury scale', 'Evident Injury scale', 'Disabling Injury scale', 'Killed scale', 'Safe']

    return int(result[-3])


#    return json.dumps(weatherList)
  #  return data

#    return jsonify(data) 

@app.route('/')
def home():  # pragma: no cover
#    content = get_file('index.html')
    return render_template('index.html', title='index')


if __name__ == '__main__':
    app.run(host='localhost',port=80, debug=True)
