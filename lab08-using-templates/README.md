# lab08-using-templates
Lab 8 - Using Templates

## Files
All files required for this lab are stored directly in this directory or in /vagrant/lab08-using-templates directory of your vagrant machine

## Preparation

It is assumed that all activities will be performed inside /vagrant/lab08-using-templates on your vagrant machine

- Run the following command to change current directory

```
cd /vagrant/lab08-using-templates
```

- Create a new project named "lab8"

```
oc new-project lab8
```

## Understanding templates

- List all available templates

```
[vagrant@openshift lab08-using-templates]$ oc get template -n openshift
NAME                       DESCRIPTION                                                                        PARAMETERS        OBJECTS
cakephp-mysql-persistent   An example CakePHP application with a MySQL database. For more information ab...   20 (4 blank)      9
dancer-mysql-persistent    An example Dancer application with a MySQL database. For more information abo...   17 (5 blank)      9
django-psql-persistent     An example Django application with a PostgreSQL database. For more informatio...   18 (5 blank)      9
jenkins-persistent         Jenkins service, with persistent storage....                                       7 (all set)       7
jenkins-pipeline-example   This example showcases the new Jenkins Pipeline integration in OpenShift,...       16 (4 blank)      8
mariadb-persistent         MariaDB database service, with persistent storage. For more information about...   9 (3 generated)   4
mongodb-persistent         MongoDB database service, with persistent storage. For more information about...   9 (3 generated)   4
mysql-persistent           MySQL database service, with persistent storage. For more information about u...   9 (3 generated)   4
nodejs-mongo-persistent    An example Node.js application with a MongoDB database. For more information...    17 (4 blank)      9
postgresql-persistent      PostgreSQL database service, with persistent storage. For more information ab...   8 (2 generated)   4
rails-pgsql-persistent     An example Rails application with a PostgreSQL database. For more information...   21 (4 blank)      9
```

Note! List of templates may be different on your platfrom
Note! By default, templates are stored in the "openshift" project

- Gather template details

```
[vagrant@openshift lab08-using-templates]$ oc describe template jenkins-persistent -n openshift
Name:		jenkins-persistent
Namespace:	openshift
Created:	3 hours ago
Labels:		<none>
Description:	Jenkins service, with persistent storage.

		NOTE: You must have persistent volumes available in your cluster to use this template.
Annotations:	iconClass=icon-jenkins
		openshift.io/display-name=Jenkins
		openshift.io/documentation-url=https://docs.openshift.org/latest/using_images/other_images/jenkins.html
		openshift.io/long-description=This template deploys a Jenkins server capable of managing OpenShift Pipeline builds and supporting OpenShift-based oauth login.
		openshift.io/provider-display-name=Red Hat, Inc.
		openshift.io/support-url=https://access.redhat.com
		tags=instant-app,jenkins

Parameters:
    Name:		JENKINS_SERVICE_NAME
    Display Name:	Jenkins Service Name
    Description:	The name of the OpenShift Service exposed for the Jenkins container.
    Required:		false
    Value:		jenkins

    Name:		JNLP_SERVICE_NAME
    Display Name:	Jenkins JNLP Service Name
    Description:	The name of the service used for master/slave communication.
    Required:		false
    Value:		jenkins-jnlp

    Name:		ENABLE_OAUTH
    Display Name:	Enable OAuth in Jenkins
    Description:	Whether to enable OAuth OpenShift integration. If false, the static account 'admin' will be initialized with the password 'password'.
    Required:		false
    Value:		true

    Name:		MEMORY_LIMIT
    Display Name:	Memory Limit
    Description:	Maximum amount of memory the container can use.
    Required:		false
    Value:		512Mi

    Name:		VOLUME_CAPACITY
    Display Name:	Volume Capacity
    Description:	Volume space available for data, e.g. 512Mi, 2Gi.
    Required:		true
    Value:		1Gi

    Name:		NAMESPACE
    Display Name:	Jenkins ImageStream Namespace
    Description:	The OpenShift Namespace where the Jenkins ImageStream resides.
    Required:		false
    Value:		openshift

    Name:		JENKINS_IMAGE_STREAM_TAG
    Display Name:	Jenkins ImageStreamTag
    Description:	Name of the ImageStreamTag to be used for the Jenkins image.
    Required:		false
    Value:		jenkins:2


Object Labels:	app=jenkins-persistent,template=jenkins-persistent-template

Message:	A Jenkins service has been created in your project.  Log into Jenkins with your OpenShift account.  The tutorial at https://github.com/openshift/origin/blob/master/examples/jenkins/README.md contains more information about using this template.

Objects:
    Route			${JENKINS_SERVICE_NAME}
    PersistentVolumeClaim	${JENKINS_SERVICE_NAME}
    DeploymentConfig		${JENKINS_SERVICE_NAME}
    ServiceAccount		${JENKINS_SERVICE_NAME}
    RoleBinding			${JENKINS_SERVICE_NAME}_edit
    Service			${JNLP_SERVICE_NAME}
    Service			${JENKINS_SERVICE_NAME}
```

