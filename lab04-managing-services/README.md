# lab04-managing-services
Lab 4 - Managing services

## Files
All files required for this lab are stored directly in this directory or in /vagrant/lab04-managing-services/ directory of your vagrant machine

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab04-managing-services on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab04-managing-services
```

- Create a new project named "lab4"

```
[vagrant@openshift lab04-managing-services]$ oc new-project lab4
Now using project "lab4" on server "https://localhost:8443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app centos/ruby-25-centos7~https://github.com/sclorg/ruby-ex.git

to build a new example application in Ruby.
```

## Exposing pods automatically

- Check the content of pod_httpd1.yaml

```
cat pod_httpd1.yaml
```

- Create an httpd pod

```
[vagrant@openshift lab04-managing-services]$ oc create -f pod_httpd1.yaml
pod/httpd1 created
```

- Make sure that the httpd1 pod works as expectec

```
[vagrant@openshift lab04-managing-services]$ oc get pod
NAME      READY     STATUS    RESTARTS   AGE
httpd1    1/1       Running   0          3s

[vagrant@openshift lab04-managing-services]$ oc describe pod httpd|grep IP
IP:                 172.17.0.6


[vagrant@openshift lab04-managing-services]$ curl 172.17.0.6:8080|head -n5
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3985  100  3985    0     0  1917k      0 --:--:-- --:--:-- --:--:-- 3891k
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
		<title>Test Page for the Apache HTTP Server on Red Hat Enterprise Linux</title>

```

- Check the "oc expose -h" documentation


```
[vagrant@openshift lab04-managing-services]$ oc expose -h
Expose containers internally as services or externally via routes

There is also the ability to expose a deployment configuration, replication controller, service, or pod as a new service
on a specified port. If no labels are specified, the new object will re-use the labels from the object it exposes.

Usage:
  oc expose (-f FILENAME | TYPE NAME) [--port=port] [--protocol=TCP|UDP] [--target-port=number-or-name] [--name=name]
[--external-ip=external-ip-of-service] [--type=type] [flags]

Examples:
  # Create a route based on service nginx. The new route will re-use nginx's labels
  oc expose service nginx

  # Create a route and specify your own label and route name
  oc expose service nginx -l name=myroute --name=fromdowntown

  # Create a route and specify a hostname
  oc expose service nginx --hostname=www.example.com

  # Create a route with wildcard
  oc expose service nginx --hostname=x.example.com --wildcard-policy=Subdomain
  This would be equivalent to *.example.com. NOTE: only hosts are matched by the wildcard, subdomains would not be
included.

  # Expose a deployment configuration as a service and use the specified port
  oc expose dc ruby-hello-world --port=8080

  # Expose a service as a route in the specified path
  oc expose service nginx --path=/nginx

  # Expose a service using different generators
  oc expose service nginx --name=exposed-svc --port=12201 --protocol="TCP" --generator="service/v2"
  oc expose service nginx --name=my-route --port=12201 --generator="route/v1"

  Exposing a service using the "route/v1" generator (default) will create a new exposed route with the "--name" provided
  (or the name of the service otherwise). You may not specify a "--protocol" or "--target-port" option when using this
generator.

Options:
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --cluster-ip='': ClusterIP to be assigned to the service. Leave empty to auto-allocate, or set to 'None' to create
a headless service.
      --dry-run=false: If true, only print the object that would be sent, without sending it.
      --external-ip='': Additional external IP address (not managed by Kubernetes) to accept for the service. If this IP
is routed to a node, the service can be accessed by this IP in addition to its generated service IP.
  -f, --filename=[]: Filename, directory, or URL to files identifying the resource to expose a service
      --generator='': The name of the API generator to use. Defaults to "route/v1". Available generators include
"service/v1", "service/v2", and "route/v1". "service/v1" will automatically name the port "default", while "service/v2"
will leave it unnamed.
      --hostname='': Set a hostname for the new route
  -l, --labels='': Labels to apply to the service created by this call.
      --load-balancer-ip='': IP to assign to the LoadBalancer. If empty, an ephemeral IP will be created and used
