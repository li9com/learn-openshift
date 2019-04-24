# lab13-deployment-configs

Lab 13 - Using deployment configs for deploying applications

## Files

All files required for this lab are stored directly in this directory or in _/vagrant/lab13-deployment-configs_ directory of your vagrant machine


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

This command can be used to create a deployement config. Option `-o yaml` also tells to print out the created configuration on the screen. Option `--dry-run` performs a test run without actual creating.

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

Since we use the publicly available image from __docker.io__ we can find there a documentation about it as _https://hub.docker.com/_/mysql_. The documentation tells that we need to provide some environment variables and a storage for data:

* Add following pieces of the confiruation to `dc.yaml` file

  * environment variables 

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

  * an ephemeral volume
  ```yaml
      volumes:
        - name: datadir
          type: emptyDir
  ```
  We use volume type `emptyDir`. That means that this storage will be available while the pod is available and any data on it will be lost after the pod dies.

  * and in the specification of the database container, put this

  ```yaml
      volumeMounts:
        - name: datadir
          mountPoint: /var/lib/mysql
  ```

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
### define a volume
      volumes:
        - name: datadir
          type: emptyDir
### end
      containers:
      - image: docker.io/mysql
        imagePullPolicy: Always
        name: default-container
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
### attaching a volume to the container
        volumeMounts:
          - name: datadir
            mountPath: /var/lib/mysql
### end
### environment variables
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: rootpass
        - name: MYSQL_DATABASE
          value: demobase
        - name: MYSQL_USER
          value: demouser
        - name: MYSQL_PASSWORD
          value: demopass
### end
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

* Replication Controller _replicationcontroller/database-1_

Here we can find that the _deployment config_ has created a _replication controller_ named as __database-1__, that is __replicationcontroller/database-1__.

```
$ oc describe replicationcontroller/database-1
```

```
Name:         database-1
Namespace:    lab13
Selector:     deployment-config.name=database,deployment=database-1,deploymentconfig=database
Labels:       openshift.io/deployment-config.name=database
Annotations:  openshift.io/deployer-pod.completed-at=2019-04-24 15:10:36 +0000 UTC
              openshift.io/deployer-pod.created-at=2019-04-24 15:10:26 +0000 UTC
              openshift.io/deployer-pod.name=database-1-deploy
              openshift.io/deployment-config.latest-version=1
              openshift.io/deployment-config.name=database
              openshift.io/deployment.phase=Complete
              openshift.io/deployment.replicas=1
              openshift.io/deployment.status-reason=config change
              openshift.io/encoded-deployment-config={"kind":"DeploymentConfig","apiVersion":"apps.openshift.io/v1","metadata":{"name":"database","namespace":"lab13","selfLink":"/apis/apps.openshift.io/v1/namespace...
Replicas:     1 current / 1 desired
Pods Status:  1 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:       deployment=database-1
                deployment-config.name=database
                deploymentconfig=database
  Annotations:  openshift.io/deployment-config.latest-version=1
                openshift.io/deployment-config.name=database
                openshift.io/deployment.name=database-1
  Containers:
   default-container:
    Image:      docker.io/mysql
    Port:       <none>
    Host Port:  <none>
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpass
      MYSQL_DATABASE:       demobase
      MYSQL_USER:           demouser
      MYSQL_PASSWORD:       demopass
    Mounts:
      /var/lib/mysql from datadir (rw)
  Volumes:
   datadir:
    Type:    EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
Events:
  Type    Reason            Age   From                    Message
  ----    ------            ----  ----                    -------
  Normal  SuccessfulCreate  1m    replication-controller  Created pod: database-1-pk5l6
```

The annotations were added automatically and they tell what has created the replication controller and other information

```
Annotations:  openshift.io/deployer-pod.completed-at=2019-04-24 15:10:36 +0000 UTC
              openshift.io/deployer-pod.created-at=2019-04-24 15:10:26 +0000 UTC
              openshift.io/deployer-pod.name=database-1-deploy
              openshift.io/deployment-config.latest-version=1
              openshift.io/deployment-config.name=database
              openshift.io/deployment.phase=Complete
              openshift.io/deployment.replicas=1
              openshift.io/deployment.status-reason=config change
```

* Pod 

Getting details from the Pod

```
$ oc describe pod/database-1-pk5l6
```

```
Name:               database-1-pk5l6
Namespace:          lab13
Priority:           0
PriorityClassName:  <none>
Node:               node04.ocp.local/172.31.53.11
Start Time:         Wed, 24 Apr 2019 11:10:30 -0400
Labels:             deployment=database-1
                    deployment-config.name=database
                    deploymentconfig=database
Annotations:        openshift.io/deployment-config.latest-version=1
                    openshift.io/deployment-config.name=database
                    openshift.io/deployment.name=database-1
                    openshift.io/scc=restricted
Status:             Running
IP:                 10.130.0.253
Controlled By:      ReplicationController/database-1
Containers:
  default-container:
    Container ID:   docker://3990d12c13077f087b9c8144895f0274d99cace6858ccf7524757e47a3d58f47
    Image:          docker.io/mysql
    Image ID:       docker-pullable://docker.io/mysql@sha256:a7cf659a764732a27963429a87eccc8457e6d4af0ee9d5140a3b56e74986eed7
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Wed, 24 Apr 2019 11:10:34 -0400
    Ready:          True
    Restart Count:  0
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpass
      MYSQL_DATABASE:       demobase
      MYSQL_USER:           demouser
      MYSQL_PASSWORD:       demopass
    Mounts:
      /var/lib/mysql from datadir (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-982kj (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  datadir:
    Type:    EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
  default-token-982kj:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-982kj
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  region=primary
Tolerations:     <none>
Events:
  Type    Reason     Age   From                       Message
  ----    ------     ----  ----                       -------
  Normal  Scheduled  6m    default-scheduler          Successfully assigned lab13/database-1-pk5l6 to node04.ocp.local
  Normal  Pulling    6m    kubelet, node04.ocp.local  pulling image "docker.io/mysql"
  Normal  Pulled     6m    kubelet, node04.ocp.local  Successfully pulled image "docker.io/mysql"
  Normal  Created    6m    kubelet, node04.ocp.local  Created container
  Normal  Started    6m    kubelet, node04.ocp.local  Started container
```

