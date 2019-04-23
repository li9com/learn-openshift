# lab02-managing-roles

Lab 2 - Managing roles

## Roles and Cluster Roles

OpenShift has roles of two types:

* __Cluster Roles__ are the roles which available everywhere and can give access on both _cluster-wide_ and _project-wide_ levels.
* __Roles__ are the roles which were created for a project and therefore can work only on the resources within the project.


## Cluster Roles

Cluster roles can be created, modified, updated, deleted by the cluster-admins. OpenShift is supplied with a set of predefined cluster roles. A set of cluster roles can vary from cluster to cluster depending on a number of installed components.

### Discovering exising Cluster Roles

- We can get a list of existing cluster roles

```
$ oc get clusterroles.rbac
NAME                                                                   AGE
admin                                                                  8d
alertmanager-main                                                      7d
basic-user                                                             8d
cluster-admin                                                          8d
cluster-debugger                                                       8d
cluster-monitoring-operator                                            7d
cluster-monitoring-view                                                7d
cluster-reader                                                         8d
cluster-status                                                         8d
edit                                                                   8d
glusterblock-provisioner-runner                                        8d
grafana                                                                7d
grafana-user                                                           4d
hawkular-metrics                                                       4d
hawkular-metrics-admin                                                 8d
kube-state-metrics                                                     7d
management-infra-admin                                                 8d
node-exporter                                                          7d
prometheus-k8s                                                         7d
prometheus-operator                                                    7d
registry-admin                                                         8d
registry-editor                                                        8d
registry-viewer                                                        8d
self-access-reviewer                                                   8d
self-provisioner                                                       8d
storage-admin                                                          8d
sudoer                                                                 8d
system:aggregate-to-admin                                              8d
system:aggregate-to-edit                                               8d
system:aggregate-to-view                                               8d
system:auth-delegator                                                  8d
system:aws-cloud-provider                                              8d
system:basic-user                                                      8d
system:build-controller                                                8d
system:build-strategy-custom                                           8d
system:build-strategy-docker                                           8d
system:build-strategy-jenkinspipeline                                  8d
system:kube-aggregator                                                 8d
system:kube-controller-manager                                         8d
system:kube-dns                                                        8d
system:kube-scheduler                                                  8d
system:kubelet-api-admin                                               8d
system:master                                                          8d
system:namespace-controller                                            8d
system:node                                                            8d
system:node-admin                                                      8d
view                                                                   8d

< a lot of output truncated >

```

Some of interesting cluster roles:
- __cluster-admin__ - use this role to give a full access to the cluster
- __cluster-reader__ - gives read-only access to most of resources of the cluster
- __admin__ - is assigned to admins of project, projects' owners have by default
- __edit__ - gives permissions to manipulate resources within a project except the project itself

### Researching a role


- Role __cluster-admin__: has all permissions on all resources enabled

```
$ oc describe clusterrole.rbac cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  authorization.openshift.io/system-only=true
              openshift.io/description=A super-user that can perform any action in the cluster. When granted to a user within a project, they have full control over quota and membership and can perform every action...
              rbac.authorization.kubernetes.io/autoupdate=true
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
  *.*        []                 []              [*]
             [*]                []              [*]
```


- Role __edit__: has enabled only specific actions on the certain resources

