# lab13-deployment-configs

Lab 13 - Using deployment configs for deploying applications

## Files

All files required for this lab are stored directly in this directory or in _/vagrant/lab13-deployment-configs_ directory of your vagrant machine

## Default routes

The lab installation uses apps.172.24.0.11.nip.io as the default application domain.

## Preparation

It is assumed that all activities will be performed inside _/vagrant/lab13-deployment-configs_ on your vagrant machine.

- Run the following command to change current directory

```
cd /vagrant/lab13-deployment-configs
```

- Create a new project named __lab13__

```
$ oc new-project lab13
```

## How create a Deployment Config

For this can be used `oc create deploymentconfig` command.


## Command oc create deploymentconfig


### Getting help


```
$ oc create deploymentconfig -h
Create a deployment config that uses a given image.

Deployment configs define the template for a pod and manages deploying new images or configuration changes.

Aliases:
deploymentconfig, dc

Usage:
  oc create deploymentconfig NAME --image=IMAGE -- [COMMAND] [args...] [flags]

Examples:
  # Create an nginx deployment config named my-nginx
  oc create deploymentconfig my-nginx --image=nginx

Options:
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --dry-run=false: If true, only print the object that would be sent, without sending it.
      --image='': The image for the container to run.
  -o, --output='': Output format. One of:
json|yaml|name|template|go-template|go-template-file|templatefile|jsonpath|jsonpath-file.
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].

Use "oc options" for a list of global command-line options (applies to all commands).
```


### Creating of a deployment config

This command can be used to create a deployement config. Option `-o yaml` tells to print out the created configuration on the screen.

Save the output to file `dc.yaml`

```
$ oc create deploymentconfig database --image=docker.io/mysql -o yaml --dry-run | tee dc.yaml
```

```yaml
apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  creationTimestamp: 2019-04-24T01:34:27Z
  generation: 1
  name: database
  namespace: lab13
  resourceVersion: "686061"
  selfLink: /apis/apps.openshift.io/v1/namespaces/lab13/deploymentconfigs/database
  uid: 1942b44b-6631-11e9-b07d-124d3830dbee
spec:
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    deployment-config.name: database
  strategy:
    activeDeadlineSeconds: 21600
    resources: {}
    rollingParams:
      intervalSeconds: 1
      maxSurge: 25%
      maxUnavailable: 25%
      timeoutSeconds: 600
      updatePeriodSeconds: 1
    type: Rolling
  template:
    metadata:
      creationTimestamp: null
      labels:
        deployment-config.name: database
    spec:
      containers:
      - image: docker.io/mysql
        imagePullPolicy: Always
        name: default-container
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
  test: false triggers:
  - type: ConfigChange
status:
  availableReplicas: 0
  latestVersion: 0
  observedGeneration: 0
  replicas: 0
  unavailableReplicas: 0
  updatedReplicas: 0
```

Since we use the publicly available image from __docker.io__ we can find there a documentation about this as _https://hub.docker.com/_/mysql_. The documentation tells that we need to provide some environment variables and a storage for data:

* Modify the file as shown below

  ** add environment variables 

  ```yaml
      env:
        - name: MYSQL_ROOT_PASSWORD
          value: rootpass
        - name: MYSQL_DATABASE
          value: demobase
        - name: MYSQL_USER
          value: demouser
        - name: MYSQL_PASSWORD
          value: demopass
  ``` 

  ** add a volume
  ```yaml
      volumes:
        - name: datadir
          type: emptyDir
  ```

  and in the specification of the database container, put this

  ```yaml
      volumeMounts:
        - name: datadir
          mountPoint: /var/lib/mysql
  ```
  We use type `emptyDir`. That means that this storage will be available while the pod is available.

* The final config should look like this

```yaml
apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  creationTimestamp: 2019-04-24T01:34:27Z
  generation: 1
  name: database
  namespace: lab13
  resourceVersion: "686061"
  selfLink: /apis/apps.openshift.io/v1/namespaces/lab13/deploymentconfigs/database
  uid: 1942b44b-6631-11e9-b07d-124d3830dbee
spec:
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    deployment-config.name: database
  strategy:
    activeDeadlineSeconds: 21600
    resources: {}
    rollingParams:
      intervalSeconds: 1
      maxSurge: 25%
      maxUnavailable: 25%
      timeoutSeconds: 600
      updatePeriodSeconds: 1
    type: Rolling
  template:
    metadata:
      creationTimestamp: null
      labels:
        deployment-config.name: database
    spec:
      volumes:
        - name: datadir
          type: emptyDir
      containers:
      - image: docker.io/mysql
        imagePullPolicy: Always
        name: default-container
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
          - name: datadir
            mountPath: /var/lib/mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: rootpass
        - name: MYSQL_DATABASE
          value: demobase
        - name: MYSQL_USER
          value: demouser
        - name: MYSQL_PASSWORD
          value: demopass
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
  test: false
  triggers:
  - type: ConfigChange
status:
  availableReplicas: 0
  latestVersion: 0
  observedGeneration: 0
  replicas: 0
  unavailableReplicas: 0
  updatedReplicas: 0
```

* Create the deployment config from `dc.yaml` file

```
$ oc create -f dc.yaml
deploymentconfig.apps.openshift.io/database created
```

* Check created resources

```
$ oc get all
NAME                   READY     STATUS    RESTARTS   AGE
pod/database-1-tmn25   1/1       Running   0          20s

NAME                               DESIRED   CURRENT   READY     AGE
replicationcontroller/database-1   1         1         1         25s

NAME                                          REVISION   DESIRED   CURRENT   TRIGGERED BY
deploymentconfig.apps.openshift.io/database   1          1         1         config
```

* Now we can enter to the pod `database-1-tmn25` and check the database

```
$ oc rsh database-1-tmn25 /bin/sh

```
and run following

```
$ echo 'show databases;' | mysql -u$MYSQL_USER -p$MYSQL_PASSWORD
mysql: [Warning] Using a password on the command line interface can be insecure.
Database
demobase
information_schema
$ exit
```

Here we even don't need to know which login and passwords have been set. We can just use those environment variables.


* Remove the deployment config

```
$ oc delete -f dc.yaml
deploymentconfig.apps.openshift.io "database" deleted
```

## Authors

- Dmitrii Mostovshchikokv <Dmitrii.Mostovshchikov@li9.com>