We can find details of what controls the pod.

```
Annotations:        openshift.io/deployment-config.latest-version=1
                    openshift.io/deployment-config.name=database
                    openshift.io/deployment.name=database-1
                    openshift.io/scc=restricted
Status:             Running
Controlled By:      ReplicationController/database-1
```

* Dependencies

From here we can see that what we need is only to create a deployment config and the other work such as creating a proper _Replication Controller_ and a _Pod_ will be done automatically.


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

Here we even don't need to know which login and passwords have been set. We can just use the provided environment variables.


* Change some variables

Now let's change some configuration information

```
$ oc set env dc/database MYSQL_USER=newuser MYSQL_PASSWORD=newpass
```

and watch for the result

```
$ oc get pod --watch
NAME                READY     STATUS              RESTARTS   AGE
database-1-pk5l6    1/1       Running             0          13m
database-2-deploy   0/1       ContainerCreating   0          5s
database-2-deploy   1/1       Running   0         6s
database-2-sbmlv   0/1       Pending   0         0s
database-2-sbmlv   0/1       Pending   0         0s
database-2-sbmlv   0/1       ContainerCreating   0         1s
database-2-sbmlv   1/1       Running   0         6s
database-1-pk5l6   1/1       Terminating   0         13m
database-1-pk5l6   0/1       Terminating   0         13m
database-2-deploy   0/1       Completed   0         18s
database-2-deploy   0/1       Terminating   0         18s
database-2-deploy   0/1       Terminating   0         18s
database-1-pk5l6   0/1       Terminating   0         14m
database-1-pk5l6   0/1       Terminating   0         14m
```

oc just see the status of pods at a moment of time
```
$ oc get pod
NAME               READY     STATUS    RESTARTS   AGE
database-2-sbmlv   1/1       Running   0          44s
```

This example demonstrates that __Deployment Configs__ manages its objects and creates them when needed. Current triggers can found this way:

```
$ oc describe dc/database | grep ^Triggers
Triggers: Config
```

The only configured trigger now is _Config_. That means that any change of configuration of the _deployment config_ will trigger a recreation of pods.

At the same time, such events create a new configuration for the _replication controller_:

```
$ oc get rc
NAME         DESIRED   CURRENT   READY     AGE
database-1   0         0         0         26m
database-2   1         1         1         13m
```

* Getting information about changes of the configuration

```
$ oc rollout history dc/database
deploymentconfigs "database"
REVISION  STATUS    CAUSE
1   Complete  config change
2   Complete  config change
```

* View a historical configuration

```
$ oc rollout history dc/database --revision=1
deploymentconfigs "database" with revision #1
Pod Template:
  Labels: deployment=database-1
  deployment-config.name=database
  deploymentconfig=database
  Annotations:  openshift.io/deployment-config.latest-version=1
  openshift.io/deployment-config.name=database
  openshift.io/deployment.name=database-1
  Containers:
   default-container:
    Image:  docker.io/mysql
    Port: <none>
    Host Port:  <none>
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpass
      MYSQL_DATABASE: demobase
      MYSQL_USER: demouser
      MYSQL_PASSWORD: demopass
    Mounts:
      /var/lib/mysql from datadir (rw)
  Volumes:
   datadir:
    Type: EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
```

We can see that variables _MYSQL_USER_, _MYSQL_PASSWORD_ have here old values.

* Going back to a previous configuration

Keep in mind that latest Pod has been destroyed and a new one created thus it got a new name.

```
$ oc rollout undo dc/database --to-revision=1
deploymentconfig.apps.openshift.io/database rolled back
```

Trying latest login and password - they do not work
```
$ echo 'show databases;' | oc rsh database-3-w59hq mysql -unewuser -pnewpass demobase
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'newuser'@'localhost' (using password: YES)
command terminated with exit code 1
```

Trying the initial login and passwords - they work

```
$ echo 'show databases;' | oc rsh database-3-w59hq mysql -udemouser -pdemopass demobase
mysql: [Warning] Using a password on the command line interface can be insecure.
Database
demobase
information_schema
```

And, since, the current configuration was also update, a new historical state is also added

```
$ oc rollout history dc/database
deploymentconfigs "database"
REVISION  STATUS    CAUSE
1   Complete  config change
2   Complete  config change
3   Complete  config change
```


* Cleaning up

```
$ oc delete -f dc.yaml
deploymentconfig.apps.openshift.io "database" deleted

$ oc delete project lab13
project.project.openshift.io "lab13" deleted
```

## Authors

- Dmitrii Mostovshchikokv <Dmitrii.Mostovshchikov@li9.com>



