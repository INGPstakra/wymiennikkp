"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.TZCO=15
app.TZM=100
app.TZCO0=0
app.FZM=0
app.TPM=0
app.TPCO=0
app.TPCO0=0
app.FZCO=0
app.value=1
app.simthread=None
app.sendthread=None
app.value1=1
app.timeout=0.5
app.log=True
app.test=False
app.simbud=True
app.mulbydif=1000
app.Tr=0;
print(['Tryb testowy',app.test])
import KPSSw0.views