```
$ oc describe clusterrole.rbac edit
Name:         edit
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  openshift.io/description=A user that can create and edit most objects in a project, but can not update the project's membership.
              rbac.authorization.kubernetes.io/autoupdate=true
PolicyRule:
  Resources                                          Non-Resource URLs  Resource Names  Verbs
  ---------                                          -----------------  --------------  -----
  networkpolicies.extensions                         []                 []              [create delete deletecollection get list patch update watch create delete deletecollection get list patch update watch]
  networkpolicies.networking.k8s.io                  []                 []              [create delete deletecollection get list patch update watch create delete deletecollection get list patch update watch]
  serviceaccounts                                    []                 []              [create delete deletecollection get list patch update watch impersonate]
  buildconfigs/webhooks                              []                 []              [create delete deletecollection get list patch update watch]
  buildconfigs                                       []                 []              [create delete deletecollection get list patch update watch]
  buildlogs                                          []                 []              [create delete deletecollection get list patch update watch]
  builds                                             []                 []              [create delete deletecollection get list patch update watch]
  configmaps                                         []                 []              [create delete deletecollection get list patch update watch]
  deploymentconfigs/scale                            []                 []              [create delete deletecollection get list patch update watch]
  deploymentconfigs                                  []                 []              [create delete deletecollection get list patch update watch]
  endpoints                                          []                 []              [create delete deletecollection get list patch update watch]
  imagestreamimages                                  []                 []              [create delete deletecollection get list patch update watch]
  imagestreammappings                                []                 []              [create delete deletecollection get list patch update watch]
  imagestreams/secrets                               []                 []              [create delete deletecollection get list patch update watch]
  imagestreams                                       []                 []              [create delete deletecollection get list patch update watch]
  imagestreamtags                                    []                 []              [create delete deletecollection get list patch update watch]
  persistentvolumeclaims                             []                 []              [create delete deletecollection get list patch update watch]
  pods/attach                                        []                 []              [create delete deletecollection get list patch update watch]
  pods/exec                                          []                 []              [create delete deletecollection get list patch update watch]
  pods/portforward                                   []                 []              [create delete deletecollection get list patch update watch]
  pods/proxy                                         []                 []              [create delete deletecollection get list patch update watch]
  pods                                               []                 []              [create delete deletecollection get list patch update watch]
  processedtemplates                                 []                 []              [create delete deletecollection get list patch update watch]
  replicationcontrollers/scale                       []                 []              [create delete deletecollection get list patch update watch]
  replicationcontrollers                             []                 []              [create delete deletecollection get list patch update watch]
  routes                                             []                 []              [create delete deletecollection get list patch update watch]
  secrets                                            []                 []              [create delete deletecollection get list patch update watch]
  services/proxy                                     []                 []              [create delete deletecollection get list patch update watch]
  services                                           []                 []              [create delete deletecollection get list patch update watch]
  templateconfigs                                    []                 []              [create delete deletecollection get list patch update watch]
  templateinstances                                  []                 []              [create delete deletecollection get list patch update watch]
  templates                                          []                 []              [create delete deletecollection get list patch update watch]
  deploymentconfigs.apps.openshift.io/scale          []                 []              [create delete deletecollection get list patch update watch]
  deploymentconfigs.apps.openshift.io                []                 []              [create delete deletecollection get list patch update watch]
  daemonsets.apps                                    []                 []              [create delete deletecollection get list patch update watch]
  deployments.apps/rollback                          []                 []              [create delete deletecollection get list patch update watch]
  deployments.apps/scale                             []                 []              [create delete deletecollection get list patch update watch]
  deployments.apps                                   []                 []              [create delete deletecollection get list patch update watch]
  replicasets.apps/scale                             []                 []              [create delete deletecollection get list patch update watch]
  replicasets.apps                                   []                 []              [create delete deletecollection get list patch update watch]
  statefulsets.apps/scale                            []                 []              [create delete deletecollection get list patch update watch]
  statefulsets.apps                                  []                 []              [create delete deletecollection get list patch update watch]
  horizontalpodautoscalers.autoscaling               []                 []              [create delete deletecollection get list patch update watch]
  cronjobs.batch                                     []                 []              [create delete deletecollection get list patch update watch]
  jobs.batch                                         []                 []              [create delete deletecollection get list patch update watch]
  buildconfigs.build.openshift.io/webhooks           []                 []              [create delete deletecollection get list patch update watch]
  buildconfigs.build.openshift.io                    []                 []              [create delete deletecollection get list patch update watch]
  buildlogs.build.openshift.io                       []                 []              [create delete deletecollection get list patch update watch]
  builds.build.openshift.io                          []                 []              [create delete deletecollection get list patch update watch]
  daemonsets.extensions                              []                 []              [create delete deletecollection get list patch update watch]
  deployments.extensions/rollback                    []                 []              [create delete deletecollection get list patch update watch]
  deployments.extensions/scale                       []                 []              [create delete deletecollection get list patch update watch]
  deployments.extensions                             []                 []              [create delete deletecollection get list patch update watch]
  ingresses.extensions                               []                 []              [create delete deletecollection get list patch update watch]
  replicasets.extensions/scale                       []                 []              [create delete deletecollection get list patch update watch]
  replicasets.extensions                             []                 []              [create delete deletecollection get list patch update watch]
  replicationcontrollers.extensions/scale            []                 []              [create delete deletecollection get list patch update watch]
  imagestreamimages.image.openshift.io               []                 []              [create delete deletecollection get list patch update watch]
  imagestreammappings.image.openshift.io             []                 []              [create delete deletecollection get list patch update watch]
  imagestreams.image.openshift.io/secrets            []                 []              [create delete deletecollection get list patch update watch]
  imagestreams.image.openshift.io                    []                 []              [create delete deletecollection get list patch update watch]
  imagestreamtags.image.openshift.io                 []                 []              [create delete deletecollection get list patch update watch]
  poddisruptionbudgets.policy                        []                 []              [create delete deletecollection get list patch update watch]
  routes.route.openshift.io                          []                 []              [create delete deletecollection get list patch update watch]
  processedtemplates.template.openshift.io           []                 []              [create delete deletecollection get list patch update watch]
  templateconfigs.template.openshift.io              []                 []              [create delete deletecollection get list patch update watch]
  templateinstances.template.openshift.io            []                 []              [create delete deletecollection get list patch update watch]
  templates.template.openshift.io                    []                 []              [create delete deletecollection get list patch update watch]
  buildconfigs/instantiate                           []                 []              [create]
  buildconfigs/instantiatebinary                     []                 []              [create]
  builds/clone                                       []                 []              [create]
  deploymentconfigrollbacks                          []                 []              [create]
  deploymentconfigs/instantiate                      []                 []              [create]
  deploymentconfigs/rollback                         []                 []              [create]
  imagestreamimports                                 []                 []              [create]
  routes/custom-host                                 []                 []              [create]
  deploymentconfigrollbacks.apps.openshift.io        []                 []              [create]
  deploymentconfigs.apps.openshift.io/instantiate    []                 []              [create]
  deploymentconfigs.apps.openshift.io/rollback       []                 []              [create]
  buildconfigs.build.openshift.io/instantiate        []                 []              [create]
  buildconfigs.build.openshift.io/instantiatebinary  []                 []              [create]
  builds.build.openshift.io/clone                    []                 []              [create]
  imagestreamimports.image.openshift.io              []                 []              [create]
  routes.route.openshift.io/custom-host              []                 []              [create]
  jenkins.build.openshift.io                         []                 []              [edit view]
  appliedclusterresourcequotas                       []                 []              [get list watch]
  bindings                                           []                 []              [get list watch]
  builds/log                                         []                 []              [get list watch]
  deploymentconfigs/log                              []                 []              [get list watch]
  deploymentconfigs/status                           []                 []              [get list watch]
  events                                             []                 []              [get list watch]
  imagestreams/status                                []                 []              [get list watch]
  limitranges                                        []                 []              [get list watch]
  namespaces/status                                  []                 []              [get list watch]
  namespaces                                         []                 []              [get list watch]
  pods/log                                           []                 []              [get list watch]
  pods/status                                        []                 []              [get list watch]
  replicationcontrollers/status                      []                 []              [get list watch]
  resourcequotas/status                              []                 []              [get list watch]
  resourcequotas                                     []                 []              [get list watch]
  resourcequotausages                                []                 []              [get list watch]
  routes/status                                      []                 []              [get list watch]
  deploymentconfigs.apps.openshift.io/log            []                 []              [get list watch]
  deploymentconfigs.apps.openshift.io/status         []                 []              [get list watch]
  builds.build.openshift.io/log                      []                 []              [get list watch]
  imagestreams.image.openshift.io/status             []                 []              [get list watch]
  appliedclusterresourcequotas.quota.openshift.io    []                 []              [get list watch]
  routes.route.openshift.io/status                   []                 []              [get list watch]
  imagestreams/layers                                []                 []              [get update]
  imagestreams.image.openshift.io/layers             []                 []              [get update]
  projects                                           []                 []              [get]
  projects.project.openshift.io                      []                 []              [get]
  builds/details                                     []                 []              [update]
  builds.build.openshift.io/details                  []                 []              [update]
```

