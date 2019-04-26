# Lab. Using S2I tool

This lab demonstrates usage of __S2I__ tool.

## Prerequisites

* The lab should be done on a linux host with running _docker_ service.
* A Docker registry should exist and the client should be able to pull and push images from/to it.

* ___S2I___ tool should be downloaded and put into _$HOME_ directory:

```
$ curl -sLo - https://github.com/openshift/source-to-image/releases/download/v1.1.13/source-to-image-v1.1.13-b54d75d3-linux-amd64.tar.gz | tar -C $HOME -xzf -
$ ls -l $HOME/s2i
-rwxr-xr-x. 1 demo demo 7271680 Dec 11 18:26 /home/demo/s2i
```

* Copy all files from this directory to $HOME/lab-s2i-tool


Perform all further actions in __$HOME/lab-s2i-tool__ directory.


## Phase 1: Preparing S2I scripts


Make sure that all scripts in _s2i/bin_ directory has the execute bit enabled (`chmod a+x s2i/bin/*`).

### Script s2i/bin/run

This script is executed to run the application.

```bash
$ cat s2i/bin/run
#!/bin/bash

FLASK_APP=main.py flask run --debugger -h 0.0.0.0 -p $LISTEN_PORT

exit 0
```

### Script s2i/bin/assemble

This script is executed when the image on the second stage - building an app image. The current context is  __app/__ directory as it will be used in __s2i build__ command below, so all files should be referenced inside this directory.

```bash
#!/bin/bash

install -m 0644 main.py /app/main.py

exit 0
```

### Script s2i/bin/usage

This script shows the basic information on how to use this image. Put all needed information here to tell this.
Check the __Dockerfile__ below to see how the script is called.

```bash
$ cat s2i/bin/usage
#!/bin/bash

cat << EOF

Usage:
  Put the sources of your Flask application into /app directory.
  File main.py must exist as /app/main.py. This is an entry point
  to your app.
EOF

exit 0
```

### Script s2i/bin/save-artifacts

Use this script if you need to save some artifacts between builds. Later they can be used repeatedly in the __assemble__ script to speed up new roll outs.

```bash
#!/bin/bash

exit 0
```


### File app/requirements.txt

This file includes dependencies needed for the __Flask__ applications. Those dependencies will be installed by calling in the __Dockerfile__.

```
Flask==1.0.2
```

### Dockerfile

```dockerfile
FROM        python:3
LABEL       maintainer.name="Dmitrii Mostovshchikov" \
            maintainer.email="Dmitrii.Mostovshchikov@li9.com" \
            maintainer.company="Li9, Inc." \
            company.website="https://www.li9.com" \
            s2i.app="flask" \
            io.openshift.s2i.scripts-url="image:///usr/libexec/s2i"
ENV         LISTEN_PORT 9000
USER        1001
WORKDIR     /app

ADD         ./s2i/bin /usr/libexec/s2i
ADD         ./app/requirements.txt .
RUN         pip install --no-cache-dir -r requirements.txt

EXPOSE      ${LISTEN_PORT}/tcp

CMD         [ "/usr/libexec/s2i/usage" ]
```

The __Dockerfile__ should have the label `io.openshift.s2i.scripts-url="image:///usr/libexec/s2i"` which indicates where S2I scrips are located.

## Application

The application consists of a single python file which runs some functions as __Flask__ application.

```
$ cat app/main.py
```

```python
#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello(): return "Hello, World!"

@app.route("/ping")
def ping(): return "Pong"

@app.route("/healthz")
def healthz(): return "ok"
```


## Phase 2: Building the building image

Now we are ready to create an __SI2 image__.

* Build the image __frontend-s2i__

