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

- You may also want to have an explaination of every pod attribute

```
[vagrant@openshift lab03-managing-pods]$ oc explain pod
KIND:     Pod
VERSION:  v1

DESCRIPTION:
     Pod is a collection of containers that can run on a host. This resource is
     created by clients and scheduled onto hosts.

FIELDS:
   apiVersion	<string>
     APIVersion defines the versioned schema of this representation of an
     object. Servers should convert recognized schemas to the latest internal
     value, and may reject unrecognized values. More info:
     https://git.k8s.io/community/contributors/devel/api-conventions.md#resources

   kind	<string>
     Kind is a string value representing the REST resource this object
     represents. Servers may infer this from the endpoint the client submits
     requests to. Cannot be updated. In CamelCase. More info:
     https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds

   metadata	<Object>
     Standard object's metadata. More info:
     https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata

   spec	<Object>
     Specification of the desired behavior of the pod. More info:
     https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status

   status	<Object>
     Most recently observed status of the pod. This data may not be up to date.
     Populated by the system. Read-only. More info:
     https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status
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

## Deleting pods

- Get pod list

```
[vagrant@openshift lab03-managing-pods]$ oc get pod
NAME      READY     STATUS    RESTARTS   AGE
httpd     1/1       Running   0          11m
```

- Check "oc delete -h"

```
[vagrant@openshift lab03-managing-pods]$ oc delete -h
Delete a resource

JSON and YAML formats are accepted.

If both a filename and command line arguments are passed, the command line arguments are used and
the filename is ignored.

Note that the delete command does NOT do resource version checks, so if someone submits an update to
a resource right when you submit a delete, their update will be lost along with the rest of the
resource.

Usage:
  oc delete ([-f FILENAME] | TYPE [(NAME | -l label | --all)]) [flags]

Examples:
  # Delete a pod using the type and ID specified in pod.json.
  oc delete -f pod.json

  # Delete a pod based on the type and ID in the JSON passed into stdin.
  cat pod.json | oc delete -f -

  # Delete pods and services with label name=myLabel.
  oc delete pods,services -l name=myLabel

  # Delete a pod with name node-1-vsjnm.
  oc delete pod node-1-vsjnm

  # Delete all resources associated with a running app, includes
  # buildconfig,deploymentconfig,service,imagestream,route and pod,
  # where 'appName' is listed in 'Labels' of 'oc describe [resource] [resource name]' output.
  oc delete all -l app=appName

  # Delete all pods
  oc delete pods --all
```

- Delete the "httpd" pod 

```
[vagrant@openshift lab03-managing-pods]$ oc delete pod httpd
pod "httpd" deleted
```

- Make sure that the httpd pod doesn't exist

```
[vagrant@openshift lab03-managing-pods]$ oc get pod
No resources found.
```


## Executing a custom command inside pod

- Create the httpd pod again

```
[vagrant@openshift lab03-managing-pods]$ oc create -f pod_httpd.yaml
pod/httpd created
```

- Make sure that pod is started

```
[vagrant@openshift lab03-managing-pods]$ oc get pods
NAME      READY     STATUS    RESTARTS   AGE
httpd     1/1       Running   0          28s
```

- Check the "oc exec -h" documenation

```
[vagrant@openshift lab03-managing-pods]$ oc exec -h
Execute a command in a container

Usage:
  oc exec [flags] POD [-c CONTAINER] -- COMMAND [args...]

Examples:
  # Get output from running 'date' in ruby-container from pod 'mypod'
  oc exec mypod -c ruby-container date

  # Switch to raw terminal mode, sends stdin to 'bash' in ruby-container from pod 'mypod' and sends
stdout/stderr from 'bash' back to the client
  oc exec mypod -c ruby-container -i -t -- bash -il

Options:
  -c, --container='': Container name. If omitted, the first container in the pod will be chosen
  -p, --pod='': Pod name (deprecated)
  -i, --stdin=false: Pass stdin to the container
  -t, --tty=false: Stdin is a TTY

