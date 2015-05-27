Jenkins on tomcat + nginx
=========================

A Jenkins docker image running on tomcat and nginx with a focus on enabling user configuration and automation.

## Usage

To run this jenkins container with you may run the following command:

```bash
sudo docker run \
    -it \
    -p $PORT_FOR_JENKINS:8081 \
    -v path/to/jenkins_home:/jenkins_home \
    -v path/to/config.yml:/config.yml
    verigreen/jenkins-tomcat-nginx
```

Where `config.yml` represents the configuration for each container instance
```yaml
##################################
# Use Jenkins' own user database #
##################################
hudson:
  securityRealm:
    attributes: 'database-authentication'
    disableSignup: 'true'
    enableCaptcha: 'false'
---
hudson:
  authorizationStrategy:
    attributes: 'login-authorization'
---
users:
  - 'user1:password1'
  - 'user2:password2'
```

Then, from your host, you may access the jenkins UI at `localhost:$PORT_FOR_JENKINS`. 

The `-p $PORT_FOR_JENKINS:8081` is *required* to map a host port to the port where jenkins is exposed in the container. The `-v path/to/jenkins_home:/var/jenkins_home` is *recommended* if you want to persist any configuration and data that happens during the execution of jenkins in that container instance. The `-v path/to/config.yml:/config.yml` is how each Jenkins instance is customized. The `-it` command runs the container interactively. To run the container in *detached* mode replace the `-it` option with `-d` or if it is already running press `CTRL`+`P` followed by `CTRL`+`Q` and it will detach.

The following is the complete list of mountable volumes that you may use for *customizing* `jenkins`, `nginx`, and/or `tomcat` to your needs:
```bash
sudo docker run \
    -d \
    --name $CONTAINER_NAME \
    -e ADMIN_PASSWORD=mysecretpass \
    -p $PORT_FOR_JENKINS:8081 \
    -v path/to/nginx.conf:/nginx.conf \
    -v path/to/supervisord.conf:/supervisord.conf \
    -v path/to/jenkins/log/directory/:/var/log/nginx/jenkins/ \
    -v path/to/supervisor/log/directory:/var/log/supervisor/ \
    -v path/to/sample_jobs.groovy:/jobs.groovy \
    -v path/to/jenkins_home:/jenkins_home \
    -v path/to/config.xml:/config.xml \
    jonathan/jenkins-nginx
```

## Configuration

### Migrating existing Jenkins

If you already have a jenkins instance you can migrate your existing data and configuration to be used with this container. To accomplish this, you must add the `-v /path/to/jenkins_home:/var/jenkins_home` to the `docker run` command. Your `/path/to/jenkins_home` should allow you to point the following assets:

1. **Existing jobs**: the jobs that you want to reuse and persist with this container should be located in your *host's* `/path/to/jenkins_home/jobs`. The jenkins running within the container will look for them in `/var/jenkins_home/jobs` during startup.

2. **Existing plugins**: the plugins that you want to reuse and persist with this container should be located in your *host's* `/path/to/jenkins_home/plugins`. The jenkins running within the container will look for them in `/var/jenkins_home/plugins`.

### The config.yml

The specification for the config.yml allows you to modify sections of Jenkins' root configuration file. You need not provide a complete XML file with the intention of modifying only the authentication settings, for example.

This YAML
```yaml
hudson:
  securityRealm:
    attributes:
      - 'class=hudson.security.HudsonPrivateSecurityRealm'
    disableSignup: 'true'
    enableCaptcha: 'false'
```
Will have this effect on the Jenkins configuration file
```xml
<hudson>
  .
  .
  <authorizationStrategy .../>
  <securityRealm class="hudson.security.HudsonPrivateSecurityRealm">
    <enableCaptcha>true</enableCaptcha>
    <disableSignup>false</disableSignup>
  </securityRealm>
  <disableRememberMe>...</disableRememberMe>
  .
  .
</hudson>
```

Through the config.yml, you can also:

1. **Use aliases**: You may specify intuitive aliases for attributes when working with the root configuration file.

2. **Download and install plugins**: You may specify a list containing the name of the plugin and it's version. The container will then download the plugin and install it.

3. **Add users to Jenkins' internal database**: You may specify a list of user names and passwords. The container will proceed to encrypt the passwords and make the appropriate xml files for each user.

4. **Add SSL certificates**: You may be using an external service which requires secured communication, such as ldap. You may specify a list of servers in YAML file. The container will then download the appropriate certificate for each server in the list and will import them into the keystore.

