# lab07-injecting-configuration-data

Lab 7 - Injecting configuration data

## Files

All files required for this lab are stored directly in this directory or in /vagrant/lab07-injecting-configuration-data directory of your vagrant machine

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab07-injecting-configuration-data on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab07-injecting-configuration-data
```

- Create a new project named "lab7"

```
oc new-project lab7
```

## Creating secrets

- Check builtin documentation how to create secrets

```
neonbook1:lab07-injecting-configuration-data neon$ oc create secret generic  -h
Create a secret based on a file, directory, or specified literal value.

A single secret may package one or more key/value pairs.

When creating a secret based on a file, the key will default to the basename of the file, and the
value will default to the file content. If the basename is an invalid key or you wish to chose your
own, you may specify an alternate key.

When creating a secret based on a directory, each file whose basename is a valid key in the
directory will be packaged into the secret. Any directory entries except regular files are ignored
(e.g. subdirectories, symlinks, devices, pipes, etc).

Usage:
  oc create secret generic NAME [--type=string] [--from-file=[key=]source]
[--from-literal=key1=value1] [--dry-run] [flags]

Examples:
  # Create a new secret named my-secret with keys for each file in folder bar
  oc create secret generic my-secret --from-file=path/to/bar

  # Create a new secret named my-secret with specified keys instead of names on disk
  oc create secret generic my-secret --from-file=ssh-privatekey=~/.ssh/id_rsa
--from-file=ssh-publickey=~/.ssh/id_rsa.pub

  # Create a new secret named my-secret with key1=supersecret and key2=topsecret
  oc create secret generic my-secret --from-literal=key1=supersecret --from-literal=key2=topsecret

  # Create a new secret named my-secret using a combination of a file and a literal
  oc create secret generic my-secret --from-file=ssh-privatekey=~/.ssh/id_rsa
--from-literal=passphrase=topsecret

  # Create a new secret named my-secret from an env file
  oc create secret generic my-secret --from-env-file=path/to/bar.env

Options:
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or
map key is missing in the template. Only applies to golang and jsonpath output formats.
      --append-hash=false: Append a hash of the secret to its name.
      --dry-run=false: If true, only print the object that would be sent, without sending it.
      --from-env-file='': Specify the path to a file to read lines of key=val pairs to create a
secret (i.e. a Docker .env file).
      --from-file=[]: Key files can be specified using their file path, in which case a default name
will be given to them, or optionally with a name and file path, in which case the given name will be
used.  Specifying a directory will iterate each named file in the directory that is a valid secret
key.
      --from-literal=[]: Specify a key and literal value to insert in secret (i.e. mykey=somevalue)
      --generator='secret/v1': The name of the API generator to use.
  -o, --output='': Output format. One of:
json|yaml|name|template|go-template|go-template-file|templatefile|jsonpath|jsonpath-file.
      --save-config=false: If true, the configuration of current object will be saved in its
annotation. Otherwise, the annotation will be unchanged. This flag is useful when you want to
perform kubectl apply on this object in the future.
      --template='': Template string or path to template file to use when -o=go-template,
-o=go-template-file. The template format is golang templates
[http://golang.org/pkg/text/template/#pkg-overview].
      --type='': The type of secret to create
      --validate=false: If true, use a schema to validate the input before sending it

Use "oc options" for a list of global command-line options (applies to all commands).
```

- Create a secret which contain accesses to a database service

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc create secret generic mysecret --from-literal=MYSQL_USER=user1 --from-literal=MYSQL_PASSWORD=topsecret --from-literal=MYSQL_DATABASE=secretdb
secret "mysecret" created
```

- Make sure that the "mysecret" has been created

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc get secret mysecret
NAME       TYPE      DATA      AGE
mysecret   Opaque    3         6s
```

- Gather secret details

```
vagrant@openshift lab07-injecting-configuration-data]$ oc describe secret mysecret
Name:         mysecret
Namespace:    lab7
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
MYSQL_DATABASE:  8 bytes
MYSQL_PASSWORD:  9 bytes
MYSQL_USER:      5 bytes
```

- Export secret runtime coniguration

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc describe secret mysecret
Name:         mysecret
Namespace:    lab7
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
MYSQL_DATABASE:  8 bytes
MYSQL_PASSWORD:  9 bytes
MYSQL_USER:      5 bytes
[vagrant@openshift lab07-injecting-configuration-data]$ oc descr^C
[vagrant@openshift lab07-injecting-configuration-data]$ oc get secret mysecret -o yaml
apiVersion: v1
data:
  MYSQL_DATABASE: c2VjcmV0ZGI=
  MYSQL_PASSWORD: dG9wc2VjcmV0
  MYSQL_USER: dXNlcjE=
kind: Secret
metadata:
  creationTimestamp: 2018-12-08T02:20:47Z
  name: mysecret
  namespace: lab7
  resourceVersion: "9490"
  selfLink: /api/v1/namespaces/lab7/secrets/mysecret
  uid: df97c1c5-fa8f-11e8-914e-525400c042d5
type: Opaque
```