Use "oc options" for a list of global command-line options (applies to all commands).
```

- Execute a custom command inside the httpd pod

```
[vagrant@openshift lab03-managing-pods]$ oc exec httpd cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)
```

- Try to access Pod shell

```
[vagrant@openshift lab03-managing-pods]$ oc exec -it httpd /bin/sh
sh-4.2$ ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
1000170+     1     0  0 01:40 ?        00:00:00 httpd -D FOREGROUND
1000170+    25     1  0 01:40 ?        00:00:00 /usr/bin/cat
1000170+    26     1  0 01:40 ?        00:00:00 /usr/bin/cat
1000170+    27     1  0 01:40 ?        00:00:00 /usr/bin/cat
1000170+    28     1  0 01:40 ?        00:00:00 /usr/bin/cat
1000170+    29     1  0 01:40 ?        00:00:00 httpd -D FOREGROUND
1000170+    30     1  0 01:40 ?        00:00:00 httpd -D FOREGROUND
1000170+    35     1  0 01:40 ?        00:00:00 httpd -D FOREGROUND
1000170+    43     1  0 01:40 ?        00:00:00 httpd -D FOREGROUND
1000170+    54     1  0 01:40 ?        00:00:00 httpd -D FOREGROUND
1000170+    95     0  0 01:43 ?        00:00:00 /bin/sh
1000170+   103    95  0 01:43 ?        00:00:00 ps -ef
sh-4.2$ date
Fri Dec  7 01:43:29 UTC 2018
sh-4.2$ exit
exit
```

Note! You may execute another set of command

- Check the "oc rsh -h"

```
[vagrant@openshift lab03-managing-pods]$ oc rsh -h
Open a remote shell session to a container

This command will attempt to start a shell session in a pod for the specified resource. It works
with pods, deployment configs, deployments, jobs, daemon sets, replication controllers and replica
sets. Any of the aforementioned resources (apart from pods) will be resolved to a ready pod. It will
default to the first container if none is specified, and will attempt to use '/bin/sh' as the
default shell. You may pass any flags supported by this command before the resource name, and an
optional command after the resource name, which will be executed instead of a login shell. A TTY
will be automatically allocated if standard input is interactive - use -t and -T to override. A TERM
variable is sent to the environment where the shell (or command) will be executed. By default its
value is the same as the TERM variable from the local environment; if not set, 'xterm' is used.

Note, some containers may not include a shell - use 'oc exec' if you need to run commands directly.

Usage:
  oc rsh [flags] POD [COMMAND]

Examples:
  # Open a shell session on the first container in pod 'foo'
  oc rsh foo

  # Run the command 'cat /etc/resolv.conf' inside pod 'foo'
  oc rsh foo cat /etc/resolv.conf

  # See the configuration of your internal registry
  oc rsh dc/docker-registry cat config.yml

  # Open a shell session on the container named 'index' inside a pod of your job
  # oc rsh -c index job/sheduled

Options:
  -c, --container='': Container name; defaults to first container
  -T, --no-tty=false: Disable pseudo-terminal allocation
      --shell='/bin/sh': Path to the shell command
      --timeout=10: Request timeout for obtaining a pod from the server; defaults to 10 seconds
  -t, --tty=false: Force a pseudo-terminal to be allocated

Use "oc options" for a list of global command-line options (applies to all commands).
```

- Execute a custom command in the httpd container

```
[vagrant@openshift lab03-managing-pods]$ oc rsh httpd cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)
```


## Getting pod logs

- Check the "oc logs -h" documentation

```
[vagrant@openshift lab03-managing-pods]$ oc logs -h
Print the logs for a resource

Supported resources are builds, build configs (bc), deployment configs (dc), and pods. When a pod is
specified and has more than one container, the container name should be specified via -c. When a
build config or deployment config is specified, you can view the logs for a particular version of it
via --version.

If your pod is failing to start, you may need to use the --previous option to see the logs of the
last attempt.

Aliases:
logs, log

Usage:
  oc logs [-f] [-p] (POD | TYPE/NAME) [-c CONTAINER] [flags]

