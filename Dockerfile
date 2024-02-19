FROM python:3

WORKDIR /home/py

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/py

#CMD [ "python", "server.py" ]