Note! Make sure that values are encrypted

- Try to decode values

```
[vagrant@openshift lab07-injecting-configuration-data]$ echo c2VjcmV0ZGI= | base64 -d
secretdb

[vagrant@openshift lab07-injecting-configuration-data]$ echo dG9wc2VjcmV0 | base64 -d
topsecret

[vagrant@openshift lab07-injecting-configuration-data]$ echo dXNlcjE= | base64 -d
user1
```

- Create a new secret with the same values using a file

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc create secret generic myfile-secret --from-env-file=./mysql_secrets.txt
secret "myfile-secret" created

[vagrant@openshift lab07-injecting-configuration-data]$ oc get secret myfile-secret
NAME            TYPE      DATA      AGE
myfile-secret   Opaque    3         6s
```

- Gather secret details

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc describe secret myfile-secret
Name:         myfile-secret
Namespace:    lab7
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
MYSQL_PASSWORD:  9 bytes
MYSQL_USER:      5 bytes
MYSQL_DATABASE:  8 bytes
```

## Using secrets

- Create a mariadb conainer without passing environment variables. It is expected that deployment fails

```
oc new-app mariadb
```

- Make sure that container fails

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc get pod
NAME              READY     STATUS    RESTARTS   AGE
mariadb-1-2p2zz   0/1       Error     3          49s
```

- Connect secret mysecret as environment variable file

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc set env dc/mariadb --from secret/mysecret
deploymentconfig "mariadb" updated
```

- Make sure that mariadb application has been redeployed

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
mariadb   2          1         1         config,image(mariadb:10.2)
```

- Make sure that mairiadb pod works properly

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc get pod
NAME              READY     STATUS        RESTARTS   AGE
mariadb-1-2p2zz   0/1       Terminating   4          3m
mariadb-2-j4c42   1/1       Running       0          56s
```

- Make sure that mariadb service uses correct variables

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc exec mariadb-2-j4c42 env|grep MYSQL_
MYSQL_PASSWORD=topsecret
MYSQL_USER=user1
MYSQL_DATABASE=secretdb
MYSQL_VERSION=10.2
MYSQL_PREFIX=/opt/rh/rh-mariadb102/root/usr
```

Note! These variables has been taken from the secret

## Creating config maps

In this example, we will mount config map as a file on the filesystem. This may be useful for application configuration

- Delete all OpenShift entities created previosly

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc delete all --all
deploymentconfig "mariadb" deleted
imagestream "mariadb" deleted
pod "mariadb-2-j4c42" deleted
service "mariadb" deleted
```

- Check the "index.html" file

```
cat index.html
```

- Create a config map named "cm1" from index.html

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc create cm cm1 --from-file index.html
configmap "cm1" created
```

- Make sure that config map "cm1" has been created and contains correct data

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc get cm
NAME      DATA      AGE
cm1       1         3s


[vagrant@openshift lab07-injecting-configuration-data]$ oc describe cm cm1
Name:         cm1
Namespace:    lab7
Labels:       <none>
Annotations:  <none>

Data
====
index.html:
----
<HTML><HEAD><TITLE>Config map test page</TITLE></HEAD>
<BODY>
<H1>If you can see this page - config map works!</H1>
</BODY></HTML>


Events:  <none>
```