5. **Run CLI commands**: You may have Jenkins run CLI commands on startup. Simply provide a list of commands in the config.yml.

```yaml
hudson:
  securityRealm:
    attributes: 'database-authentication' # 1. Alias for 'class=hudson.security.HudsonPrivateSecurityRealm'
    # attributes:
    #   - 'class=hudson.security.HudsonPrivateSecurityRealm'
    disableSignup: 'true'
    enableCaptcha: 'false'
---
plugins: # 2. List of plugins 'PlUGIN:VERSION'
  - 'dockerhub:1.0'
  - 'token-macro:1.10'
---
users: # 3. List of users 'USERNAME:PASSWORD'
  - 'user1:password1'
  - 'user2:password2'
---
certificates: # 4. List of certificates 'DOMAIN:PORT'
  - 'ldap.example1.net:636'
  - 'ldap.example2.com:636'
---
commands: # 5. List of commands 
  - "echo 'jenkins.model.Jenkins.instance.securityRealm.createAccount(\"admin\", \"password\")'"
```

####Examples

#####Using Jenkins' database for authentication and authorization

```yaml
##################################
# Use Jenkins' own user database #
##################################
hudson:
  securityRealm:
    attributes: 'database-authentication'
    disableSignup: 'true'
    enableCaptcha: 'false'
---
hudson:
  authorizationStrategy:
    attributes: 'login-authorization'
---
users:
  - 'user1:password1'
  - 'user2:password2'
```

#####Using Jenkins' database for authentication and authorization (with matrix authorization)

```yaml
###################
#DATABASE + MATRIX#
###################
hudson:
  securityRealm:
    attributes: 'database-authentication'
    disableSignup: 'true'
    enableCaptcha: 'false'
---
hudson:
  authorizationStrategy:
    attributes: 'matrix-authorization'
    permissions:
      - 'overall-administer:user1'
      - 'overall-configure-update-center:user1' 
      - 'overall-read:user1'
      - 'overall-run-scripts:user1' 
      - 'overall-upload-plugins:user1'
---
users:
  - 'user1:password1' # Has all privileges
  - 'user2:password2' # User has no privileges
```

#####Using LDAP authentication with basic login authorization

```yaml
##############
#LDAP + LOGIN#
##############
hudson:
  securityRealm:
    attributes: 'ldap-authentication'
    # attributes:
    #   - 'class=hudson.security.LDAPSecurityRealm'
    #   - 'plugin=ldap@1.6'
    server: 'ldap://ldap.example.com:636'
    rootDN: 'OU=users,DC=example,DC=net'
    inhibitInferRootDN: ''
    userSearchBase: ''
    userSearch: 'sAMAccountName={0}'
    groupSearchBase: ''
    groupSearchFilter: ''
    managerDN: 'CN=example@main.com,DC=example,DC=net'
    managerPassword: 'MANAGER_PASSWORD'
    disableMailAddressResolver: ''
---
hudson:
  authorizationStrategy:
    attributes: 'login-authorization'
---
certificates:
  - 'ldap.example.net:636'
```

#####Using LDAP authentication with matrix authorization

```yaml
###############
#LDAP + MATRIX#
###############
hudson:
  securityRealm:
    attributes: 'ldap-authentication'
    # attributes:
    #   - 'class=hudson.security.LDAPSecurityRealm'
    #   - 'plugin=ldap@1.6'
    server: 'ldap://ldap.example.com:636'
    rootDN: 'OU=users,DC=example,DC=net'
    inhibitInferRootDN: ''
    userSearchBase: ''
    userSearch: 'sAMAccountName={0}'
    groupSearchBase: ''
    groupSearchFilter: ''
    managerDN: 'CN=example@main.com,DC=example,DC=net'
    managerPassword: 'MANAGER_PASSWORD'
    disableMailAddressResolver: ''
---
hudson:
  authorizationStrategy:
    attributes: 'matrix-authorization'
    permissions:
      - 'overall-read:example2@mail.com' # User example2@mail.com will only have read permission
```

### Adding new plugins

Specify a list of plugins in the config.yml. The value of each list item should match the format <PLUGIN:VERSION>. This list has to be a 'separate document', meaning that you have to separate the list from the others with three dashes ("---"). The container will look for the plugin in http://updates.jenkins-ci.org/download/plugins, so make sure that what you are referencing appears on that list.

```yaml
.
.
.
---
plugins:
  - 'dockerhub:1.0'
  - 'token-macro:1.10'
```

