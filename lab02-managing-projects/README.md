# lab02-managing-projects

Lab 2 - Managing projects

## Accessing VM

- Access vm using vagrant or SSH

```
vagrant ssh
```

- Make sure that client is connected to openshit cluster

```
[vagrant@openshift ~]$ oc status
You don't have any projects. You can try to create a new project, by running

    oc new-project <projectname>

[vagrant@openshift ~]$ oc whoami
student
```

Note! If it doesn't show cluster, you need to use "oc login"

## Creating new projects

- List all projects

```
[vagrant@openshift ~]$ oc get projects
No resources found.

[vagrant@openshift ~]$ oc projects
You are not a member of any projects. You can request a project to be created with the 'new-project' command.
```

- Check builtin help

```
[vagrant@openshift ~]$ oc new-project -h
Create a new project for yourself

If your administrator allows self-service, this command will create a new project for you and assign
you as the project admin.

After your project is created it will become the default project in your config.

Usage:
  oc new-project NAME [--display-name=DISPLAYNAME] [--description=DESCRIPTION] [flags]

Examples:
  # Create a new project with minimal information
  oc new-project web-team-dev

  # Create a new project with a display name and description
  oc new-project web-team-dev --display-name="Web Team Development" --description="Development
project for the web team."

Options:
      --description='': Project description
      --display-name='': Project display name
      --skip-config-write=false: If true, the project will not be set as a cluster entry in
kubeconfig after being created

Use "oc options" for a list of global command-line options (applies to all commands).
```

- Create a new project named "lab2"

```
[vagrant@openshift ~]$ oc new-project --description="The first project" --display-name="Lab2" lab2
Now using project "lab2" on server "https://localhost:8443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app centos/ruby-25-centos7~https://github.com/sclorg/ruby-ex.git

to build a new example application in Ruby.
```

- Check current project

```
[vagrant@openshift ~]$ oc project
Using project "lab2" on server "https://localhost:8443".
```

- Create a new project named  "lab2-demo"

```
[vagrant@openshift ~]$ oc new-project lab2-demo
Now using project "lab2-demo" on server "https://localhost:8443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app centos/ruby-25-centos7~https://github.com/sclorg/ruby-ex.git

to build a new example application in Ruby.
```

- Get current project and make sure that current project has been changed to "lab2-demo"

```
[vagrant@openshift ~]$ oc project
Using project "lab2-demo" on server "https://localhost:8443".

[vagrant@openshift ~]$ oc get projects
NAME        DISPLAY NAME   STATUS
lab2        Lab2           Active
lab2-demo                  Active
```

## Switching between projects

- Check help for oc project

```
[vagrant@openshift ~]$ oc project -h
Switch to another project and make it the default in your configuration

If no project was specified on the command line, display information about the current active
project. Since you can use this command to connect to projects on different servers, you will
occasionally encounter projects of the same name on different servers. When switching to that
project, a new local context will be created that will have a unique name - for instance, 'myapp-2'.
If you have previously created a context with a different name than the project name, this command
will accept that context name instead.

For advanced configuration, or to manage the contents of your config file, use the 'config' command.

Usage:
  oc project [NAME] [flags]

Examples:
  # Switch to 'myapp' project
  oc project myapp

  # Display the project currently in use
  oc project

Options:
  -q, --short=false: If true, display only the project name

Use "oc options" for a list of global command-line options (applies to all commands).
```

- Change current project to lab2 and make sure that it is active

```
[vagrant@openshift ~]$ oc project lab2
Now using project "lab2" on server "https://localhost:8443".

[vagrant@openshift ~]$ oc projects
You have access to the following projects and can switch between them with 'oc project <projectname>':

  * lab2 - Lab2
    lab2-demo

Using project "lab2" on server "https://localhost:8443".
```