(cloud-provider specific).
      --name='': The name for the newly created object.
  -o, --output='': Output format. One of:
json|yaml|name|templatefile|template|go-template|go-template-file|jsonpath-file|jsonpath.
      --overrides='': An inline JSON override for the generated object. If this is non-empty, it is used to override the
generated object. Requires that the object supply a valid apiVersion field.
      --path='': Set a path for the new route
      --port='': The port that the resource should serve on.
      --protocol='': The network protocol for the service to be created. Default is 'TCP'.
      --record=false: Record current kubectl command in the resource annotation. If set to false, do not record the
command. If set to true, record the command. If not set, default to updating the existing annotation value only if one
already exists.
  -R, --recursive=false: Process the directory used in -f, --filename recursively. Useful when you want to manage
related manifests organized within the same directory.
      --save-config=false: If true, the configuration of current object will be saved in its annotation. Otherwise, the
annotation will be unchanged. This flag is useful when you want to perform kubectl apply on this object in the future.
      --selector='': A label selector to use for this service. Only equality-based selector requirements are supported.
If empty (the default) infer the selector from the replication controller or replica set.)
      --session-affinity='': If non-empty, set the session affinity for the service to this; legal values: 'None',
'ClientIP'
      --target-port='': Name or number for the port on the container that the service should direct traffic to.
Optional.
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
      --type='': Type for this service: ClusterIP, NodePort, LoadBalancer, or ExternalName. Default is 'ClusterIP'.
      --wildcard-policy='': Sets the WildcardPolicy for the hostname, the default is "None". Valid values are "None" and
"Subdomain"

Use "oc options" for a list of global command-line options (applies to all commands).
```

- Create a service automatically using oc expose

```
[vagrant@openshift lab04-managing-services]$ oc get pod
NAME      READY     STATUS    RESTARTS   AGE
httpd1    1/1       Running   0          3m

[vagrant@openshift lab04-managing-services]$ oc expose pod httpd1 --port 8080
service/httpd1 exposed
```

- Make sure that service was created

```
[vagrant@openshift lab04-managing-services]$ oc get svc
NAME      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
httpd1    ClusterIP   172.30.221.123   <none>        8080/TCP   7s
```

- Try to access application using the service address

```
[vagrant@openshift lab04-managing-services]$ curl 172.30.221.123:8080 |head -n5
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3985  100  3985    0     0  2323k      0 --:--:-- --:--:-- --:--:-- 3891k
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
		<title>Test Page for the Apache HTTP Server on Red Hat Enterprise Linux</title>
```

Note! Make sure that it is still the pod's answer


## Gathering service details

- Gather service list

```
[vagrant@openshift lab04-managing-services]$ oc get svc
NAME      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
httpd1    ClusterIP   172.30.221.123   <none>        8080/TCP   3m
```

- Gather service configuration

```
[vagrant@openshift lab04-managing-services]$ oc describe svc httpd1
Name:              httpd1
Namespace:         lab4
Labels:            app=httpd
Annotations:       <none>
Selector:          app=httpd
Type:              ClusterIP
IP:                172.30.221.123
Port:              <unset>  8080/TCP
TargetPort:        8080/TCP
Endpoints:         172.17.0.6:8080
Session Affinity:  None
Events:            <none>
```

Note! Make sure that Selector value is "app=httpd"

- Get service runtime configuration

```
[vagrant@openshift lab04-managing-services]$ oc get svc httpd1 -o yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: 2018-12-07T02:17:35Z
  labels:
    app: httpd
  name: httpd1
  namespace: lab4
  resourceVersion: "18967"
  selfLink: /api/v1/namespaces/lab4/services/httpd1
  uid: 42f10914-f9c6-11e8-8e8c-525400c042d5