###Adding an admin account
You can create a quick admin account by setting the environment variable ADMIN_PASSWORD at run-time

`Docker run`
```bash
sudo docker run \
    -d \
    -e ADMIN_PASSWORD=mysecretpass \
    -p $PORT_FOR_JENKINS:8081 \
    verigreen/jenkins-tomcat-nginx
```
###Adding users programmatically
Specify a list of users in the config.yml in the format <USERNAME:PASSWORD>. This list has to be a 'separate document', meaning that you have to separate the list from the others with three dashes ("---"). The container will parse each list item from the list and create an XML file for each user.

```yaml
.
.
.
---
users:
  - 'user1:password1'
  - 'user2:password2'
  - 'user3:password3'
  - 'user4:password4'
```

###Running commands in the Jenkins CLI
Jenkins has a built-in command line client that allows you to access Jenkins from a script or from your shell. This is convenient for automation of routine tasks, bulk updates, trouble diagnosis, and so on.

You can supply CLI commands to Jenkins listing the commands in the config.yml.

`cli.txt`
```yaml
.
.
.
---
commands:
  - "echo 'jenkins.model.Jenkins.instance.securityRealm.createAccount(\"admin\", \"password\")'"
  - "echo 'restart'"
```

These commands will create a new user within Jenkins own user database and restart the server.

### Adding new jobs

