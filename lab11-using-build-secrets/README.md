# lab11-using-build-secrets
Lab 1 - Building applications from Dockerfile

## Files
All files required for this lab are stored directly in this directory or in /vagrant/lab11-using-build-secrets directory of your vagrant machine

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab11-using-build-secrets on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab11-using-build-secrets
```

- Create a new project named "lab11"

```
oc new-project lab11
```

## Building applications from a private GIT repository

- Try to build the demo application from a private repository

```
[vagrant@openshift lab11-using-build-secrets]$ oc new-app http://gitlab.demo.li9.com/root/tornadoapp.git
Username for 'http://gitlab.demo.li9.com': student
Password for 'http://student@gitlab.demo.li9.com':
Username for 'http://gitlab.demo.li9.com': student
Password for 'http://student@gitlab.demo.li9.com':
warning: Cannot check if git requires authentication.
--> Found image f00aae8 (46 hours old) in image stream "openshift/python" under tag "3.6" for "python"

    Python 3.6
    ----------
    Python 3.6 available as container is a base platform for building and running various Python 3.6 applications and frameworks. Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python's elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms.

    Tags: builder, python, python36, rh-python36

    * A Docker build using source code from http://gitlab.demo.li9.com/root/tornadoapp.git will be created
      * The resulting image will be pushed to image stream tag "tornadoapp:latest"
      * Use 'start-build' to trigger a new build
      * WARNING: this source repository may require credentials.
                 Create a secret with your git credentials and use 'set build-secret' to assign it to the build config.
    * This image will be deployed in deployment config "tornadoapp"
    * Port 8888/tcp will be load balanced by service "tornadoapp"
      * Other containers can access this service through the hostname "tornadoapp"

--> Creating resources ...
    imagestream.image.openshift.io "tornadoapp" created
    buildconfig.build.openshift.io "tornadoapp" created
    deploymentconfig.apps.openshift.io "tornadoapp" created
    service "tornadoapp" created
--> Success
    Build scheduled, use 'oc logs -f bc/tornadoapp' to track its progress.
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/tornadoapp'
    Run 'oc status' to view your app.
```

- Verify build status

```
[vagrant@openshift lab11-using-build-secrets]$ oc get pod
NAME                 READY     STATUS       RESTARTS   AGE
tornadoapp-1-build   0/1       Init:Error   0          30s


[vagrant@openshift lab11-using-build-secrets]$ oc logs -f bc/tornadoapp
Cloning "http://gitlab.demo.li9.com/root/tornadoapp.git" ...
error: failed to fetch requested repository "http://gitlab.demo.li9.com/root/tornadoapp.git" with provided credentials
```

Note! it is expected that application fails


- Create a secret

```
oc create secret generic gitlab-student-access \
    --from-literal=username=student \
    --from-literal=password=PASSWORD
```

Note! ask for  PASWORD

You will see the following

```
secret/gitlab-student-access created
```

Note! ask for PASSWORD

- Attach secret as a build secret to the build resources

```
[vagrant@openshift lab11-using-build-secrets]$ oc set build-secret --source bc/tornadoapp gitlab-student-access
buildconfig.build.openshift.io/tornadoapp secret updated


[vagrant@openshift lab11-using-build-secrets]$ oc get secret
NAME                       TYPE                                  DATA      AGE
builder-dockercfg-grsgp    kubernetes.io/dockercfg               1         9m
builder-token-4jhsv        kubernetes.io/service-account-token   4         9m
builder-token-tvqp5        kubernetes.io/service-account-token   4         9m
default-dockercfg-lnlsl    kubernetes.io/dockercfg               1         9m
default-token-7kshk        kubernetes.io/service-account-token   4         9m
default-token-jqmbk        kubernetes.io/service-account-token   4         9m
deployer-dockercfg-7z9mf   kubernetes.io/dockercfg               1         9m
deployer-token-4qvhv       kubernetes.io/service-account-token   4         9m
deployer-token-cwz5r       kubernetes.io/service-account-token   4         9m
gitlab-student-access      Opaque                                2         1m

```

- Restart the build

```
[vagrant@openshift lab11-using-build-secrets]$ oc get build
NAME           TYPE      FROM      STATUS                       STARTED         DURATION
tornadoapp-1   Docker    Git       Failed (FetchSourceFailed)   5 minutes ago   1s

[vagrant@openshift lab11-using-build-secrets]$ oc get bc
NAME         TYPE      FROM      LATEST
tornadoapp   Docker    Git       1

[vagrant@openshift lab11-using-build-secrets]$ oc start-build tornadoapp
build.build.openshift.io/tornadoapp-2 started


