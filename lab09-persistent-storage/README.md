# lab09-persistent-storage
Lab 9 - Using persistent storage

## Files
All files required for this lab are stored directly in this directory or in /vagrant/lab09-persistent-storage directory of your vagrant machine

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab09-persistent-storage on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab09-persistent-storage
```

- Create a new project named "lab9"

```
oc new-project lab9
```

## Verifying Persistent Volumes (PV)
By default, "oc cluster up" creates a number of PV. You may verify that PVs are available

- Login as the "sysmem:admin" under the root account

```
[vagrant@openshift lab09-persistent-storage]$ sudo oc login -u system:admin
Logged into "https://127.0.0.1:8443" as "system:admin" using existing credentials.

You have access to the following projects and can switch between them with 'oc project <projectname>':

    default
    kube-public
    kube-system
    lab9
  * myproject
    openshift
    openshift-infra
    openshift-node
    openshift-web-console

Using project "myproject".
```

Note! Do not forget to run the command using "sudo".

- Make sure that you are system:admin

```
[vagrant@openshift lab09-persistent-storage]$ sudo oc whoami
system:admin
```

Note! Do not forget to run the command using "sudo".

- List all available cluster PVs

```
[vagrant@openshift lab09-persistent-storage]$ sudo oc get pv
NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM     STORAGECLASS   REASON    AGE
pv0001    100Gi      RWO,ROX,RWX    Recycle          Available                                      4h
pv0002    100Gi      RWO,ROX,RWX    Recycle          Available                                      4h
pv0003    100Gi      RWO,ROX,RWX    Recycle          Available                                      4h
pv0004    100Gi      RWO,ROX,RWX    Recycle          Available                                      4h
pv0005    100Gi      RWO,ROX,RWX    Recycle          Available                                      4h

<OMITTED>
```

Note! There should be ~100 PVs available for usage


- Check location of the persitent data

```
[vagrant@openshift lab09-persistent-storage]$ sudo oc describe pv pv0061
Name:            pv0061
Labels:          volume=pv0061
Annotations:     <none>
StorageClass:
Status:          Available
Claim:
Reclaim Policy:  Recycle
Access Modes:    RWO,ROX,RWX
Capacity:        100Gi
Message:
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /var/lib/origin/openshift.local.pv/pv0061
    HostPathType:
Events:            <none>
```

Note! all volume data is stored at /var/lib/origin/openshift.local.pv/<pvname>


## Creating Persistent Volume Claims (PVC)

- Make sure that you are in "lab9" project

```
oc project lab9
```

- Check the claim file

```
cat pvc-web.yaml
```

- Create a PVC

```
[vagrant@openshift lab09-persistent-storage]$ oc create -f pvc-web.yaml
persistentvolumeclaim "pvc-web" created
```

- Make sure that PVC is bound to a PV

```
[vagrant@openshift lab09-persistent-storage]$ oc get pvc
NAME      STATUS    VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc-web   Bound     pv0059    100Gi      RWO,ROX,RWX                   3s
```

Note! The example above shows that pvc-web is bound to pv0059. This means that data will be located at /var/lib/origin/openshift.local.pv/pv0059

Note! the PV may be different depending on your OpenShift cluster settings

## Deploying a persistent application
We are going to deploy an httpd container which data is persistent.

- Deploy  httpd application

```
oc new-app httpd
```

- Make sure that application has been deployed

```
[vagrant@openshift lab09-persistent-storage]$ oc get pod
NAME            READY     STATUS    RESTARTS   AGE
httpd-1-j6zpk   1/1       Running   0          24s
```

- Check the revision of the "httpd" deployment config

[vagrant@openshift lab09-persistent-storage]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     1          1         1         config,image(httpd:2.4)
```

- Mount volume data via "oc volume"

```
[vagrant@openshift lab09-persistent-storage]$ oc volume dc/httpd --add --name=webdata -t pvc --claim-name=pvc-web --mount-path=/var/www/html
deploymentconfig "httpd" updated
```

- Make sure that the "httpd" deployment config has been updated

```
[vagrant@openshift lab09-persistent-storage]$ oc get dc
NAME      REVISION   DESIRED   CURRENT   TRIGGERED BY
httpd     2          1         1         config,image(httpd:2.4)
```

- Make sure that volume definition exists in both - dc and pod

```
[vagrant@openshift lab09-persistent-storage]$ oc describe dc httpd
Name:		httpd
Namespace:	lab9
Created:	4 minutes ago
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
      /var/www/html from webdata (rw)
  Volumes:
   webdata:
    Type:	PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:	pvc-web
    ReadOnly:	false

<OMITTED>
```

```
[vagrant@openshift lab09-persistent-storage]$ oc get pod
NAME            READY     STATUS    RESTARTS   AGE
httpd-2-5pc42   1/1       Running   0          2m
[vagrant@openshift lab09-persistent-storage]$ oc describe pod httpd-2-5pc42
Name:           httpd-2-5pc42
Namespace:      lab9
Node:           localhost/10.0.2.15
Start Time:     Sat, 08 Dec 2018 06:00:34 +0000
Labels:         app=httpd
                deployment=httpd-2
                deploymentconfig=httpd
Annotations:    openshift.io/deployment-config.latest-version=2
                openshift.io/deployment-config.name=httpd
                openshift.io/deployment.name=httpd-2
                openshift.io/generated-by=OpenShiftNewApp
                openshift.io/scc=restricted
Status:         Running
IP:             172.17.0.5
Controlled By:  ReplicationController/httpd-2
Containers:
  httpd:
    Container ID:   docker://ebf2145c2e0908608a5e450ab208ad525a156ab9e65f4e37de233dd8163a4a58
    Image:          docker.io/centos/httpd-24-centos7@sha256:f6393681ec205974a68386ac21e4ec2b76d42bfc885872ab8718f66826f95e68
    Image ID:       docker-pullable://docker.io/centos/httpd-24-centos7@sha256:f6393681ec205974a68386ac21e4ec2b76d42bfc885872ab8718f66826f95e68
    Ports:          8080/TCP, 8443/TCP
    State:          Running
      Started:      Sat, 08 Dec 2018 06:00:35 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-dzt47 (ro)
      /var/www/html from webdata (rw)
Conditions:
  Type           Status
  Initialized    True
  Ready          True
  PodScheduled   True
Volumes:
  webdata:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  pvc-web
    ReadOnly:   false
  default-token-dzt47:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-dzt47
    Optional:    false
```


- Copy index.html to the required location

```
sudo cp index.html /var/lib/origin/openshift.local.pv/pv0059
sudo chown root:root /var/lib/origin/openshift.local.pv/pv0059/index.html
sudo chmod 664 /var/lib/origin/openshift.local.pv/pv0059/index.html
```

- Expose the httpd application

```
[vagrant@openshift lab09-persistent-storage]$ oc expose svc httpd
route "httpd" exposed
[vagrant@openshift lab09-persistent-storage]$ oc get route
NAME      HOST/PORT                            PATH      SERVICES   PORT       TERMINATION   WILDCARD
httpd     httpd-lab9.apps.172.24.0.11.nip.io             httpd      8080-tcp                 None
```

- Make sure that new container answers correctly

```
[vagrant@openshift lab09-persistent-storage]$ curl httpd-lab9.apps.172.24.0.11.nip.io
It is stored on a persistent storage
```

- Update index.html

```
sudo bash -c 'echo "New data" > /var/lib/origin/openshift.local.pv/pv0059/index.html'
```

- Make sure that new data is accessible

```
[vagrant@openshift lab09-persistent-storage]$ curl httpd-lab9.apps.172.24.0.11.nip.io
New data
```