Examples:
  # Start streaming the logs of the most recent build of the openldap build config.
  oc logs -f bc/openldap

  # Start streaming the logs of the latest deployment of the mysql deployment config.
  oc logs -f dc/mysql

  # Get the logs of the first deployment for the mysql deployment config. Note that logs
  # from older deployments may not exist either because the deployment was successful
  # or due to deployment pruning or manual deletion of the deployment.
  oc logs --version=1 dc/mysql

  # Return a snapshot of ruby-container logs from pod backend.
  oc logs backend -c ruby-container

  # Start streaming of ruby-container logs from pod backend.
  oc logs -f pod/backend -c ruby-container

Options:
      --all-containers=false: Get all containers's logs in the pod(s).
  -c, --container='': Print the logs of this container
  -f, --follow=false: Specify if the logs should be streamed.
      --limit-bytes=0: Maximum bytes of logs to return. Defaults to no limit.
      --pod-running-timeout=20s: The length of time (like 5s, 2m, or 3h, higher than zero) to wait
until at least one pod is running
  -p, --previous=false: If true, print the logs for the previous instance of the container in a pod
if it exists.
  -l, --selector='': Selector (label query) to filter on.
      --since=0s: Only return logs newer than a relative duration like 5s, 2m, or 3h. Defaults to
all logs. Only one of since-time / since may be used.
      --since-time='': Only return logs after a specific date (RFC3339). Defaults to all logs. Only
one of since-time / since may be used.
      --tail=-1: Lines of recent log file to display. Defaults to -1 with no selector, showing all
log lines otherwise 10, if a selector is provided.
      --timestamps=false: Include timestamps on each line in the log output
      --version=0: View the logs of a particular build or deployment by version if greater than zero

Use "oc options" for a list of global command-line options (applies to all commands).
```

- Try to access the httpd container logs

```
[vagrant@openshift lab03-managing-pods]$ oc logs -f httpd
=> sourcing 10-set-mpm.sh ...
=> sourcing 20-copy-config.sh ...
=> sourcing 40-ssl-certs.sh ...
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.6. Set the 'ServerName' directive globally to suppress this message
[Fri Dec 07 01:40:15.667449 2018] [ssl:warn] [pid 1] AH01909: 172.17.0.6:8443:0 server certificate does NOT include an ID which matches the server name
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.6. Set the 'ServerName' directive globally to suppress this message
[Fri Dec 07 01:40:15.763481 2018] [ssl:warn] [pid 1] AH01909: 172.17.0.6:8443:0 server certificate does NOT include an ID which matches the server name
[Fri Dec 07 01:40:15.763862 2018] [http2:warn] [pid 1] AH10034: The mpm module (prefork.c) is not supported by mod_http2. The mpm determines how things are processed in your server. HTTP/2 has more demands in this regard and the currently selected mpm will just not do. This is an advisory warning. Your server will continue to work, but the HTTP/2 protocol will be inactive.
[Fri Dec 07 01:40:15.764815 2018] [lbmethod_heartbeat:notice] [pid 1] AH02282: No slotmem from mod_heartmonitor
[Fri Dec 07 01:40:15.770224 2018] [mpm_prefork:notice] [pid 1] AH00163: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips configured -- resuming normal operations
[Fri Dec 07 01:40:15.770254 2018] [core:notice] [pid 1] AH00094: Command line: 'httpd -D FOREGROUND'
^C
```

Note! -f updates output on the fly
Note! you need to press CTRL + C to exit


## Cleanup

- Delete everything we've just created

```
[vagrant@openshift lab03-managing-pods]$ oc delete all --all
pod "httpd" deleted

[vagrant@openshift lab03-managing-pods]$ oc get pod
No resources found.

[vagrant@openshift lab03-managing-pods]$ oc project
Using project "lab3-httpd" on server "https://localhost:8443".

[vagrant@openshift lab03-managing-pods]$ oc delete project lab3-httpd
project.project.openshift.io "lab3-httpd" deleted

[vagrant@openshift lab03-managing-pods]$ oc project
error: you do not have rights to view project "lab3-httpd".

[vagrant@openshift lab03-managing-pods]$ oc get projects
No resources found.
```

