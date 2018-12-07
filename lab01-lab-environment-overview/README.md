# lab01-lab-environment-overview
Lab 1 - Overview of the lab environment

## Accessing VM
- You may deploy the lab environment using the following command

```
https://github.com/li9com/learn-openshift.git
cd learn-openshift
vagrant up
```

- Once VM provisioning is complete, you may access your VM as follows

```
$ vagrant  ssh
Last login: Thu Dec  6 23:32:48 2018 from 10.0.2.2
[vagrant@openshift ~]$ whoami
vagrant
[vagrant@openshift ~]$

```

- Check VM details

```
[vagrant@openshift ~]$ hostname
openshift.172.24.0.11.nip.io

[vagrant@openshift ~]$ cat /etc/redhat-release
CentOS Linux release 7.5.1804 (Core)

[vagrant@openshift ~]$ rpm -q origin-clients
origin-clients-3.11.0-1.el7.git.0.62803d0.x86_64

[vagrant@openshift ~]$ rpm -q docker
docker-1.13.1-84.git07f3374.el7.centos.x86_64
```

Note! it is expected that docker and origin-clients packages are installed

- Check cluster status

```
[vagrant@openshift ~]$ sudo oc cluster status
Web console URL: https://openshift.172.24.0.11.nip.io:8443/console/

Config is at host directory
Volumes are at host directory
Persistent volumes are at host directory /home/vagrant/openshift.local.clusterup/openshift.local.pv
Data will be discarded when cluster is destroyed
```

Note! you need to run this command under the root account or using sudo as in the example above.

- Make sure that the "oc" client is not connected to a cluster

```
[vagrant@openshift ~]$ oc status
error: Missing or incomplete configuration info.  Please login or point to an existing, complete config file:

  1. Via the command-line flag --config
  2. Via the KUBECONFIG environment variable
  3. In your home directory as ~/.kube/config

To view or setup config directly use the 'config' command.
```

Note! it is expected that oc is not connected to the cluster under the "vagrant" user

- Connect to the OpenShift cluster installed on the local machine

```
[vagrant@openshift ~]$ oc login
Server [https://localhost:8443]:
The server uses a certificate signed by an unknown authority.
You can bypass the certificate check, but any data you send to the server could be intercepted by others.
Use insecure connections? (y/n): y

Authentication required for https://localhost:8443 (openshift)
Username: student
Password: <TYPE ANY PASSWORD>
Login successful.

You don't have any projects. You can try to create a new project, by running

    oc new-project <projectname>

Welcome! See 'oc help' to get started.

```

- Check current openshift user

```
[vagrant@openshift ~]$ oc whoami
student
```

- Check that oc is connected to the cluster under the root user

```
[vagrant@openshift ~]$ sudo oc whoami
developer
[vagrant@openshift ~]$ sudo su -
Last login: Thu Dec  6 23:32:50 UTC 2018 on pts/0
[root@openshift ~]# oc whoami
developer
```

- Connect to the cluster using "system:admin" account

```
[root@openshift ~]# oc login -u system:admin
Logged into "https://127.0.0.1:8443" as "system:admin" using existing credentials.

You have access to the following projects and can switch between them with 'oc project <projectname>':

    default
    kube-dns
    kube-proxy
    kube-public
    kube-system
  * myproject
    openshift
    openshift-apiserver
    openshift-controller-manager
    openshift-core-operators
    openshift-infra
    openshift-node
    openshift-service-cert-signer
    openshift-web-console

Using project "myproject".
[root@openshift ~]# oc whoami
system:admin
```

Note! We need to use the root user account


## Accessing OpenShift Web console

- Check cluster status and look for OpenShift console URL

```
[root@openshift ~]# oc cluster status
Web console URL: https://openshift.172.24.0.11.nip.io:8443/console/

Config is at host directory
Volumes are at host directory
Persistent volumes are at host directory /home/vagrant/openshift.local.clusterup/openshift.local.pv
Data will be discarded when cluster is destroyed

```

Note! you need to run the command under root user

- Try to access openshift web console using the url:

```
https://openshift.172.24.0.11.nip.io:8443/console/
```
