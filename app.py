from flask import Flask,request
from skyfield.api import load
from skyfield.api import N,S,E,W, wgs84
import pytz
from datetime import datetime

eph = load('de421.bsp')
ts = load.timescale()

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def index():
       tz = pytz.timezone('Asia/Kolkata')

       if(request.method == 'POST'):
           
            if((request.form.get('date') != "") & (request.form.get('time') != "")):
               time_submitted = tz.localize(datetime.strptime(request.form['date']+"-"+request.form['time'], "%Y-%m-%d-%H:%M"))
               time = ts.utc(time_submitted)
               T = time
       else:
            T = ts.now()
        
       T_local = T.astimezone(tz).strftime(format='%Y-%m-%d %H:%M:%S ')
       T_UTC = T.utc_strftime(format='%Y-%m-%d %H:%M:%S ')
       T_JD = ts.J(T.J).tt
        
       Earth = eph['earth']
       Observer = Earth + wgs84.latlon(42.3583 * N, 71.0603 * W, elevation_m=43)
       Bodies = ['sun','mercury','venus','mars','jupiter','saturn','uranus','neptune','pluto']
       Objects = [Observer.at(T).observe(eph[(i + " barycenter" if i != "sun" else "sun")]) for i in Bodies]
        
        
       parse = lambda x: [ x[0]._degrees, x[1].degrees,x[2].au]
       radec = [parse(i.radec()) for i in Objects]
       hadec = [parse(i.hadec()) for i in Objects]
       altaz = [[j.degrees for j in i.apparent().altaz()[:-1]] for i in Objects]    
        
       parameters = ['Ra','Dec','Distance','Ha','alt','az']    

       data = [dict(zip(parameters,i + j[:1] + k)) for i,j,k in zip(radec,hadec,altaz)]

            
        
       return  {
                'local time': T_local,
                'UTC time': T_UTC,
                "JD": T_JD,
                "Astronomical Bodies": dict(zip(Bodies,data))
            }
    # the code below is executed if the request method
    # was GET or the credentials were invalid