- Display config map runtime data

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc get cm cm1 -o yaml
apiVersion: v1
data:
  index.html: |+
    <HTML><HEAD><TITLE>Config map test page</TITLE></HEAD>
    <BODY>
    <H1>If you can see this page - config map works!</H1>
    </BODY></HTML>

kind: ConfigMap
metadata:
  creationTimestamp: 2018-12-08T03:07:48Z
  name: cm1
  namespace: lab7
  resourceVersion: "13559"
  selfLink: /api/v1/namespaces/lab7/configmaps/cm1
  uid: 71667f50-fa96-11e8-914e-525400c042d5
```

- Deploy an httpd service

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc new-app httpd


[vagrant@openshift lab07-injecting-configuration-data]$ oc get pod
NAME            READY     STATUS    RESTARTS   AGE
httpd-1-p2cjj   1/1       Running   0          4s
```

- Mount config map cm1 as a file using the following syntax

```
oc set volumes dc/httpd --add -t configmap  -m /var/www/html --configmap-name cm1
```

This should work as follows

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc set volumes dc/httpd --add -t configmap  -m /var/www/html --configmap-name cm1
info: Generated volume name: volume-xjkkr
deploymentconfig "httpd" updated
```

- Make sure that the httpd appliation has been redeployed.

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     2          1         1         config,image(httpd:2.4)

[vagrant@openshift lab07-injecting-configuration-data]$ oc get pod
NAME            READY     STATUS    RESTARTS   AGE
httpd-2-t7rw9   1/1       Running   0          6s
```

- Gather service address

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc describe svc|grep IP:
IP:                172.30.227.127
```

- Access the service IP

```
[vagrant@openshift lab07-injecting-configuration-data]$ curl 172.30.227.127:8080
<HTML><HEAD><TITLE>Config map test page</TITLE></HEAD>
<BODY>
<H1>If you can see this page - config map works!</H1>
</BODY></HTML>
```

- Display deployment config

```
[vagrant@openshift lab07-injecting-configuration-data]$ oc describe dc httpd
Name:		httpd
Namespace:	lab7
Created:	3 minutes ago
Labels:		app=httpd
Annotations:	openshift.io/generated-by=OpenShiftNewApp
Latest Version:	2
Selector:	app=httpd,deploymentconfig=httpd
Replicas:	1
Triggers:	Config, Image(httpd@2.4, auto=true)
Strategy:	Rolling
Template:
Pod Template:
  Labels:	app=httpd
		deploymentconfig=httpd
  Annotations:	openshift.io/generated-by=OpenShiftNewApp
  Containers:
   httpd:
    Image:		docker.io/centos/httpd-24-centos7@sha256:f6393681ec205974a68386ac21e4ec2b76d42bfc885872ab8718f66826f95e68
    Ports:		8080/TCP, 8443/TCP
    Environment:	<none>
    Mounts:
      /var/www/html from volume-xjkkr (rw)
  Volumes:
   volume-xjkkr:
    Type:	ConfigMap (a volume populated by a ConfigMap)
    Name:	cm1
    Optional:	false

Deployment #2 (latest):
	Name:		httpd-2
	Created:	2 minutes ago
	Status:		Complete
	Replicas:	1 current / 1 desired
	Selector:	app=httpd,deployment=httpd-2,deploymentconfig=httpd
	Labels:		app=httpd,openshift.io/deployment-config.name=httpd
	Pods Status:	1 Running / 0 Waiting / 0 Succeeded / 0 Failed
Deployment #1:
	Created:	3 minutes ago
	Status:		Complete
	Replicas:	0 current / 0 desired

Events:
  Type		Reason			Age	From				Message
  ----		------			----	----				-------
  Normal	DeploymentCreated	3m	deploymentconfig-controller	Created new replication controller "httpd-1" for version 1
  Normal	DeploymentCreated	2m	deploymentconfig-controller	Created new replication controller "httpd-2" for version 2
```

Note! This has been mounted as volume

## Cleanup

```
oc delete lab7
```
