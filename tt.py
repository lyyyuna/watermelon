from gevent import monkey; monkey.patch_all()
from bottle111 import *
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time
import os


import threading

ii = 1


@route('/css/<filename:re:.*\.css>')
def send_css(filename):
    print 'dsdsfsdfsdfsfsdfsfs'
    return static_file(filename, root='static/css');
    
@route('/js/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='static/js');    

@route('/image/<filename:re:.*\.png>')
def send_png(filename):
    return static_file111(filename, root='static/image');    





@route('/')
def index():
    global ii
    return template('index_template', name=ii)

@route('/history')
def history():
    # n=20
    # duration=100
    # now=time.mktime(time.localtime())
    # timestamps=np.linspace(now,now+duration,n)
    # dates=[dt.datetime.fromtimestamp(ts) for ts in timestamps]
    global q
    dates = [dt.datetime.fromtimestamp(ts) for nongdu, ts in q]
    datenums = md.date2num(dates)
    values = [nongdu for nongdu, ts in q]
    
    plt.subplots_adjust(bottom=0.2)
    plt.xticks( rotation=25 )
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(datenums,values)
    
    os.remove('static/image/history.png')
    plt.savefig('static/image/history.png')
    plt.clf()
    return template('history_template')
    
@route('/about')    
def about():
    return template('about_template')
    

@route('/t')  
def fun():
    global ii
    global q
    ii = int(request.query.id)
    now = time.mktime(time.localtime())
    q.pop()
    q.insert(0, [ii, now])
    # print q
 
def worker1():
    global ii
    while True:
        time.sleep(1)
        ii = ii + 1 
t = threading.Thread(target = worker1)
t.start()


global q
q = []
for i in range(1, 60):
    now=time.mktime(time.localtime())
    q.append([i, now])

    

run(server='gevent', host='0.0.0.0', port=80, debug=True)