In jenkins, it is possible to configure a job by creating custom XML files that describe the job. However, this container *supports* the use of the [Job DSL plugin](https://github.com/jenkinsci/job-dsl-plugin/wiki/Tutorial---Using-the-Jenkins-Job-DSL) by allowing the specification of jobs using a `groovy` DSL. Simply map the groovy script to the container's root directory `-v /path/to/sample_jobs.groovy:/var/tmp/jobs.groovy`.

We recommend that you take a look at the [tutorial](https://github.com/jenkinsci/job-dsl-plugin/wiki/Tutorial---Using-the-Jenkins-Job-DSL) for using the DSL plugin before attempting this.

Once you have written some jobs, add them to `/path/to/sample_jobs.groovy` file. It is *required* that the file ends with `.groovy` extension. It should look something similar to the following:

```groovy
// Example of sample_jobs.groovy
job('NAME-groovy') { //To separate groovy jobs from other, please add the *-groovy to your groovy defined job
    scm {
        git('git://github.com/jgritman/aws-sdk-test.git')
    }
    triggers {
        scm('*/15 * * * *')
    }
    steps {
        maven('-e clean test')
    }
}
```

When you are done, `run` or `restart` your container. The setup script will inspect the `/var/tmp/jobs.groovy` file and install them correctly by setting up the Job DSL plugin and performing some requests on Jenkins.

### Configuring `nginx`

We use nginx to serve jenkins' static files. You may customize its configuration by writing your own `nginx.conf` and mapping it to the container using the `-v /path/to/nginx.conf:/etc/nginx/nginx.conf:ro` volume mapping. We recommend that you use the included `nginx.conf` as a starting point. You must `run` or `restart` the container after modifications are done to pick up any changes.

### Configuring `supervisord`

We use a process management tool called Supervisor (http://docs.docker.com/articles/using_supervisord/) to better handle our multi-process container. You may customize it by writing your own `supervisord.conf` configuration file and mapping it to the container using `-v /path/to/supervisord.conf:/etc/supervisor/conf.d/supervisord.conf:ro` volume mapping.  We recommend that you use the included `supervisord.conf` as a starting point. You must `run` or `restart` the container after modifications are done to pick up any changes.

###Configuring Global Security Programmatically
Let's look at how we can setup a secure Jenkins (via root config.xml)

Here's a clean config.xml for your convenience:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<hudson>
  <disabledAdministrativeMonitors/>
  <version>1.0</version>
  <numExecutors>2</numExecutors>
  <mode>NORMAL</mode>
  <useSecurity>true</useSecurity>
  <authorizationStrategy class="hudson.security.AuthorizationStrategy$Unsecured"/>
  <securityRealm class="hudson.security.SecurityRealm$None"/>
  <disableRememberMe>false</disableRememberMe>
  <projectNamingStrategy class="jenkins.model.ProjectNamingStrategy$DefaultProjectNamingStrategy"/>
  <workspaceDir>${ITEM_ROOTDIR}/workspace</workspaceDir>
  <buildsDir>${ITEM_ROOTDIR}/builds</buildsDir>
  <markupFormatter class="hudson.markup.EscapedMarkupFormatter"/>
  <jdks/>
  <viewsTabBar class="hudson.views.DefaultViewsTabBar"/>
  <myViewsTabBar class="hudson.views.DefaultMyViewsTabBar"/>
  <clouds/>
  <slaves/>
  <scmCheckoutRetryCount>0</scmCheckoutRetryCount>
  <views>
    <hudson.model.AllView>
      <owner class="hudson" reference="../../.."/>
      <name>All</name>
      <filterExecutors>false</filterExecutors>
      <filterQueue>false</filterQueue>
      <properties class="hudson.model.View$PropertyList"/>
    </hudson.model.AllView>
  </views>
  <primaryView>All</primaryView>
  <slaveAgentPort>0</slaveAgentPort>
  <label></label>
  <nodeProperties/>
  <globalNodeProperties/>
</hudson>
```
###Authentication
####Ldap
To make Jenkins authenticate via LDAP, add the following xml to your root `config.xml` with your own configuration values.
```xml
...
<mode>...</mode>
<useSecurity>...</useSecurity>
<authorizationStrategy .../>
<securityRealm class="hudson.security.LDAPSecurityRealm" plugin="ldap@1.6">
    <server>ldap://ldap.example.com</server>
    <rootDN>ou=People,O=example</rootDN>
    <inhibitInferRootDN>false</inhibitInferRootDN>
    <userSearchBase></userSearchBase>
    <userSearch>uid={}</userSearch>
    <groupSearchBase>groupAttr</groupSearchBase>
    <groupSearchFilter>groupAttr=100</groupSearchFilter>
    <managerDN>cn=john.doe@example.com,ou=people,o=example</managerDN>
    <managerPassword>bG9s</managerPassword>
    <disableMailAddressResolver>false</disableMailAddressResolver>
</securityRealm>
...
```
The values provided in the snippet should serve as a clue as to how to format your own.

The value for `<managerPassword>` is base64 encoded. This is how Jenkins stores passwords and it is how it'll read them. 

Open up a terminal and run the following command to get the base64 version of your password 
`echo <MYPASSWORD> | base64 | awk -F'=' '{print $1}'`

Replace `<MYPASSWORD>` with your own and put the result of the command in the `<managerPassword>` node.

>NOTE: If you want to make sure you got the right encoding for your password, you can run the following command and see for yourself
>`echo <ENCODED_PASSWORD> | base64 --decode`
>You might receive a warning if your password's base64 encoding is not divisible by 3 bytes. You can go ahead and ignore this.

Once you're finished with the root config file. Go ahead and restart Jenkins by running 
`sudo docker exec <CONTAINERNAME> /bin/bash -c "supervisorctl restart all:jenkins"`
If you're already inside the container, you can achieve the same running these commands
`${CATALINA_HOME}/bin/catalina.sh stop`
`${CATALINA_HOME}/bin/catalina.sh start`

You should now have Jenkins configured for LDAP authentication.

> NOTE: If you get an SSL handshake exception while configuring LDAP in Jenkins, you will probably have to add the SSL certificate to Java's keystore.
> 
> You can do the following:  
> 
> 1) Access the container via `sudo docker exec -ti <CONTAINER_NAME> /bin/bash`  
> 2) Download your SSL certificate. If you have the server running, you can download it directly 
`echo -n | openssl s_client -connect <HOST>:<PORT> | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > /tmp/<SERVERNAME>.crt`
>3) Use the keytool to add the SSL certificate to Java's keystore (keystore password = `changeit`)
`keytool -import -trustcacerts -alias <HOST_NAME> -file /tmp/<SERVERNAME>.crt -keystore ${JAVA_HOME}/jre/lib/security/cacerts`
> 4) Check to see if the SS certificate was added to the keystore successfully
`keytool -list -v -keystore /usr/lib/jvm/java-7-openjdk-amd64/jre/lib/security/cacerts`
>5) Restart Jenkins
>
>Alternatively, you can provide a text file (specifying the servers which you want Jenkins to have access to) to the container and it will try to add the certs to the keystore. If no port is specified, port 443 will be used.
>```
>ldap.example.com:443
>ldap.example2.com:636
>ldap.example3.com
>```
>`-v path/to/SSLcerts.txt:/SSLcerts.txt` 
>
>Finally, to check if everything works, access the container and run this command
>`cd Cert-Install-Tool/ && java SSLPoke ldap.example.com 443`
>This will send a byte to your LDAP server and verify confidentiality. 
>
>If you're still getting a handshake exception, you can try downloading a different certificate (assuming the server yields multiple SSL certificates).
>Just append whichever one you want to download to the server:port entry.
>```
>ldap.example.com:443:1
>ldap.example2.com:636:2
>ldap.example3.com:443:1
>```


####Jenkins’ own user database 
```xml
...
<mode>...</mode>
<useSecurity>...</useSecurity>
<authorizationStrategy .../>
<securityRealm class="hudson.security.HudsonPrivateSecurityRealm">
    <disableSignup>false</disableSignup>
    <enableCaptcha>false</enableCaptcha>
</securityRealm>
...
```
####Unix user/group database 
```xml
...
<mode>...</mode>
<useSecurity>...</useSecurity>
<authorizationStrategy .../>
<securityRealm class="hudson.security.PAMSecurityRealm" plugin="pam-auth@1.1">
    <serviceName>sshd</serviceName>
</securityRealm>
...
```
###Authorization
####Anyone can do anything
```xml
...
<numExecutors>...</numExecutors>
<mode>...</mode>
<useSecurity>true</useSecurity>
<authorizationStrategy class="hudson.security.AuthorizationStrategy$Unsecured"/>
<securityRealm .../>
<disableRememberMe>...</disableRememberMe>
...
```
####Legacy mode
```xml
...
<numExecutors>...</numExecutors>
<mode>...</mode>
<useSecurity>true</useSecurity>
<authorizationStrategy class="hudson.security.LegacyAuthorizationStrategy"/>
<securityRealm .../>
<disableRememberMe>...</disableRememberMe>
...
```
####Logged-in users can do anything
```xml
...
<numExecutors>...</numExecutors>
<mode>...</mode>
<useSecurity>true</useSecurity>
<authorizationStrategy class="hudson.security.FullControlOnceLoggedInAuthorizationStrategy"/>
<securityRealm .../>
<disableRememberMe>...</disableRememberMe>
...
```
####Matrix-based security
Here we give `Anonymous`  reading privileges and we give `User1` full control.
```xml
...
<numExecutors>...</numExecutors>
<mode>...</mode>
<useSecurity>true</useSecurity>
<authorizationStrategy class="hudson.security.ProjectMatrixAuthorizationStrategy">
    <permission>com.cloudbees.plugins.credentials.CredentialsProvider.Create:user1</permission>
    <permission>com.cloudbees.plugins.credentials.CredentialsProvider.Delete:user1</permission>
    <permission>com.cloudbees.plugins.credentials.CredentialsProvider.ManageDomains:user1</permission>
    <permission>com.cloudbees.plugins.credentials.CredentialsProvider.Update:user1</permission>
    <permission>com.cloudbees.plugins.credentials.CredentialsProvider.View:user1</permission>
    <permission>hudson.model.Computer.Build:user1</permission>
    <permission>hudson.model.Computer.Configure:user1</permission>
    <permission>hudson.model.Computer.Connect:user1</permission>
    <permission>hudson.model.Computer.Create:user1</permission>
    <permission>hudson.model.Computer.Delete:user1</permission>
    <permission>hudson.model.Computer.Disconnect:user1</permission>
    <permission>hudson.model.Hudson.Administer:user1</permission>
    <permission>hudson.model.Hudson.ConfigureUpdateCenter:user1</permission>
    <permission>hudson.model.Hudson.Read:anonymous</permission>
    <permission>hudson.model.Hudson.Read:user1</permission>
    <permission>hudson.model.Hudson.RunScripts:user1</permission>
    <permission>hudson.model.Hudson.UploadPlugins:user1</permission>
    <permission>hudson.model.Item.Build:user1</permission>
    <permission>hudson.model.Item.Cancel:user1</permission>
    <permission>hudson.model.Item.Configure:user1</permission>
    <permission>hudson.model.Item.Create:user1</permission>
    <permission>hudson.model.Item.Delete:user1</permission>
    <permission>hudson.model.Item.Discover:user1</permission>
    <permission>hudson.model.Item.Read:user1</permission>
    <permission>hudson.model.Item.Workspace:user1</permission>
    <permission>hudson.model.Run.Delete:user1</permission>
    <permission>hudson.model.Run.Update:user1</permission>
    <permission>hudson.model.View.Configure:user1</permission>
    <permission>hudson.model.View.Create:user1</permission>
    <permission>hudson.model.View.Delete:user1</permission>
    <permission>hudson.model.View.Read:user1</permission>
    <permission>hudson.scm.SCM.Tag:user1</permission>
</authorizationStrategy>
<securityRealm .../>
<disableRememberMe>...</disableRememberMe>
...
```
