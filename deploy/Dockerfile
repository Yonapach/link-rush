FROM python:3.11
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update && apt-get purge -y --auto-remove

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt