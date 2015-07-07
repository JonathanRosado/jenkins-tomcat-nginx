#####Using Jenkins' database for authentication and authorization

```yaml
##################################
# Use Jenkins' own user database #
##################################
hudson:
  . . .
  securityRealm:
    attributes: 'database-authentication'
    disableSignup: 'true'
    enableCaptcha: 'false'
  authorizationStrategy:
    attributes: 'login-authorization'
  . . .
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
  . . .
  securityRealm:
    attributes: 'database-authentication'
    disableSignup: 'true'
    enableCaptcha: 'false'
  authorizationStrategy:
    attributes: 'matrix-authorization'
    permissions:
      - 'overall-administer:user1'
      - 'overall-configure-update-center:user1'
      - 'overall-read:user1'
      - 'overall-run-scripts:user1'
      - 'overall-upload-plugins:user1'
  . . .
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
  . . .
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
  authorizationStrategy:
    attributes: 'login-authorization'
  . . .
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
  . . .
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
  authorizationStrategy:
    attributes: 'matrix-authorization'
    permissions:
      - 'overall-read:example2@mail.com' # User example2@mail.com will only have read permission
  . . .
```




#Slaves_config.md

#slaves
```yml
hudson:
  authorizationStrategy:
    attributes:
    - class=hudson.security.AuthorizationStrategy$Unsecured
  buildsDir: ${ITEM_ROOTDIR}/builds
  clouds:
    com.nirima.jenkins.plugins.docker.DockerCloud-1:
      attributes:
      - plugin=docker-plugin@0.9.3
      connectTimeout: '50'
      containerCap: '5'
      credentialsId: ''
      name: ANYNAME
      readTimeout: '150'
      serverUrl: http://16.59.60.234:4243
      templates:
        com.nirima.jenkins.plugins.docker.DockerTemplate:
          bindAllPorts: 'false'
          bindPorts: ''
          credentialsId: 6504ac81-a5fc-4654-9714-390b479afef5
          dnsHosts: ''
          dockerCommand: ''
          environment: ''
          hostname: ''
          idleTerminationMinutes: '5'
          image: evarga/jenkins-slave
          instanceCap: '5'
          javaPath: ''
          jvmOptions: ''
          labelString: ''
          lxcConfString: ''
          mode: EXCLUSIVE
          numExecutors: '1'
          prefixStartSlaveCmd: ''
          privileged: 'false'
          remoteFs: /home/jenkins
          remoteFsMapping: ''
          sshLaunchTimeoutMinutes: '1'
          suffixStartSlaveCmd: ''
          tty: 'false'
          volumes: ''
          volumesFrom2: ''
      version: 1.7.0
    com.nirima.jenkins.plugins.docker.DockerCloud-2:
      attributes:
      - plugin=docker-plugin@0.9.3
      connectTimeout: '50'
      containerCap: '5'
      credentialsId: ''
      name: ANYNAME2
      readTimeout: '150'
      serverUrl: http://16.59.60.234:4243
      templates:
        com.nirima.jenkins.plugins.docker.DockerTemplate:
          bindAllPorts: 'false'
          bindPorts: ''
          credentialsId: b760e70c-4f69-4ec0-9817-505cea27717b
          dnsHosts: ''
          dockerCommand: ''
          environment: ''
          hostname: ''
          idleTerminationMinutes: '5'
          image: jenkins_slave
          instanceCap: '5'
          javaPath: ''
          jvmOptions: ''
          labelString: ''
          lxcConfString: ''
          mode: NORMAL
          numExecutors: '1'
          prefixStartSlaveCmd: ''
          privileged: 'false'
          remoteFs: /home/jenkins
          remoteFsMapping: ''
          sshLaunchTimeoutMinutes: '1'
          suffixStartSlaveCmd: ''
          tty: 'false'
          volumes: ''
          volumesFrom2: ''
      version: 1.7.0
  disableRememberMe: 'false'
  disabledAdministrativeMonitors: ''
  globalNodeProperties: ''
  jdks: ''
  label: ''
  markupFormatter:
    attributes:
    - class=hudson.markup.EscapedMarkupFormatter
  mode: EXCLUSIVE
  myViewsTabBar:
    attributes:
    - class=hudson.views.DefaultMyViewsTabBar
  nodeProperties: ''
  numExecutors: '2'
  primaryView: All
  projectNamingStrategy:
    attributes:
    - class=jenkins.model.ProjectNamingStrategy$DefaultProjectNamingStrategy
  quietPeriod: '5'
  scmCheckoutRetryCount: '0'
  securityRealm:
    attributes:
    - class=hudson.security.SecurityRealm$None
  slaveAgentPort: '0'
  slaves: ''
  useSecurity: 'true'
  version: 1.596.2
  views:
    hudson.model.AllView:
      filterExecutors: 'false'
      filterQueue: 'false'
      name: All
      owner:
        attributes:
        - class=hudson
        - reference=../../..
  viewsTabBar:
    attributes:
    - class=hudson.views.DefaultViewsTabBar
  workspaceDir: ${ITEM_ROOTDIR}/workspace
---
plugins:
  - 'docker-plugin:0.9.3'
  - 'durable-task:0.5'
  - 'token-macro:1.7'
  - 'ssh-slaves:1.6'
```