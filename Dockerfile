FROM python:3.8-slim
MAINTAINER Mark Vander Stel <mvndrstl@gmail.com>

COPY requirements.txt /tmp/

RUN pip install --requirement /tmp/requirements.txt

ENV SE_API_ENDPOINT=9533eeca.compilers.sphere-engine.com \
    DEBUG=False

COPY . /app
WORKDIR /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD [ "python", "run.py" ]