[vagrant@openshift lab11-using-build-secrets]$ oc get build
NAME           TYPE      FROM      STATUS                       STARTED         DURATION
tornadoapp-1   Docker    Git       Failed (FetchSourceFailed)   5 minutes ago   1s
tornadoapp-2   Docker    Git       Running                      2 seconds ago

```

- Check the build logs

```
[vagrant@openshift lab11-using-build-secrets]$ oc logs -f bc/tornadoapp
Cloning "http://gitlab.demo.li9.com/root/tornadoapp.git" ...
	Commit:	6a5e3d12d9c9d46c88bbb2af74c470d9848c77f6 (Add new file)
	Author:	Administrator <admin@example.com>
	Date:	Sun Dec 9 02:47:46 2018 +0000
Replaced Dockerfile FROM image python
Step 1/7 : FROM 172.30.1.1:5000/openshift/python@sha256:db33a65b95899b1cd57a7f698a4ff56fd9a1a8674965f25d09027680b5b0a641
 ---> f00aae81431e
Step 2/7 : COPY ./app /home
 ---> 17548c740fd5
Removing intermediate container 94a8491dc438
Step 3/7 : EXPOSE 8888
 ---> Running in 3b3b768abc6e
 ---> c39cef4e72f1
Removing intermediate container 3b3b768abc6e
Step 4/7 : RUN pip3 install tornado
 ---> Running in a063374c6ad2
Collecting tornado
  Downloading https://files.pythonhosted.org/packages/e6/78/6e7b5af12c12bdf38ca9bfe863fcaf53dc10430a312d0324e76c1e5ca426/tornado-5.1.1.tar.gz (516kB)
Installing collected packages: tornado
  Running setup.py install for tornado: started
    Running setup.py install for tornado: finished with status 'done'
Successfully installed tornado-5.1.1
You are using pip version 9.0.1, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
 ---> 00c8033ee7b2
Removing intermediate container a063374c6ad2
Step 5/7 : CMD python /home/app.py
 ---> Running in da5d57cfe568
 ---> da489b6def02
Removing intermediate container da5d57cfe568
Step 6/7 : ENV "OPENSHIFT_BUILD_NAME" "tornadoapp-2" "OPENSHIFT_BUILD_NAMESPACE" "lab11" "OPENSHIFT_BUILD_SOURCE" "http://gitlab.demo.li9.com/root/tornadoapp.git" "OPENSHIFT_BUILD_COMMIT" "6a5e3d12d9c9d46c88bbb2af74c470d9848c77f6"
 ---> Running in 2af4eb961d7c
 ---> 4543fffc7aa2
Removing intermediate container 2af4eb961d7c
Step 7/7 : LABEL "io.openshift.build.commit.author" "Administrator \u003cadmin@example.com\u003e" "io.openshift.build.commit.date" "Sun Dec 9 02:47:46 2018 +0000" "io.openshift.build.commit.id" "6a5e3d12d9c9d46c88bbb2af74c470d9848c77f6" "io.openshift.build.commit.message" "Add new file" "io.openshift.build.commit.ref" "master" "io.openshift.build.name" "tornadoapp-2" "io.openshift.build.namespace" "lab11"
 ---> Running in d4d06ab2ff22
 ---> 1128e5688930
Removing intermediate container d4d06ab2ff22
Successfully built 1128e5688930
Pushing image 172.30.1.1:5000/lab11/tornadoapp:latest ...
Pushed 0/11 layers, 6% complete
Pushed 1/11 layers, 27% complete
Pushed 2/11 layers, 36% complete
Pushed 3/11 layers, 36% complete
Pushed 4/11 layers, 36% complete
Pushed 5/11 layers, 45% complete
Pushed 6/11 layers, 55% complete
Push successful
```

- Expose the application and make sure that it frameworks

```
[vagrant@openshift lab11-using-build-secrets]$ oc expose svc tornadoapp
route.route.openshift.io/tornadoapp exposed

[vagrant@openshift lab11-using-build-secrets]$ oc get route
NAME         HOST/PORT                                  PATH      SERVICES     PORT       TERMINATION   WILDCARD
tornadoapp   tornadoapp-lab11.apps.172.24.0.11.nip.io             tornadoapp   8888-tcp                 None

[vagrant@openshift lab11-using-build-secrets]$ curl tornadoapp-lab11.apps.172.24.0.11.nip.io
This is an example Python applicaiton
It is running on tornadoapp-1-nspk6
Current time is 2018-12-09 18:10:18.351095
```


## Cleanup

```
oc delete project lab11
```
