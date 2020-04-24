FROM python:3.8-slim
MAINTAINER Mark Vander Stel <mvndrstl@gmail.com>

COPY requirements.txt /tmp/

RUN pip install --requirement /tmp/requirements.txt

COPY . /app
WORKDIR /app

CMD [ "python", "run.py" ]
