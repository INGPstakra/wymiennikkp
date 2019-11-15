FROM python:3.7-buster
WORKDIR /

ADD ./runserver.py ./runserver.py
ADD ./KPSSw0 ./KPSSw0

RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install flask
RUN pip3 install requests

EXPOSE 5000

CMD env FLASK_APP=runserver.py flask run --host=0.0.0.0