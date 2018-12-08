# lab06-oc-new-app
Lab 6 - Application deployment using "oc new-app"

## Files
All files required for this lab are stored directly in this directory or in /vagrant/lab06-oc-new-app directory of your vagrant machine

## Default routes

The lab installation uses apps.172.24.0.11.nip.io as the default application domain.

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab06-oc-new-app on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab06-oc-new-app
```

- Create a new project named "lab6"

```
oc new-project lab5
```

## oc new-app

- Check builtin "oc new-app -h" documenation

```
[vagrant@openshift lab06-oc-new-app]$ oc new-app --help
Create a new application by specifying source code, templates, and/or images

This command will try to build up the components of an application using images, templates, or code that has a public
repository. It will lookup the images on the local Docker installation (if available), a Docker registry, an integrated
image stream, or stored templates.

If you specify a source code URL, it will set up a build that takes your source code and converts it into an image that
can run inside of a pod. Local source must be in a git repository that has a remote repository that the server can see.
The images will be deployed via a deployment configuration, and a service will be connected to the first public port of
the app. You may either specify components using the various existing flags or let new-app autodetect what kind of
components you have provided.

If you provide source code, a new build will be automatically triggered. You can use 'oc status' to check the progress.

Usage:
  oc new-app (IMAGE | IMAGESTREAM | TEMPLATE | PATH | URL ...) [flags]

Examples:
  # List all local templates and image streams that can be used to create an app
  oc new-app --list

  # Create an application based on the source code in the current git repository (with a public remote)
  # and a Docker image
  oc new-app . --docker-image=repo/langimage

  # Create a Ruby application based on the provided [image]~[source code] combination
  oc new-app centos/ruby-25-centos7~https://github.com/sclorg/ruby-ex.git

  # Use the public Docker Hub MySQL image to create an app. Generated artifacts will be labeled with db=mysql
  oc new-app mysql MYSQL_USER=user MYSQL_PASSWORD=pass MYSQL_DATABASE=testdb -l db=mysql

  # Use a MySQL image in a private registry to create an app and override application artifacts' names
  oc new-app --docker-image=myregistry.com/mycompany/mysql --name=private

  # Create an application from a remote repository using its beta4 branch
  oc new-app https://github.com/openshift/ruby-hello-world#beta4

  # Create an application based on a stored template, explicitly setting a parameter value
  oc new-app --template=ruby-helloworld-sample --param=MYSQL_USER=admin

  # Create an application from a remote repository and specify a context directory
  oc new-app https://github.com/youruser/yourgitrepo --context-dir=src/build

  # Create an application from a remote private repository and specify which existing secret to use
  oc new-app https://github.com/youruser/yourgitrepo --source-secret=yoursecret

  # Create an application based on a template file, explicitly setting a parameter value
  oc new-app --file=./example/myapp/template.json --param=MYSQL_USER=admin

  # Search all templates, image streams, and Docker images for the ones that match "ruby"
  oc new-app --search ruby

  # Search for "ruby", but only in stored templates (--template, --image-stream and --docker-image
  # can be used to filter search results)
  oc new-app --search --template=ruby

  # Search for "ruby" in stored templates and print the output as an YAML
  oc new-app --search --template=ruby --output=yaml

Options:
      --allow-missing-images=false: If true, indicates that referenced Docker images that cannot be found locally or in
a registry should still be used.
      --allow-missing-imagestream-tags=false: If true, indicates that image stream tags that don't exist should still be
used.
      --allow-missing-template-keys=false: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --as-test=false: If true create this application as a test deployment, which validates that the deployment
succeeds and then scales down.
      --build-env=[]: Specify a key-value pair for an environment variable to set into each build image.
      --build-env-file=[]: File containing key-value pairs of environment variables to set into each build image.
      --code=[]: Source code to use to build this application.
      --context-dir='': Context directory to be used for the build.
      --docker-image=[]: Name of a Docker image to include in the app.
      --dry-run=false: If true, show the result of the operation without performing it.
  -e, --env=[]: Specify a key-value pair for an environment variable to set into each container.
      --env-file=[]: File containing key-value pairs of environment variables to set into each container.
  -f, --file=[]: Path to a template file to use for the app.
      --grant-install-rights=false: If true, a component that requires access to your account may use your token to
install software into your project. Only grant images you trust the right to run with your token.
      --group=[]: Indicate components that should be grouped together as <comp1>+<comp2>.
      --ignore-unknown-parameters=false: If true, will not stop processing if a provided parameter does not exist in the
