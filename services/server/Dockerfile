FROM python:3.7.5-slim

# set working directory
WORKDIR /usr/src/app

RUN apt update -y 
RUN python3 -m pip install --user --upgrade pip

RUN rm /etc/ssl/openssl.cnf
COPY openssl.cnf /etc/ssl

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

#add and install requirements
#COPY ./requirements.txt /usr/src/app/requirements.txt


#RUN apt-get update \
#    && apt-get install -y --no-install-recommends \
#        postgresql-client \
#    && rm -rf /var/lib/apt/lists/*

#RUN pip install -r requirements.txt

# install dependencies
#RUN apt-get update -y && \
#    apt-get install  gcc g++ musl-dev libpq-dev -y && \
#    python3 -m pip install --upgrade pip && \
#    python3 -m pip install -r requirements.txt --no-cache-dir


#RUN apt update -y && \
#	apt install python3-pip -y && \
#	pip3 install -r requirements.txt --no-cache-dir


# add app
COPY . /usr/src/app

# migrate database
#RUN python3 manage.py makemigrations && \
#   python3 manage.py migrate

# run server
# CMD
