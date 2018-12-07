# lab03-managing-pods
Lab 3 - Managing pods

## Files
All files required for this lab are stored directly in this directory or in /vagrant/lab03-managing-pods/ directory of your vagrant machine

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab03-managing-pods on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab03-managing-pods/pod_httpd.yaml
```

- Create a new project named "lab3-httpd"

```
[vagrant@openshift lab03-managing-pods]$ oc new-project lab3-httpd
Now using project "lab3-httpd" on server "https://localhost:8443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app centos/ruby-25-centos7~https://github.com/sclorg/ruby-ex.git

to build a new example application in Ruby.
```

## Creating Pods manually

- Check syntax of pod_httpd.yaml

```
cat pod_httpd.yaml
```

- Check internal documentation

```
[vagrant@openshift lab03-managing-pods]$ oc create -h
Create a resource by filename or stdin

JSON and YAML formats are accepted.

Usage:
  oc create -f FILENAME [flags]

Examples:
  # Create a pod using the data in pod.json.
  oc create -f pod.json

  # Create a pod based on the JSON passed into stdin.
  cat pod.json | oc create -f -
```

- Create the httpd pod manually

```
[vagrant@openshift lab03-managing-pods]$ oc create -f pod_httpd.yaml
pod/httpd created
```


## Getting pod details

- Check status of the port using "oc get pod"
Note! it is expected that Pod status changes from "ContainerCreating" to "Running"

```
[vagrant@openshift lab03-managing-pods]$ oc get pod
NAME      READY     STATUS              RESTARTS   AGE
httpd     0/1       ContainerCreating   0          4s
```

```
[vagrant@openshift lab03-managing-pods]$ oc get pod
NAME      READY     STATUS    RESTARTS   AGE
httpd     1/1       Running   0          1m
```

- Check internal documentation for "oc describe"

```
[vagrant@openshift lab03-managing-pods]$ oc describe -h
Show details of a specific resource

This command joins many API calls together to form a detailed description of a given resource.

Usage:
  oc describe (-f FILENAME | TYPE [NAME_PREFIX | -l label] | TYPE/NAME) [flags]

Examples:
  # Provide details about the ruby-22-centos7 image repository
  oc describe imageRepository ruby-22-centos7

  # Provide details about the ruby-sample-build build configuration
  oc describe bc ruby-sample-build
```

- Get pod details using "oc describe pod"

```
[vagrant@openshift lab03-managing-pods]$ oc describe pod httpd
Name:               httpd
Namespace:          lab3-httpd
Priority:           0
PriorityClassName:  <none>
Node:               localhost/10.0.2.15
Start Time:         Fri, 07 Dec 2018 01:26:20 +0000
Labels:             app=httpd
Annotations:        openshift.io/scc=restricted
Status:             Running
IP:                 172.17.0.6
Containers:
  httpd:
    Container ID:   docker://90c65f9279bae9380ed2c65c2926135880614a61f81323651561be1d06db154d
    Image:          centos/httpd-24-centos7
    Image ID:       docker-pullable://docker.io/centos/httpd-24-centos7@sha256:f6393681ec205974a68386ac21e4ec2b76d42bfc885872ab8718f66826f95e68
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Fri, 07 Dec 2018 01:26:26 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-54fhc (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  default-token-54fhc:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-54fhc
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     <none>
Events:
  Type    Reason     Age   From                Message
  ----    ------     ----  ----                -------
  Normal  Scheduled  4m    default-scheduler   Successfully assigned lab3-httpd/httpd to localhost
  Normal  Pulling    4m    kubelet, localhost  pulling image "centos/httpd-24-centos7"
  Normal  Pulled     4m    kubelet, localhost  Successfully pulled image "centos/httpd-24-centos7"
  Normal  Created    4m    kubelet, localhost  Created container
  Normal  Started    4m    kubelet, localhost  Started container
```

Note! We need Pod IP address

- Access Pod service

```
[vagrant@openshift lab03-managing-pods]$ curl 172.17.0.6:8080 |head -n 10
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3985  100  3985    0     0  1783k      0 --:--:-- --:--:-- --:--:-- 3891k
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
		<title>Test Page for the Apache HTTP Server on Red Hat Enterprise Linux</title>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<style type="text/css">
			/*<![CDATA[*/
			body {
				background-color: #fff;
```

Note! This is the default welcome page for the image

- Export pod runtime configuration

```
[vagrant@openshift lab03-managing-pods]$ oc get pod httpd -o yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    openshift.io/scc: restricted
  creationTimestamp: 2018-12-07T01:26:20Z
  labels:
    app: httpd
  name: httpd
  namespace: lab3-httpd
  resourceVersion: "6467"
  selfLink: /api/v1/namespaces/lab3-httpd/pods/httpd
  uid: 19b7e03d-f9bf-11e8-8e8c-525400c042d5
spec:
  containers:
  - image: centos/httpd-24-centos7
    imagePullPolicy: Always
    name: httpd
    resources: {}
    securityContext:
      capabilities:
        drop:
        - KILL
        - MKNOD
        - SETGID
        - SETUID
      runAsUser: 1000170000
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-54fhc
      readOnly: true
  dnsPolicy: ClusterFirst
  imagePullSecrets:
  - name: default-dockercfg-5cxzt
  nodeName: localhost
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext:
    fsGroup: 1000170000
    seLinuxOptions:
      level: s0:c13,c7
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  volumes:
  - name: default-token-54fhc
    secret:
      defaultMode: 420
      secretName: default-token-54fhc
status:
  conditions:
  - lastProbeTime: null
    lastTransitionTime: 2018-12-07T01:26:20Z
    status: "True"
    type: Initialized
  - lastProbeTime: null
    lastTransitionTime: 2018-12-07T01:26:27Z
    status: "True"
    type: Ready
  - lastProbeTime: null
    lastTransitionTime: null
    status: "True"
    type: ContainersReady
  - lastProbeTime: null
    lastTransitionTime: 2018-12-07T01:26:20Z
    status: "True"
    type: PodScheduled
  containerStatuses:
  - containerID: docker://90c65f9279bae9380ed2c65c2926135880614a61f81323651561be1d06db154d
    image: docker.io/centos/httpd-24-centos7:latest
    imageID: docker-pullable://docker.io/centos/httpd-24-centos7@sha256:f6393681ec205974a68386ac21e4ec2b76d42bfc885872ab8718f66826f95e68
    lastState: {}
    name: httpd
    ready: true
    restartCount: 0
    state:
      running:
        startedAt: 2018-12-07T01:26:26Z
  hostIP: 10.0.2.15
  phase: Running
  podIP: 172.17.0.6
  qosClass: BestEffort
  startTime: 2018-12-07T01:26:20Z
```
