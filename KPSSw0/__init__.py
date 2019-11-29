"""
The flask application package.
"""
import threading
import requests
import json
from flask import Flask
app = Flask(__name__)
app.TZCO=30
app.TZM=100
app.TZCO0=30
app.FZM=100
app.TPM=100
app.TPCO=30
app.TPCO0=30
app.FZCO=0
app.value=1
app.simthread=None
app.sendthread=None
app.value1=1
app.timeout=1
app.time=0
app.log=True
app.test=False
app.simbud=False
app.mulbydif=2006
app.i=0
app.Tr=20;
print(['Tryb testowy',app.test])
print(['SimBud',app.simbud])
print(['speed',app.mulbydif])
import KPSSw0.views

def sim():
    while True:
        app.i=app.i+1
        KPSSw0.views.runsim()

app.simthread = threading.Thread(target=sim)
app.simthread.start()