- Export template data

```
[vagrant@openshift lab08-using-templates]$ oc get template jenkins-persistent -n openshift -o yaml
apiVersion: template.openshift.io/v1
kind: Template
labels:
  app: jenkins-persistent
  template: jenkins-persistent-template
message: A Jenkins service has been created in your project.  Log into Jenkins with
  your OpenShift account.  The tutorial at https://github.com/openshift/origin/blob/master/examples/jenkins/README.md
  contains more information about using this template.
metadata:
  annotations:
    description: |-
      Jenkins service, with persistent storage.

      NOTE: You must have persistent volumes available in your cluster to use this template.
    iconClass: icon-jenkins
    openshift.io/display-name: Jenkins
    openshift.io/documentation-url: https://docs.openshift.org/latest/using_images/other_images/jenkins.html
    openshift.io/long-description: This template deploys a Jenkins server capable
      of managing OpenShift Pipeline builds and supporting OpenShift-based oauth login.
    openshift.io/provider-display-name: Red Hat, Inc.
    openshift.io/support-url: https://access.redhat.com
    tags: instant-app,jenkins
  creationTimestamp: 2018-12-08T00:50:17Z
  name: jenkins-persistent
  namespace: openshift
  resourceVersion: "314"
  selfLink: /apis/template.openshift.io/v1/namespaces/openshift/templates/jenkins-persistent
  uid: 3b2d14a5-fa83-11e8-914e-525400c042d5
objects:
- apiVersion: v1
  kind: Route
  metadata:
    annotations:
      haproxy.router.openshift.io/timeout: 4m
      template.openshift.io/expose-uri: http://{.spec.host}{.spec.path}
    name: ${JENKINS_SERVICE_NAME}
  spec:
    tls:
      insecureEdgeTerminationPolicy: Redirect
      termination: edge
    to:
      kind: Service
      name: ${JENKINS_SERVICE_NAME}
- apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: ${JENKINS_SERVICE_NAME}
  spec:
    accessModes:
    - ReadWriteOnce
    resources:
      requests:
        storage: ${VOLUME_CAPACITY}
- apiVersion: v1
  kind: DeploymentConfig
  metadata:
    annotations:
      template.alpha.openshift.io/wait-for-ready: "true"
    name: ${JENKINS_SERVICE_NAME}
  spec:
    replicas: 1
    selector:
      name: ${JENKINS_SERVICE_NAME}
    strategy:
      type: Recreate
    template:
      metadata:
        labels:
          name: ${JENKINS_SERVICE_NAME}
      spec:
        containers:
        - capabilities: {}
          env:
          - name: OPENSHIFT_ENABLE_OAUTH
            value: ${ENABLE_OAUTH}
          - name: OPENSHIFT_ENABLE_REDIRECT_PROMPT
            value: "true"
          - name: KUBERNETES_MASTER
            value: https://kubernetes.default:443
          - name: KUBERNETES_TRUST_CERTIFICATES
            value: "true"
          - name: JENKINS_SERVICE_NAME
            value: ${JENKINS_SERVICE_NAME}
          - name: JNLP_SERVICE_NAME
            value: ${JNLP_SERVICE_NAME}
          image: ' '
          imagePullPolicy: IfNotPresent
          livenessProbe:
            failureThreshold: 2
            httpGet:
              path: /login
              port: 8080
            initialDelaySeconds: 420
            periodSeconds: 360
            timeoutSeconds: 240
          name: jenkins
          readinessProbe:
            httpGet:
              path: /login
              port: 8080
            initialDelaySeconds: 3
            timeoutSeconds: 240
          resources:
            limits:
              memory: ${MEMORY_LIMIT}
          securityContext:
            capabilities: {}
            privileged: false
          terminationMessagePath: /dev/termination-log
          volumeMounts:
          - mountPath: /var/lib/jenkins
            name: ${JENKINS_SERVICE_NAME}-data
        dnsPolicy: ClusterFirst
        restartPolicy: Always
        serviceAccountName: ${JENKINS_SERVICE_NAME}
        volumes:
        - name: ${JENKINS_SERVICE_NAME}-data
          persistentVolumeClaim:
            claimName: ${JENKINS_SERVICE_NAME}
    triggers:
    - imageChangeParams:
        automatic: true
        containerNames:
        - jenkins
        from:
          kind: ImageStreamTag
          name: ${JENKINS_IMAGE_STREAM_TAG}
          namespace: ${NAMESPACE}
        lastTriggeredImage: ""
      type: ImageChange
    - type: ConfigChange
- apiVersion: v1
  kind: ServiceAccount
  metadata:
    annotations:
      serviceaccounts.openshift.io/oauth-redirectreference.jenkins: '{"kind":"OAuthRedirectReference","apiVersion":"v1","reference":{"kind":"Route","name":"${JENKINS_SERVICE_NAME}"}}'
    name: ${JENKINS_SERVICE_NAME}
- apiVersion: v1
  groupNames: null
  kind: RoleBinding
  metadata:
    name: ${JENKINS_SERVICE_NAME}_edit
  roleRef:
    name: edit
  subjects:
  - kind: ServiceAccount
    name: ${JENKINS_SERVICE_NAME}
- apiVersion: v1
  kind: Service
  metadata:
    name: ${JNLP_SERVICE_NAME}
  spec:
    ports:
    - name: agent
      nodePort: 0
      port: 50000
      protocol: TCP
      targetPort: 50000
    selector:
      name: ${JENKINS_SERVICE_NAME}
    sessionAffinity: None
    type: ClusterIP
- apiVersion: v1
  kind: Service
  metadata:
    annotations:
      service.alpha.openshift.io/dependencies: '[{"name": "${JNLP_SERVICE_NAME}",
        "namespace": "", "kind": "Service"}]'
      service.openshift.io/infrastructure: "true"
    name: ${JENKINS_SERVICE_NAME}
  spec:
    ports:
    - name: web
      nodePort: 0
      port: 80
      protocol: TCP
      targetPort: 8080
    selector:
      name: ${JENKINS_SERVICE_NAME}
    sessionAffinity: None
    type: ClusterIP
parameters:
- description: The name of the OpenShift Service exposed for the Jenkins container.
  displayName: Jenkins Service Name
  name: JENKINS_SERVICE_NAME
  value: jenkins
- description: The name of the service used for master/slave communication.
  displayName: Jenkins JNLP Service Name
  name: JNLP_SERVICE_NAME
  value: jenkins-jnlp
- description: Whether to enable OAuth OpenShift integration. If false, the static
    account 'admin' will be initialized with the password 'password'.
  displayName: Enable OAuth in Jenkins
  name: ENABLE_OAUTH
  value: "true"
- description: Maximum amount of memory the container can use.
  displayName: Memory Limit
  name: MEMORY_LIMIT
  value: 512Mi
- description: Volume space available for data, e.g. 512Mi, 2Gi.
  displayName: Volume Capacity
  name: VOLUME_CAPACITY
  required: true
  value: 1Gi
- description: The OpenShift Namespace where the Jenkins ImageStream resides.
  displayName: Jenkins ImageStream Namespace
  name: NAMESPACE
  value: openshift
- description: Name of the ImageStreamTag to be used for the Jenkins image.
  displayName: Jenkins ImageStreamTag
  name: JENKINS_IMAGE_STREAM_TAG
  value: jenkins:2
```