template.
  -i, --image-stream=[]: Name of an image stream to use in the app.
      --insecure-registry=false: If true, indicates that the referenced Docker images are on insecure registries and
should bypass certificate checking
  -l, --labels='': Label to set in all resources for this application.
  -L, --list=false: List all local templates and image streams that can be used to create.
      --name='': Set name to use for generated application artifacts
      --no-install=false: Do not attempt to run images that describe themselves as being installable
  -o, --output='': Output format. One of:
json|yaml|name|templatefile|template|go-template|go-template-file|jsonpath|jsonpath-file.
      --output-version='': The preferred API versions of the output objects
  -p, --param=[]: Specify a key-value pair (e.g., -p FOO=BAR) to set/override a parameter value in the template.
      --param-file=[]: File containing parameter values to set/override in the template.
  -S, --search=false: Search all templates, image streams, and Docker images that match the arguments provided.
  -a, --show-all=true: When printing, show all resources (false means hide terminated pods.)
      --show-labels=false: When printing, show all labels as the last column (default hide labels column)
      --sort-by='': If non-empty, sort list types using this field specification.  The field specification is expressed
as a JSONPath expression (e.g. '{.metadata.name}'). The field in the API resource specified by this JSONPath expression
must be an integer or a string.
      --source-secret='': The name of an existing secret that should be used for cloning a private git repository.
      --strategy=: Specify the build strategy to use if you don't want to detect (docker|pipeline|source).
      --template=[]: Name of a stored template to use in the app.

Use "oc options" for a list of global command-line options (applies to all commands).
```

- Check the list of available application templates

```
[vagrant@openshift lab06-oc-new-app]$ oc new-app --list
Templates (oc new-app --template=<template>)
-----
cakephp-mysql-persistent
  Project: openshift
  An example CakePHP application with a MySQL database. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/cakephp-ex/blob/master/README.md.
dancer-mysql-persistent
  Project: openshift
  An example Dancer application with a MySQL database. For more information about using this template, including OpenShift considerations, see https://github.com/openshift/dancer-ex/blob/master/README.md.
django-psql-persistent
  Project: openshift
  An example Django application with a PostgreSQL database. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/django-ex/blob/master/README.md.
jenkins-ephemeral
  Project: openshift
  Jenkins service, without persistent storage.

WARNING: Any data stored will be lost upon pod destruction. Only use this template for testing.
jenkins-pipeline-example
  Project: openshift
  This example showcases the new Jenkins Pipeline integration in OpenShift,
which performs continuous integration and deployment right on the platform.
The template contains a Jenkinsfile - a definition of a multi-stage CI/CD process - that
leverages the underlying OpenShift platform for dynamic and scalable
builds. OpenShift integrates the status of your pipeline builds into the web
console allowing you to see your entire application lifecycle in a single view.
mariadb-persistent
  Project: openshift
  MariaDB database service, with persistent storage. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/mariadb-container/blob/master/10.2/root/usr/share/container-scripts/mysql/README.md.

NOTE: Scaling to more than one replica is not supported. You must have persistent volumes available in your cluster to use this template.
mongodb-persistent
  Project: openshift
  MongoDB database service, with persistent storage. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/mongodb-container/blob/master/3.2/README.md.

NOTE: Scaling to more than one replica is not supported. You must have persistent volumes available in your cluster to use this template.
mysql-persistent
  Project: openshift
  MySQL database service, with persistent storage. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/mysql-container/blob/master/5.7/root/usr/share/container-scripts/mysql/README.md.

NOTE: Scaling to more than one replica is not supported. You must have persistent volumes available in your cluster to use this template.
nodejs-mongo-persistent
  Project: openshift
  An example Node.js application with a MongoDB database. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/nodejs-ex/blob/master/README.md.
postgresql-persistent
  Project: openshift
  PostgreSQL database service, with persistent storage. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/postgresql-container/.

NOTE: Scaling to more than one replica is not supported. You must have persistent volumes available in your cluster to use this template.
rails-pgsql-persistent
  Project: openshift
  An example Rails application with a PostgreSQL database. For more information about using this template, including OpenShift considerations, see https://github.com/openshift/rails-ex/blob/master/README.md.

Image streams (oc new-app --image-stream=<image-stream> [--code=<source>])
-----
dotnet
  Project: openshift
  Tags:    2.0, latest
httpd
  Project: openshift
  Tags:    2.4, latest
jenkins
  Project: openshift
  Tags:    2, latest