spec:
  clusterIP: 172.30.221.123
  ports:
  - port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: httpd
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
```


## Adding the second pod

- Check pod_jenkins1.yaml

```
cat pod_jenkins1.yaml
```

Note! Make sure that app label is set to "httpd"
Note! We are now going to add a jenkins container with the same label app=httpd. This doens't make sense in the real world but it is still acceptable from the Lab perspective.
Note! Again, this is incorrect for the real world. Do not perform that in production

- Create a jenkins pod

```
[vagrant@openshift lab04-managing-services]$ oc create -f pod_jenkins1.yaml
pod/jenkins1 created
```

- Allow jenkins to start

```
[vagrant@openshift lab04-managing-services]$ oc get pod
NAME       READY     STATUS    RESTARTS   AGE
httpd1     1/1       Running   0          31m
jenkins1   1/1       Running   0          1m
```

- Get Service IP address

```
[vagrant@openshift lab04-managing-services]$ oc get svc
NAME      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
httpd1    ClusterIP   172.30.221.123   <none>        8080/TCP   34m
```


- Make sure that traffic is load balanced between both pods with app=httpd label (jenkins1 and httpd1). You need to run several times the following command and compare the output
Note! It doesn't make sense to compare exact output. We need 2 different containers to only demonstrate that traffic is load balanced

```
curl -sI  172.30.221.123:8080|grep Server
```

You may see the following example output:

```
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Jetty(9.4.z-SNAPSHOT)
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Jetty(9.4.z-SNAPSHOT)
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Jetty(9.4.z-SNAPSHOT)
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
```

- Delete jenkins1 pod and make sure that service returns only httpd answer

```
[vagrant@openshift lab04-managing-services]$ oc delete pod jenkins1
pod "jenkins1" deleted
[vagrant@openshift lab04-managing-services]$ oc get pod
NAME      READY     STATUS    RESTARTS   AGE
httpd1    1/1       Running   0          39m
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
[vagrant@openshift lab04-managing-services]$ curl -sI  172.30.221.123:8080|grep Server
Server: Apache/2.4.34 (Red Hat) OpenSSL/1.0.2k-fips
```

Note! We tried many times and we have not seen any jenkins answers


## Creating services manually

- Check service_httpd.yaml

```
cat service_httpd.yaml
```

Note! service_httpd.yaml defines a service named httpd which uses app=httpd as the selector

- Create  the httpd service
Note! We already have http1 service

```
[vagrant@openshift lab04-managing-services]$ oc create -f service_httpd.yaml
service/httpd created

[vagrant@openshift lab04-managing-services]$ oc get svc
NAME      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
httpd     ClusterIP   172.30.193.228   <none>        8080/TCP   3s
httpd1    ClusterIP   172.30.221.123   <none>        8080/TCP   41m
```

- Compare both services

```
[vagrant@openshift lab04-managing-services]$ oc describe svc httpd
Name:              httpd
Namespace:         lab4
Labels:            app=httpd
Annotations:       <none>
Selector:          app=httpd
Type:              ClusterIP
IP:                172.30.193.228
Port:              <unset>  8080/TCP
TargetPort:        8080/TCP
Endpoints:         172.17.0.6:8080
Session Affinity:  None
Events:            <none>



[vagrant@openshift lab04-managing-services]$ oc describe svc httpd1
Name:              httpd1
Namespace:         lab4
Labels:            app=httpd
Annotations:       <none>
Selector:          app=httpd
Type:              ClusterIP
IP:                172.30.221.123
Port:              <unset>  8080/TCP
TargetPort:        8080/TCP
Endpoints:         172.17.0.6:8080
Session Affinity:  None
Events:            <none>

```

Note! They are almost the same



## Deleting services

- Delete both servicee using "oc delete svc"

```
[vagrant@openshift lab04-managing-services]$ oc get svc
NAME      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
httpd     ClusterIP   172.30.193.228   <none>        8080/TCP   3m
httpd1    ClusterIP   172.30.221.123   <none>        8080/TCP   44m

[vagrant@openshift lab04-managing-services]$ oc delete svc httpd
service "httpd" deleted

[vagrant@openshift lab04-managing-services]$ oc get svc
NAME      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
httpd1    ClusterIP   172.30.221.123   <none>        8080/TCP   44m

[vagrant@openshift lab04-managing-services]$ oc delete svc httpd1
service "httpd1" deleted

[vagrant@openshift lab04-managing-services]$ oc get svc
No resources found.
```

## Cleanup

- Delete the project

```
oc delete project lab4
```


