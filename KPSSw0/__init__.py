"""
The flask application package.
"""
import threading
import requests
import json
from flask import Flask
app = Flask(__name__)
app.TZCO=15
app.TZM=100
app.TZCO0=15
app.FZM=100
app.TPM=100
app.TPCO=15
app.TPCO0=15
app.FZCO=0
app.value=1
app.simthread=None
app.sendthread=None
app.value1=1
app.timeout=0.5
app.log=True
app.test=False
app.simbud=False
app.mulbydif=100000000
app.Tr=20;
print(['Tryb testowy',app.test])
import KPSSw0.views

def sim():
    while True:
        timeurl='https://closingtime.szyszki.de/api/details'
        try:
            print('Try get speed')
            time=json.loads(requests.get(timeurl, timeout=0.5).content)
            app.mulbydif=time['speed']*100000
        except:
            pass
        KPSSw0.views.runsim()

app.simthread = threading.Thread(target=sim)
app.simthread.start()