mariadb
  Project: openshift
  Tags:    10.1, 10.2, latest
mongodb
  Project: openshift
  Tags:    3.2, 3.4, 3.6, latest
mysql
  Project: openshift
  Tags:    5.7, latest
nginx
  Project: openshift
  Tags:    1.10, 1.12, 1.8, latest
nodejs
  Project: openshift
  Tags:    10, 6, 8, 8-RHOAR, latest
perl
  Project: openshift
  Tags:    5.24, 5.26, latest
php
  Project: openshift
  Tags:    7.0, 7.1, latest
postgresql
  Project: openshift
  Tags:    10, 9.5, 9.6, latest
python
  Project: openshift
  Tags:    2.7, 3.5, 3.6, latest
redis
  Project: openshift
  Tags:    3.2, latest
ruby
  Project: openshift
  Tags:    2.3, 2.4, 2.5, latest
wildfly
  Project: openshift
  Tags:    10.0, 10.1, 11.0, 12.0, 13.0, 8.1, 9.0, latest
```

- Search mysql-related templates

```
[vagrant@openshift lab06-oc-new-app]$ oc new-app --search mysql
Templates (oc new-app --template=<template>)
-----
mysql-persistent
  Project: openshift
  MySQL database service, with persistent storage. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/mysql-container/blob/master/5.7/root/usr/share/container-scripts/mysql/README.md.

NOTE: Scaling to more than one replica is not supported. You must have persistent volumes available in your cluster to use this template.
cakephp-mysql-persistent
  Project: openshift
  An example CakePHP application with a MySQL database. For more information about using this template, including OpenShift considerations, see https://github.com/sclorg/cakephp-ex/blob/master/README.md.
dancer-mysql-persistent
  Project: openshift
  An example Dancer application with a MySQL database. For more information about using this template, including OpenShift considerations, see https://github.com/openshift/dancer-ex/blob/master/README.md.

Image streams (oc new-app --image-stream=<image-stream> [--code=<source>])
-----
mysql
  Project: openshift
  Tags:    5.7, latest

Docker images (oc new-app --docker-image=<docker-image> [--code=<source>])
-----
mysql
  Registry: Docker Hub
  Tags:     latest
```

## Deploy a basic application using oc new-app

- Search httpd-related images

```
[vagrant@openshift lab06-oc-new-app]$ oc new-app --search httpd
Image streams (oc new-app --image-stream=<image-stream> [--code=<source>])
-----
httpd
  Project: openshift
  Tags:    2.4, latest

Docker images (oc new-app --docker-image=<docker-image> [--code=<source>])
-----
httpd
  Registry: Docker Hub
  Tags:     latest
```

- Create an httpd application

```
[vagrant@openshift lab06-oc-new-app]$ oc new-app httpd
--> Found image 7cbb148 (47 hours old) in image stream "openshift/httpd" under tag "2.4" for "httpd"

    Apache httpd 2.4
    ----------------
    Apache httpd 2.4 available as container, is a powerful, efficient, and extensible web server. Apache supports a variety of features, many implemented as compiled modules which extend the core functionality. These can range from server-side programming language support to authentication schemes. Virtual hosting allows one Apache installation to serve many different Web sites.

    Tags: builder, httpd, httpd24

    * This image will be deployed in deployment config "httpd"
    * Ports 8080/tcp, 8443/tcp will be load balanced by service "httpd"
      * Other containers can access this service through the hostname "httpd"

--> Creating resources ...
    imagestreamtag "httpd:2.4" created
    deploymentconfig "httpd" created
    service "httpd" created
--> Success
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/httpd'
    Run 'oc status' to view your app.
```

- Make sure that deploy pod has been created

```
[vagrant@openshift lab06-oc-new-app]$ oc get pod
NAME            READY     STATUS    RESTARTS   AGE
httpd-1-5nbw6   1/1       Running   0          21s
```

- Check all entities created by oc new-app

```
[vagrant@openshift lab06-oc-new-app]$ oc get all
NAME                      REVISION   DESIRED   CURRENT   TRIGGERED BY
deploymentconfigs/httpd   1          1         1         config,image(httpd:2.4)

NAME                 DOCKER REPO                  TAGS      UPDATED
imagestreams/httpd   172.30.1.1:5000/lab6/httpd   2.4

NAME               READY     STATUS    RESTARTS   AGE
po/httpd-1-5nbw6   1/1       Running   0          41s

NAME         DESIRED   CURRENT   READY     AGE
rc/httpd-1   1         1         1         42s

