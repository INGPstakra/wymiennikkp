"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.TZCO=0
app.TZM=0
app.TZCO0=0
app.FZM=0
app.TPM=0
app.TPCO=0
app.TPCO0=0
app.FZCO=0
app.value=1

app.simstart=False
app.test=True
if app.test:
    app.Tr=0;
import KPSSw0.views
