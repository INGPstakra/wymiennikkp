"""
The flask application package.
"""

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
app.mulbydif=1000000
app.Tr=20;
print(['Tryb testowy',app.test])
import KPSSw0.views