NAME        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
svc/httpd   ClusterIP   172.30.169.172   <none>        8080/TCP,8443/TCP   42s
```

Note! you should be able to see pod,rc,svc,dc and is entities

- Expose the httpd service

```
[vagrant@openshift lab06-oc-new-app]$ oc expose svc httpd
route "httpd" exposed
```

- Make sure that route exists

```
[vagrant@openshift lab06-oc-new-app]$ oc get route
NAME      HOST/PORT                            PATH      SERVICES   PORT       TERMINATION   WILDCARD
httpd     httpd-lab6.apps.172.24.0.11.nip.io             httpd      8080-tcp                 None
```

- Try to access the application
Note! It is up to you which method to use (curl or Web Browser)


## Using environment variables

- Try to create a mariadb application

```
[vagrant@openshift lab06-oc-new-app]$ oc new-app mariadb
--> Found image 5e78488 (47 hours old) in image stream "openshift/mariadb" under tag "10.2" for "mariadb"

    MariaDB 10.2
    ------------
    MariaDB is a multi-user, multi-threaded SQL database server. The container image provides a containerized packaging of the MariaDB mysqld daemon and client application. The mysqld server daemon accepts connections from clients and provides access to content from MariaDB databases on behalf of the clients.

    Tags: database, mysql, mariadb, mariadb102, rh-mariadb102, galera

    * This image will be deployed in deployment config "mariadb"
    * Port 3306/tcp will be load balanced by service "mariadb"
      * Other containers can access this service through the hostname "mariadb"
    * This image declares volumes and will default to use non-persistent, host-local storage.
      You can add persistent volumes later by running 'volume dc/mariadb --add ...'

--> Creating resources ...
    imagestreamtag "mariadb:10.2" created
    deploymentconfig "mariadb" created
    service "mariadb" created
--> Success
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/mariadb'
    Run 'oc status' to view your app.
```

- Check the mariadb pod status

```
[vagrant@openshift lab06-oc-new-app]$ oc get pod
NAME              READY     STATUS             RESTARTS   AGE
httpd-1-5nbw6     1/1       Running            0          5m
mariadb-1-z5ljm   0/1       CrashLoopBackOff   3          1m
```

- Display mariadb pod logs

```
[vagrant@openshift lab06-oc-new-app]$ oc logs mariadb-1-z5ljm
=> sourcing 20-validate-variables.sh ...
You must either specify the following environment variables:
  MYSQL_USER (regex: '^[a-zA-Z0-9_]+$')
  MYSQL_PASSWORD (regex: '^[a-zA-Z0-9_~!@#$%^&*()-=<>,.?;:|]+$')
  MYSQL_DATABASE (regex: '^[a-zA-Z0-9_]+$')
Or the following environment variable:
  MYSQL_ROOT_PASSWORD (regex: '^[a-zA-Z0-9_~!@#$%^&*()-=<>,.?;:|]+$')
Or both.
Optional Settings:
  MYSQL_LOWER_CASE_TABLE_NAMES (default: 0)
  MYSQL_LOG_QUERIES_ENABLED (default: 0)
  MYSQL_MAX_CONNECTIONS (default: 151)
  MYSQL_FT_MIN_WORD_LEN (default: 4)
  MYSQL_FT_MAX_WORD_LEN (default: 20)
  MYSQL_AIO (default: 1)
  MYSQL_KEY_BUFFER_SIZE (default: 32M or 10% of available memory)
  MYSQL_MAX_ALLOWED_PACKET (default: 200M)
  MYSQL_TABLE_OPEN_CACHE (default: 400)
  MYSQL_SORT_BUFFER_SIZE (default: 256K)
  MYSQL_READ_BUFFER_SIZE (default: 8M or 5% of available memory)
  MYSQL_INNODB_BUFFER_POOL_SIZE (default: 32M or 50% of available memory)
  MYSQL_INNODB_LOG_FILE_SIZE (default: 8M or 15% of available memory)
  MYSQL_INNODB_LOG_BUFFER_SIZE (default: 8M or 15% of available memory)
For more information, see https://github.com/sclorg/mariadb-container
```

Note! the container requires a number of environent variables to start

-  Display all entities created for the service

```
[vagrant@openshift lab06-oc-new-app]$ oc get all -l app=mariadb
NAME                        REVISION   DESIRED   CURRENT   TRIGGERED BY
deploymentconfigs/mariadb   1          1         1         config,image(mariadb:10.2)

NAME                 READY     STATUS             RESTARTS   AGE
po/mariadb-1-z5ljm   0/1       CrashLoopBackOff   5          3m