```
$ sudo docker build . --tag frontend-s2i
Sending build context to Docker daemon 17.92 kB
Step 1/9 : FROM python:3
Trying to pull repository docker-registry.default.svc:5000/python ...
Trying to pull repository registry.access.redhat.com/python ...
Pulling repository registry.access.redhat.com/python
Trying to pull repository docker.io/library/python ...
3: Pulling from docker.io/library/python
e79bb959ec00: Pull complete
d4b7902036fe: Pull complete
1b2a72d4e030: Pull complete
d54db43011fd: Pull complete
69d473365bb3: Pull complete
7dc3a6a0e509: Pull complete
68cd774d0852: Pull complete
2ef86095a118: Pull complete
bd9da5a171e0: Pull complete
Digest: sha256:67a2befe73bf0233d066496f40297602fcf288858641cc8843fb5224a2b29339
Status: Downloaded newer image for docker.io/python:3
 ---> 954987809e63
Step 2/9 : LABEL maintainer.name "Dmitrii Mostovshchikov" maintainer.email "Dmitrii.Mostovshchikov@li9.com" maintainer.company "Li9, Inc." company.website "https://www.li9.com" s2i.app "flask" io.openshift.s2i.scripts-url "image:///usr/libexec/s2i"
 ---> Running in a8f30690132d
 ---> 77f738bda494
Removing intermediate container a8f30690132d
Step 3/9 : ENV LISTEN_PORT 9000
 ---> Running in 7a4b6484de3d
 ---> e7d175a11603
Removing intermediate container 7a4b6484de3d
Step 4/9 : WORKDIR /app
 ---> a71a4b301d5a
Removing intermediate container 4e4963936832
Step 5/9 : ADD ./s2i/bin /usr/libexec/s2i
 ---> cb2dd1462d85
Removing intermediate container 554367c9d867
Step 6/9 : ADD ./app .
 ---> a79a3146e80e
Removing intermediate container 7b6c419f5b52
Step 7/9 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in 240d6ac34840

Collecting Flask==1.0.2 (from -r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/7f/e7/08578774ed4536d3242b14dacb4696386634607af824ea997202cd0edb4b/Flask-1.0.2-py2.py3-none-any.whl (91kB)
Collecting click>=5.1 (from Flask==1.0.2->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/fa/37/45185cb5abbc30d7257104c434fe0b07e5a195a6847506c074527aa599ec/Click-7.0-py2.py3-none-any.whl (81kB)
Collecting itsdangerous>=0.24 (from Flask==1.0.2->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/76/ae/44b03b253d6fade317f32c24d100b3b35c2239807046a4c953c7b89fa49e/itsdangerous-1.1.0-py2.py3-none-any.whl
Collecting Jinja2>=2.10 (from Flask==1.0.2->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/1d/e7/fd8b501e7a6dfe492a433deb7b9d833d39ca74916fa8bc63dd1a4947a671/Jinja2-2.10.1-py2.py3-none-any.whl (124kB)
Collecting Werkzeug>=0.14 (from Flask==1.0.2->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/18/79/84f02539cc181cdbf5ff5a41b9f52cae870b6f632767e43ba6ac70132e92/Werkzeug-0.15.2-py2.py3-none-any.whl (328kB)
Collecting MarkupSafe>=0.23 (from Jinja2>=2.10->Flask==1.0.2->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/98/7b/ff284bd8c80654e471b769062a9b43cc5d03e7a615048d96f4619df8d420/MarkupSafe-1.1.1-cp37-cp37m-manylinux1_x86_64.whl
Installing collected packages: click, itsdangerous, MarkupSafe, Jinja2, Werkzeug, Flask
Successfully installed Flask-1.0.2 Jinja2-2.10.1 MarkupSafe-1.1.1 Werkzeug-0.15.2 click-7.0 itsdangerous-1.1.0
 ---> 2a5e76c2c5df
Removing intermediate container 240d6ac34840
Step 8/9 : EXPOSE ${LISTEN_PORT}/tcp
 ---> Running in 59228bd354ec
 ---> 8dffcffd2c68
Removing intermediate container 59228bd354ec
Step 9/9 : CMD /usr/libexec/s2i/usage
 ---> Running in 574c0f063850
 ---> 2270a302fef7
Removing intermediate container 574c0f063850
Successfully built 2270a302fef7
```

* Check the built image

```
$ sudo docker images | grep frontend-s2i
frontend-s2i                                                     latest              2270a302fef7        57 seconds ago      938 MB
```

## Phase 3. Building the app-ready image

```
$ sudo $HOME/s2i build [--loglevel=5] app/ frontend-s2i frontend-app
Build completed successfully
```

After this action the final image ___frontend-app___ is ready for running applications from.

## Verification

* Run an application container from the app image.

```
$ sudo docker run -d --name frontend -p 9000:9000/tcp frontend-app
```

* And check that the application is responding on the requests

```
$ for  url in / /ping /healthz; do curl 127.0.0.1:9000${url}; echo; done
Hello, World!
Pong
ok
```

## Authors

- Dmitrii Mostovshchikov <Dmitrii.Mostovshchikov@li9.com>