Observe on your own roles __admin__ and __view__.


## Using Roles to give permissions


One of regular tasks while working with projects is to add new members to a project.

- Authenticate using your login

```
$ oc login -u demo
$ oc whoami
demo
```

- Create a project

```
$ oc new-project sharedproject
```

- Check what permissions you have in the project

```
$ oc get rolebindings -n sharedproject
NAME                    ROLE                    USERS     GROUPS                                 SERVICE ACCOUNTS   SUBJECTS
admin                   /admin                  demo
system:deployers        /system:deployer                                                         deployer
system:image-builders   /system:image-builder                                                    builder
system:image-pullers    /system:image-puller              system:serviceaccounts:sharedproject
```

It shows roles __/admin__ assigned to user __demo__.

- Add cluster role __edit__ to the user __user1__

```
$ oc adm policy add-role-to-user edit user1 -n sharedproject
role "edit" added: "user1"

$ oc get rolebindings
NAME                    ROLE                    USERS     GROUPS                                 SERVICE ACCOUNTS   SUBJECTS
admin                   /admin                  demo
edit                    /edit                   user1
system:deployers        /system:deployer                                                         deployer
system:image-builders   /system:image-builder                                                    builder
system:image-pullers    /system:image-puller              system:serviceaccounts:sharedproject
```

Now log in to the cluster as user __user1__ and check that you can see and use project __sharedproject__

```
$ oc login -u user1
$ oc get projects
$ oc project sharedproject
```

and log in to the cluster back as __demo__ (or whichever your one is) user

```
$ oc login -u demo
```

- Remove role __edit__ from user __user1__

```
$ oc adm policy remove-role-from-user edit user1 -n sharedproject
role "edit" removed: "user1"
$ oc get rolebindings
NAME                    ROLE                    USERS     GROUPS                                 SERVICE ACCOUNTS   SUBJECTS
admin                   /admin                  demo
system:deployers        /system:deployer                                                         deployer
system:image-builders   /system:image-builder                                                    builder
system:image-pullers    /system:image-puller              system:serviceaccounts:sharedproject
```
Now user __user1__ is not here.

- Log in as user __user1__ to the cluster and check the access to project __sharedproject__

```
$ oc login -u user1
```

Supposing that __user1__ did not have other projects before __sharedproject__ the output will be like this
 
```
$ oc get projects
NAME      DISPLAY NAME   STATUS
```

Try to get in to the project __sharedproject__

```
$ oc project sharedproject
error: You are not a member of project "sharedproject".
To see projects on another server, pass '--server=<server>'.
```

## Authors

- Dmitrii Mostovshchikov <Dmitrii.Mostoshchikov@li9.com>