NAME           DESIRED   CURRENT   READY     AGE
rc/mariadb-1   1         1         0         3m

NAME          TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
svc/mariadb   ClusterIP   172.30.182.4   <none>        3306/TCP   3m
```

- Delete all mariadb entities

```
[vagrant@openshift lab06-oc-new-app]$ oc delete all -l app=mariadb
deploymentconfig "mariadb" deleted
pod "mariadb-1-z5ljm" deleted
service "mariadb" deleted
```

- Delete the "mariadb" image stream

```
[vagrant@openshift lab06-oc-new-app]$ oc delete is mariadb
imagestream "mariadb" deleted
```

Note! the "is" resource is not deleted automatically.

- Re-deploy mariadb service with all parameters

```
[vagrant@openshift lab06-oc-new-app]$ oc new-app -e MYSQL_USER=myuser -e MYSQL_PASSWORD=secret -e MYSQL_DATABASE=db1 mariadb
--> Found image 5e78488 (47 hours old) in image stream "openshift/mariadb" under tag "10.2" for "mariadb"

    MariaDB 10.2
    ------------
    MariaDB is a multi-user, multi-threaded SQL database server. The container image provides a containerized packaging of the MariaDB mysqld daemon and client application. The mysqld server daemon accepts connections from clients and provides access to content from MariaDB databases on behalf of the clients.

    Tags: database, mysql, mariadb, mariadb102, rh-mariadb102, galera

    * This image will be deployed in deployment config "mariadb"
    * Port 3306/tcp will be load balanced by service "mariadb"
      * Other containers can access this service through the hostname "mariadb"
    * This image declares volumes and will default to use non-persistent, host-local storage.
      You can add persistent volumes later by running 'volume dc/mariadb --add ...'

--> Creating resources ...
    imagestreamtag "mariadb:10.2" created
    deploymentconfig "mariadb" created
    service "mariadb" created
--> Success
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/mariadb'
    Run 'oc status' to view your app.
```

- Make sure that the mariadb pod works

```
[vagrant@openshift lab06-oc-new-app]$ oc get pod
NAME              READY     STATUS    RESTARTS   AGE
httpd-1-5nbw6     1/1       Running   0          21m
mariadb-1-tx4xk   1/1       Running   0          4m

[vagrant@openshift lab06-oc-new-app]$ oc exec -it mariadb-1-tx4xk -- /opt/rh/rh-mariadb102/root/usr/bin/mysql -umyuser -psecret -h127.0.0.1 db1 -e 'show databases'
+--------------------+
| Database           |
+--------------------+
| db1                |
| information_schema |
| test               |
+--------------------+
```

## Understanding deployment config

- List available deployment configs

```
[vagrant@openshift lab06-oc-new-app]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     1          1         1         config,image(httpd:2.4)
mariadb   1          1         1         config,image(mariadb:10.2)
```

- Gather details of the mariadb deployment config

```
[vagrant@openshift lab06-oc-new-app]$ oc describe dc mariadb
Name:		mariadb
Namespace:	lab6
Created:	7 minutes ago
Labels:		app=mariadb
Annotations:	openshift.io/generated-by=OpenShiftNewApp
Latest Version:	1
Selector:	app=mariadb,deploymentconfig=mariadb
Replicas:	1
Triggers:	Config, Image(mariadb@10.2, auto=true)
Strategy:	Rolling
Template:
Pod Template:
  Labels:	app=mariadb
		deploymentconfig=mariadb
  Annotations:	openshift.io/generated-by=OpenShiftNewApp
  Containers:
   mariadb:
    Image:	docker.io/centos/mariadb-102-centos7@sha256:e49daf523098e87b04c86c4a6dc0d6c4e192db663bf51a4df37771e2190000bd
    Port:	3306/TCP
    Environment:
      MYSQL_DATABASE:	db1
      MYSQL_PASSWORD:	secret
      MYSQL_USER:	myuser
    Mounts:
      /var/lib/mysql/data from mariadb-volume-1 (rw)
  Volumes:
   mariadb-volume-1:
    Type:	EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:

Deployment #1 (latest):
	Name:		mariadb-1
	Created:	7 minutes ago
	Status:		Complete
	Replicas:	1 current / 1 desired
	Selector:	app=mariadb,deployment=mariadb-1,deploymentconfig=mariadb
	Labels:		app=mariadb,openshift.io/deployment-config.name=mariadb
	Pods Status:	1 Running / 0 Waiting / 0 Succeeded / 0 Failed

