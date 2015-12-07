FROM ubuntu:14.04
EXPOSE 8000
RUN apt-get update
RUN apt-get install python-pip python-dev libpq-dev -y
COPY . .
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD gunicorn manage:app -b 0.0.0.0 -D