Note! This template is given for demosntration only. We are not going to use this template since it requires S2I


## Deploying applications with templates

- Check existing gogs template

```
cat gogs_template.yaml
```

- List template parameters

```
[vagrant@openshift lab08-using-templates]$ oc process --parameters -f gogs_template.yaml
NAME                       DESCRIPTION                                                                                                                             GENERATOR           VALUE
APPLICATION_NAME           The name for the application.                                                                                                                               gogs
HOSTNAME                   Custom hostname for http service route.  Leave blank for default hostname, e.g.: <application-name>-<project>.<default-domain-suffix>
DATABASE_USER                                                                                                                                                                          gogs
DATABASE_PASSWORD                                                                                                                                                                      gogs
DATABASE_NAME                                                                                                                                                                          gogs
DATABASE_ADMIN_PASSWORD                                                                                                                                            expression          [a-zA-Z0-9]{8}
DATABASE_MAX_CONNECTIONS                                                                                                                                                               100
DATABASE_SHARED_BUFFERS                                                                                                                                                                12MB
GOGS_VERSION               Version of the Gogs container image to be used (check the available version https://hub.docker.com/r/openshiftdemos/gogs/tags)                              0.9.97
INSTALL_LOCK               If set to true, installation (/install) page will be disabled. Set to false if you want to run the installation wizard via web                              true
SKIP_TLS_VERIFY            Skip TLS verification on webhooks. Enable with caution!                                                                                                     false
```