Events:
  Type		Reason			Age	From				Message
  ----		------			----	----				-------
  Normal	DeploymentCreated	7m	deploymentconfig-controller	Created new replication controller "mariadb-1" for version 1
```

Note! You can see environment variables

- Update mariadb deployment config as follows

```
[vagrant@openshift lab06-oc-new-app]$ oc edit dc mariadb
```

in the vi editor update environment variables to the following

```
<OMITTED>
    spec:
      containers:
      - env:
        - name: MYSQL_DATABASE
          value: db1_new
        - name: MYSQL_PASSWORD
          value: secret_new
        - name: MYSQL_USER
          value: myuser_new
<OMITTED>
```
save and exit

- Make sure that deployment config version has been increased

```
[vagrant@openshift lab06-oc-new-app]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     1          1         1         config,image(httpd:2.4)
mariadb   2          1         1         config,image(mariadb:10.2)
```

- Make sure that pod has been recreated

```
[vagrant@openshift lab06-oc-new-app]$ oc get pod
NAME              READY     STATUS    RESTARTS   AGE
httpd-1-5nbw6     1/1       Running   0          28m
mariadb-2-jr6t7   1/1       Running   0          3m
```

- Try to access the pod using new username/password and database

```
[vagrant@openshift lab06-oc-new-app]$ oc exec -it mariadb-2-jr6t7 -- /opt/rh/rh-mariadb102/root/usr/bin/mysql -umyuser_new -psecret_new -h127.0.0.1 db1_new -e 'show databases'
+--------------------+
| Database           |
+--------------------+
| db1_new            |
| information_schema |
| test               |
+--------------------+
```

## Redeploy application from the deployment config

- Make sure that both applications are running

```
[vagrant@openshift lab06-oc-new-app]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     1          1         1         config,image(httpd:2.4)
mariadb   2          1         1         config,image(mariadb:10.2)

[vagrant@openshift lab06-oc-new-app]$ oc get pod
NAME              READY     STATUS    RESTARTS   AGE
httpd-1-5nbw6     1/1       Running   0          31m
mariadb-2-jr6t7   1/1       Running   0          6m
```

- Redeploy the mariadb application

```
[vagrant@openshift lab06-oc-new-app]$ oc rollout latest mariadb
deploymentconfig "mariadb" rolled out
```

- Make sure that revision has been increased

```
[vagrant@openshift lab06-oc-new-app]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     1          1         1         config,image(httpd:2.4)
mariadb   3          1         1         config,image(mariadb:10.2)
```

Note! new revision is 3

- Make sure that application has been redeployed

```
[vagrant@openshift lab06-oc-new-app]$ oc get pod
NAME              READY     STATUS    RESTARTS   AGE
httpd-1-5nbw6     1/1       Running   0          33m
mariadb-3-mgg29   1/1       Running   0          53s
```

Note! the number "-3-" in the mariadb name represents revision number

## Scale up and scale down applications

- Increase number of httpd pods to 3

```
[vagrant@openshift lab06-oc-new-app]$ oc scale dc httpd --replicas=3
deploymentconfig "httpd" scaled
```

- Make sure that desired number of replicas is 3

```
[vagrant@openshift lab06-oc-new-app]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     1          3         3         config,image(httpd:2.4)
mariadb   3          1         1         config,image(mariadb:10.2)
```

- Check the number of httpd replicas

```
[vagrant@openshift lab06-oc-new-app]$ oc get pod
NAME              READY     STATUS    RESTARTS   AGE
httpd-1-5nbw6     1/1       Running   0          39m
httpd-1-fwdnv     1/1       Running   0          2s
httpd-1-rqjlv     1/1       Running   0          2s
mariadb-3-mgg29   1/1       Running   0          7m
```

- Scale down the httpd application

```
[vagrant@openshift lab06-oc-new-app]$ oc scale dc httpd --replicas=2
deploymentconfig "httpd" scaled
[vagrant@openshift lab06-oc-new-app]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     1          2         2         config,image(httpd:2.4)
mariadb   3          1         1         config,image(mariadb:10.2)
[vagrant@openshift lab06-oc-new-app]$ oc get pod
NAME              READY     STATUS    RESTARTS   AGE
httpd-1-5nbw6     1/1       Running   0          41m
httpd-1-fwdnv     1/1       Running   0          1m
mariadb-3-mgg29   1/1       Running   0          9m
```


## Cleanup

```
oc delete all --all
oc delete project lab6
```