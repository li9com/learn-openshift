# lab05-managing-routes

Lab 5 - Managing routes

## Files

All files required for this lab are stored directly in this directory or in /vagrant/lab05-managing-routes directory of your vagrant machine

## Default routes

The lab installation uses apps.172.24.0.11.nip.io as the default application domain.

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab05-managing-routes on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab05-managing-routes
```

- Create a new project named "lab5"

```
oc new-project lab5
```

## Exposing services to routes

- Create a jenkins pod

```
[vagrant@openshift lab05-managing-routes]$ oc create -f pod_jenkins.yaml
pod/jenkins created
```

- Make sure that pod is started

```
[vagrant@openshift lab05-managing-routes]$ oc get pod
NAME      READY     STATUS              RESTARTS   AGE
jenkins   0/1       ContainerCreating   0          6s

[vagrant@openshift lab05-managing-routes]$ oc get pod
NAME      READY     STATUS    RESTARTS   AGE
jenkins   1/1       Running   0          41s
```

- Expose pod to service

```
[vagrant@openshift lab05-managing-routes]$ oc expose pod jenkins
error: couldn't find port via --port flag or introspection
See 'oc expose -h' for help and examples.
[vagrant@openshift lab05-managing-routes]$ oc expose pod jenkins --port 8080
service/jenkins exposed
```

- Make sure that service has been created

```
[vagrant@openshift lab05-managing-routes]$ oc get svc
NAME      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
jenkins   ClusterIP   172.30.33.155   <none>        8080/TCP   4s
```

- Check the documentation how to expose service to route

```
[vagrant@openshift lab05-managing-routes]$ oc expose svc -h
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
json|yaml|name|template|go-template|go-template-file|templatefile|jsonpath|jsonpath-file.
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

- Expose jenkins service to a route

```
[vagrant@openshift lab05-managing-routes]$ oc expose service jenkins
route.route.openshift.io/jenkins exposed
```

- Check that route has been created

```
[vagrant@openshift lab05-managing-routes]$ oc get route
NAME      HOST/PORT                              PATH      SERVICES   PORT      TERMINATION   WILDCARD
jenkins   jenkins-lab5.apps.172.24.0.11.nip.io             jenkins    8080                    None
```

Note! We used default hostname generated by OpenShift. By default, the route is named as "<servicename>-<projectname>.<subdomain>"

- Try to access the jenkins service using your web browser

- Create a new route to the same service with a custom hostname

```
[vagrant@openshift lab05-managing-routes]$ oc expose service jenkins --name jenkins1 --hostname jenkins.apps.172.24.0.11.nip.io
route.route.openshift.io/jenkins1 exposed
[vagrant@openshift lab05-managing-routes]$ oc get route
NAME       HOST/PORT                              PATH      SERVICES   PORT      TERMINATION   WILDCARD
jenkins    jenkins-lab5.apps.172.24.0.11.nip.io             jenkins    8080                    None
jenkins1   jenkins.apps.172.24.0.11.nip.io                  jenkins    8080                    None
```

- Make sure that the jenkins applications is accessible using both links


## Describing routes

- Check route details using "oc describe route"

```
[vagrant@openshift lab05-managing-routes]$ oc describe route jenkins
Name:			jenkins
Namespace:		lab5
Created:		12 minutes ago
Labels:			app=jenkins
Annotations:		openshift.io/host.generated=true
Requested Host:		jenkins-lab5.apps.172.24.0.11.nip.io
			  exposed on router router 12 minutes ago
Path:			<none>
TLS Termination:	<none>
Insecure Policy:	<none>
Endpoint Port:		8080

Service:	jenkins
Weight:		100 (100%)
Endpoints:	172.17.0.6:8080



[vagrant@openshift lab05-managing-routes]$ oc describe route jenkins1
Name:			jenkins1
Namespace:		lab5
Created:		8 minutes ago
Labels:			app=jenkins
Annotations:		<none>
Requested Host:		jenkins.apps.172.24.0.11.nip.io
			  exposed on router router 8 minutes ago
Path:			<none>
TLS Termination:	<none>
Insecure Policy:	<none>
Endpoint Port:		8080

Service:	jenkins
Weight:		100 (100%)
Endpoints:	172.17.0.6:8080
```

- Export runtime route configuration

```
[vagrant@openshift lab05-managing-routes]$ oc get route jenkins -o yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  annotations:
    openshift.io/host.generated: "true"
  creationTimestamp: 2018-12-07T12:26:25Z
  labels:
    app: jenkins
  name: jenkins
  namespace: lab5
  resourceVersion: "166317"
  selfLink: /apis/route.openshift.io/v1/namespaces/lab5/routes/jenkins
  uid: 50420c2e-fa1b-11e8-a35b-525400c042d5
spec:
  host: jenkins-lab5.apps.172.24.0.11.nip.io
  port:
    targetPort: 8080
  to:
    kind: Service
    name: jenkins
    weight: 100
  wildcardPolicy: None
status:
  ingress:
  - conditions:
    - lastTransitionTime: 2018-12-07T12:26:25Z
      status: "True"
      type: Admitted
    host: jenkins-lab5.apps.172.24.0.11.nip.io
    routerName: router
    wildcardPolicy: None

```

## Deleting routes

- Delete the "jenkins1" route

```
[vagrant@openshift lab05-managing-routes]$ oc delete route jenkins1
route.route.openshift.io "jenkins1" deleted

[vagrant@openshift lab05-managing-routes]$ oc get route
NAME      HOST/PORT                              PATH      SERVICES   PORT      TERMINATION   WILDCARD
jenkins   jenkins-lab5.apps.172.24.0.11.nip.io             jenkins    8080                    None
```

- Delete the "jenkins" route

```
[vagrant@openshift lab05-managing-routes]$ oc get pod
NAME      READY     STATUS    RESTARTS   AGE
jenkins   1/1       Running   0          24m

[vagrant@openshift lab05-managing-routes]$ oc delete route jenkins
route.route.openshift.io "jenkins" deleted
```

## Creating routes manually

- Check route_jenkins.yaml

```
cat route_jenkins.yaml
```

- Create route

```
[vagrant@openshift lab05-managing-routes]$ oc create -f route_jenkins.yaml
route.route.openshift.io/jenkins created
```

- Make sure that route exists

```
[vagrant@openshift lab05-managing-routes]$ oc get route
NAME      HOST/PORT                         PATH      SERVICES   PORT      TERMINATION   WILDCARD
jenkins   jenkins.apps.172.24.0.11.nip.io             jenkins    <all>                   None
```

- Try to access the jenkins application

- Get route details

```
[vagrant@openshift lab05-managing-routes]$ oc describe route jenkins
Name:			jenkins
Namespace:		lab5
Created:		About a minute ago
Labels:			<none>
Annotations:		<none>
Requested Host:		jenkins.apps.172.24.0.11.nip.io
			  exposed on router router about a minute ago
Path:			<none>
TLS Termination:	<none>
Insecure Policy:	<none>
Endpoint Port:		<all endpoint ports>

Service:	jenkins
Weight:		100 (100%)
Endpoints:	172.17.0.6:8080
```

- Delete the route

```
[vagrant@openshift lab05-managing-routes]$ oc delete route jenkins
route.route.openshift.io "jenkins" deleted
```


## Cleanup

- Remove the "lab5" project

```
oc delete project lab5
```