- Deploy gogs from the template

```
[vagrant@openshift lab08-using-templates]$ oc new-app -f gogs_template.yaml -p HOSTNAME=gogs.apps.172.24.0.11.nip.io
--> Deploying template "lab8/gogs" for "gogs_template.yaml" to project lab8

     gogs
     ---------
     The Gogs git server (https://gogs.io/)

     * With parameters:
        * APPLICATION_NAME=gogs
        * HOSTNAME=gogs.apps.172.24.0.11.nip.io
        * Database Username=gogs
        * Database Password=gogs
        * Database Name=gogs
        * Database Admin Password=VxCHDL3p # generated
        * Maximum Database Connections=100
        * Shared Buffer Amount=12MB
        * Gogs Version=0.9.97
        * Installation lock=true
        * Skip TLS verification on webhooks=false

--> Creating resources ...
    serviceaccount "gogs" created
    service "gogs-postgresql" created
    deploymentconfig "gogs-postgresql" created
    service "gogs" created
    route "gogs" created
    deploymentconfig "gogs" created
    imagestream "gogs" created
    configmap "gogs-config" created
--> Success
    Access your application via route 'gogs.apps.172.24.0.11.nip.io'
    Run 'oc status' to view your app.
```

- Make sure that application pods are available

```
[vagrant@openshift lab08-using-templates]$ oc get pod
NAME                      READY     STATUS    RESTARTS   AGE
gogs-1-c6jdm              1/1       Running   0          35s
gogs-postgresql-1-wqk4x   1/1       Running   0          36s
```

- Make sure that a route is created

```
[vagrant@openshift lab08-using-templates]$ oc get route
NAME      HOST/PORT                      PATH      SERVICES   PORT      TERMINATION   WILDCARD
gogs      gogs.apps.172.24.0.11.nip.io             gogs       <all>                   None
```

- Try to access application using the route address

Note! You should see the "Gogs - Go Git Service" page


## Cleanup

```
oc delete project lab8
```


