# lab10-dockerfile-build

Lab 1 - Building applications from Dockerfile

## Files

All files required for this lab are stored directly in this directory or in /vagrant/lab10-dockerfile-build directory of your vagrant machine

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab10-dockerfile-build on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab10-dockerfile-build
```

- Create a new project named "lab10"

```
oc new-project lab10
```

## Building a python application from Dockerfile

- Check an example application at https://github.com/li9com/tornadoapp

- Build the application with custom name

```
[vagrant@openshift ~]$ oc new-app --name demo https://github.com/li9com/tornadoapp
--> Found image f00aae8 (46 hours old) in image stream "openshift/python" under tag "3.6" for "python"

    Python 3.6
    ----------
    Python 3.6 available as container is a base platform for building and running various Python 3.6 applications and frameworks. Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python's elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms.

    Tags: builder, python, python36, rh-python36

    * A Docker build using source code from https://github.com/li9com/tornadoapp will be created
      * The resulting image will be pushed to image stream tag "demo:latest"
      * Use 'start-build' to trigger a new build
    * This image will be deployed in deployment config "demo"
    * Port 8888/tcp will be load balanced by service "demo"
      * Other containers can access this service through the hostname "demo"

--> Creating resources ...
    imagestream.image.openshift.io "demo" created
    buildconfig.build.openshift.io "demo" created
    deploymentconfig.apps.openshift.io "demo" created
    service "demo" created
--> Success
    Build scheduled, use 'oc logs -f bc/demo' to track its progress.
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/demo'
    Run 'oc status' to view your app.
```

- Make sure that pod status is changed and application is built

```
[vagrant@openshift ~]$ oc get pod
NAME           READY     STATUS     RESTARTS   AGE
demo-1-build   0/1       Init:0/2   0          3s


[vagrant@openshift ~]$ oc get pod
NAME           READY     STATUS    RESTARTS   AGE
demo-1-build   1/1       Running   0          11s
```

- Check the build log

```
[vagrant@openshift ~]$ oc logs -f bc/demo
Cloning "https://github.com/li9com/tornadoapp" ...
	Commit:	ec4fd8bde7f23c7eb86c89106e4c24db3bcf5c34 (Update README.md)
	Author:	Artemii Kropachev <artem.kropachev@gmail.com>
	Date:	Sat Dec 8 12:30:12 2018 -0500
Replaced Dockerfile FROM image python
Pulling image 172.30.1.1:5000/openshift/python@sha256:db33a65b95899b1cd57a7f698a4ff56fd9a1a8674965f25d09027680b5b0a641 ...
Pulled 2/9 layers, 22% complete
Pulled 3/9 layers, 33% complete
Pulled 4/9 layers, 45% complete
Pulled 5/9 layers, 59% complete
Pulled 6/9 layers, 72% complete
Pulled 7/9 layers, 86% complete
Pulled 8/9 layers, 95% complete
Pulled 9/9 layers, 100% complete
Extracting
Step 1/7 : FROM 172.30.1.1:5000/openshift/python@sha256:db33a65b95899b1cd57a7f698a4ff56fd9a1a8674965f25d09027680b5b0a641
 ---> f00aae81431e
Step 2/7 : COPY ./app /home
 ---> aa82726797d1
Removing intermediate container c0cab0a10086
Step 3/7 : EXPOSE 8888
 ---> Running in fc8865800a91
 ---> b98f5402cb36
Removing intermediate container fc8865800a91
Step 4/7 : RUN pip3 install tornado
 ---> Running in 7d0b7bb684dd
Collecting tornado
  Downloading https://files.pythonhosted.org/packages/e6/78/6e7b5af12c12bdf38ca9bfe863fcaf53dc10430a312d0324e76c1e5ca426/tornado-5.1.1.tar.gz (516kB)
Installing collected packages: tornado
  Running setup.py install for tornado: started
    Running setup.py install for tornado: finished with status 'done'
Successfully installed tornado-5.1.1
You are using pip version 9.0.1, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
 ---> a9a7421e6809
Removing intermediate container 7d0b7bb684dd
Step 5/7 : CMD python /home/app.py
 ---> Running in 631b26b2843e
 ---> fdffc8ff8429
Removing intermediate container 631b26b2843e
Step 6/7 : ENV "OPENSHIFT_BUILD_NAME" "demo-1" "OPENSHIFT_BUILD_NAMESPACE" "lab10" "OPENSHIFT_BUILD_SOURCE" "https://github.com/li9com/tornadoapp" "OPENSHIFT_BUILD_COMMIT" "ec4fd8bde7f23c7eb86c89106e4c24db3bcf5c34"
 ---> Running in ea394e89dd0b
 ---> 3d02a1c2d59e
