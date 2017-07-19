# Part 1: Build Docker and run gunicorn

##  1.1: Start a web service to predict

### 1.1.1 Create environment
#### Install Python 3.5.3 on Ubuntu & Linuxmint

1. Install Required Packages

```sh
sudo apt-get install build-essential checkinstall

sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```
2. Download Python 3.5.3

```sh
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.5.3/Python-3.5.3.tgz
sudo tar xzf Python-3.5.3.tgz
cd Python-3.5.3
```

3. install

```
sudo ./configure
sudo make altinstall
python3.5 -V
```

#### create virtualenv with python3.5

```
$ which python3.5
/usr/local/bin/python3.5
$ virtualenv --python=/usr/local/bin/python3.5 venv
```

### 1.1.2: Add and install requirements.txt


### 1.1.3: create a web app `main.py`

receive content image and send new style image back.


### 1.1.4: create conponents

#### `model.py`

#### `transform.py`

#### add `models.ckpt`

## 1.2: test local
```
python main.py
```
```
(echo -n '{"data": "'; base64 doggy.jpg; echo '"}') | curl -X POST -H "Content-Type: application/json" -d @- http://35.197.11.221:8080
```

## 1.3 supervisor, nginx and gunicon
make it more robust

## 1.4 Dockerfile
**py35-temp:latest** 
```
FROM ubuntu:latest
MAINTAINER qian <liu.qian.am@gmail.com>

RUN apt-get update && \
    apt-get install -y \
                    wget \
                    xz-utils \
                    build-essential \
                    libsqlite3-dev \
                    libreadline-dev \
                    libssl-dev \
                    openssl

WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.5.3/Python-3.5.3.tar.xz
RUN tar -xf Python-3.5.3.tar.xz
WORKDIR /tmp/Python-3.5.3
RUN ./configure
RUN make
RUN make install


WORKDIR /
RUN rm -rf /tmp/Python-3.5.3.tar.xz /tmp/Python-3.5.3
```
**py353:latest**
```
FROM py35-temp:latest

# Update python, Install virtualenv, nginx, supervisor
RUN apt-get update --fix-missing  \
        && apt-get install -y build-essential git \
        && apt-get install -y python python-dev python-setuptools \
        && apt-get install -y python-pip python-virtualenv \
        && apt-get install -y nginx supervisor


RUN service supervisor stop \
        && service nginx stop

RUN pip install supervisor-stdout

# create virtual env and install dependencies
RUN virtualenv --python=/usr/local/bin/python3.5 /opt/venv
```
**venv:v1**
```
FROM py353:latest
# create virtual env and install dependencies
ADD ./requirements.txt /opt/venv/requirements.txt
RUN /opt/venv/bin/pip install -r /opt/venv/requirements.txt
```

**venv:latest**

```
FROM venv:v1

# Add our config files
ADD ./supervisor.conf /etc/supervisor.conf
ADD ./nginx.conf /etc/nginx/nginx.conf
# expose port
EXPOSE 8080 9001
```

**transervice:latest**

```
FROM venv:latest

# Copy our service code
ADD ./transform-service /opt/transform-service

# start supervisor to run our wsgi server, nginx, supervisor-stdout
CMD supervisord -c /etc/supervisor.conf -n
```

# 1.5 run docker
```
sudo docker run -td -p 8180:8080 -p 9101:9001 transervice
```

# Part 2 : google_app_engine_web_service

## 2.1: enviroment
App engine requires libraries to be installed into a folder for deployment. You’ll download the `Gcloud Storage Client` as well.

```
$ mkdir google_app_engine_web_service
$ cd google_app_engine_web_service
$ git clone https://github.com/GoogleCloudPlatform/appengine-gcs-client.git
$ pip install -r requirements.txt -t lib
$ pip install GoogleAppEngineCloudStorageClient -t lib
```

local run appengine
```
>>> import sys
>>> import google
>>> gae_dir = google.__path__.append('/usr/local/google_appengine/google')
>>> sys.path.insert(0, gae_dir)
>>> import google.appengine
```


## 2.2: `app.yaml` and `appengine_config.py`

app standard version
```
runtime: python27
api_version: 1
threadsafe: true
module: default
handlers:
- url: /.*
  script: main.app
```

## 2.3:`config.py` and `storage.py`
store in bucket (you may need to create one)

`config.py`
```
PROJECT_ID = 'keraspredion'
CLOUD_STORAGE_BUCKET = 'kerasimagebucket'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
PREDICTION_SERVICE_URL = 'http://35.185.255.199:8080'
```



# 2.4: `main.py` and templates


# 2.5: test app


Cloud Shell lets you test your app before deploying to make sure it's running as intended, just like debugging on your local machine.

To test your app enter:
```
dev_appserver.py $PWD
```

# 2.6: deploy
```
gcloud app deploy
```