Removing intermediate container ea394e89dd0b
Step 7/7 : LABEL "io.openshift.build.commit.author" "Artemii Kropachev \u003cartem.kropachev@gmail.com\u003e" "io.openshift.build.commit.date" "Sat Dec 8 12:30:12 2018 -0500" "io.openshift.build.commit.id" "ec4fd8bde7f23c7eb86c89106e4c24db3bcf5c34" "io.openshift.build.commit.message" "Update README.md" "io.openshift.build.commit.ref" "master" "io.openshift.build.name" "demo-1" "io.openshift.build.namespace" "lab10" "io.openshift.build.source-location" "https://github.com/li9com/tornadoapp"
 ---> Running in 761124ea7daa
 ---> 00cdd0bdc53c
Removing intermediate container 761124ea7daa
Successfully built 00cdd0bdc53c
Pushing image 172.30.1.1:5000/lab10/demo:latest ...
Pushed 0/11 layers, 6% complete
Pushed 1/11 layers, 12% complete
Pushed 2/11 layers, 18% complete
```

Note! You need to wait until build is fisnished


- Check the status of pods

```
vagrant@openshift ~]$ oc get pod
NAME           READY     STATUS      RESTARTS   AGE
demo-1-build   0/1       Completed   0          1m
demo-1-wfzws   1/1       Running     0          14s
```

Note! Application has been built!

- Check all resources created by "oc new-app"

```
[vagrant@openshift ~]$ oc get all
NAME               READY     STATUS      RESTARTS   AGE
pod/demo-1-build   0/1       Completed   0          2m
pod/demo-1-wfzws   1/1       Running     0          48s

NAME                           DESIRED   CURRENT   READY     AGE
replicationcontroller/demo-1   1         1         1         49s

NAME           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/demo   ClusterIP   172.30.88.40   <none>        8888/TCP   2m

NAME                                      REVISION   DESIRED   CURRENT   TRIGGERED BY
deploymentconfig.apps.openshift.io/demo   1          1         1         config,image(demo:latest)

NAME                                  TYPE      FROM      LATEST
buildconfig.build.openshift.io/demo   Docker    Git       1

NAME                              TYPE      FROM          STATUS     STARTED         DURATION
build.build.openshift.io/demo-1   Docker    Git@ec4fd8b   Complete   2 minutes ago   1m22s

NAME                                  DOCKER REPO                  TAGS      UPDATED
imagestream.image.openshift.io/demo   172.30.1.1:5000/lab10/demo   latest    50 seconds ago
```

- Show build config details

```
[vagrant@openshift ~]$ oc get build
NAME      TYPE      FROM          STATUS     STARTED         DURATION
demo-1    Docker    Git@ec4fd8b   Complete   2 minutes ago   1m22s
[vagrant@openshift ~]$ oc get bc
NAME      TYPE      FROM      LATEST
demo      Docker    Git       1
[vagrant@openshift ~]$ oc describe bc demo
Name:		demo
Namespace:	lab10
Created:	3 minutes ago
Labels:		app=demo
Annotations:	openshift.io/generated-by=OpenShiftNewApp
Latest Version:	1

Strategy:	Docker
URL:		https://github.com/li9com/tornadoapp
From Image:	ImageStreamTag openshift/python:3.6
Output to:	ImageStreamTag demo:latest

Build Run Policy:	Serial
Triggered by:		Config, ImageChange
Webhook Generic:
	URL:		https://localhost:8443/apis/build.openshift.io/v1/namespaces/lab10/buildconfigs/demo/webhooks/<secret>/generic
	AllowEnv:	false
Webhook GitHub:
	URL:	https://localhost:8443/apis/build.openshift.io/v1/namespaces/lab10/buildconfigs/demo/webhooks/<secret>/github
Builds History Limit:
	Successful:	5
	Failed:		5

Build	Status		Duration	Creation Time
demo-1 	complete 	1m22s 		2018-12-09 17:46:31 +0000 UTC

Events:	<none>
```

- Expose the demo application and make sure that it works

```
[vagrant@openshift ~]$ oc get svc
NAME      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
demo      ClusterIP   172.30.88.40   <none>        8888/TCP   4m


[vagrant@openshift ~]$ oc expose svc demo
route.route.openshift.io/demo exposed


[vagrant@openshift ~]$ oc get route
NAME      HOST/PORT                            PATH      SERVICES   PORT       TERMINATION   WILDCARD
demo      demo-lab10.apps.172.24.0.11.nip.io             demo       8888-tcp                 None
[vagrant@openshift ~]$ curl demo-lab10.apps.172.24.0.11.nip.io
This is an example Python applicaiton
It is running on demo-1-wfzws
Current time is 2018-12-09 17:51:38.449414
```

## Cleanup

```
oc delete project lab10
```




