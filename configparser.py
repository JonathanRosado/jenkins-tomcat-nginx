# !/usr/bin/env python
"""
Author: Jonathan Rosado Lugo
Email: jonathan.rosado-lugo@hp.com


Description:
        General script for parsing YAML lists and key value pairs 

Dependencies:
    -PyYaml

Input:

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
  - 'user1:secret'
  - 'user2:superman'

Ouput:

/hudson/securityRealm/attributes|database-authentication
/hudson/securityRealm/enableCaptcha|false
/hudson/securityRealm/disableSignup|true
/hudson/authorizationStrategy/attributes|login-authorization
/users|['jon1:secret', 'jon2:superman']

"""

import sys
import types
import yaml

def dispatch(yamlObject):

    def cycle(obj, nodePath):
        if type(obj) == types.DictType:
            for key, value in obj.iteritems():
                nodePath.append('/' + key)
                if type(value) == types.StringType or type(value) == types.BooleanType or type(value) == types.ListType:
                    print ''.join(nodePath) + '|' + value.__str__()
                    nodePath = nodePath[:-1]
                else:
                    cycle(value, nodePath)
        else:
            sys.exit('RUN: Invalid value type reached')

    cycle(yamlObject, [])

    return


def main():
    args = sys.argv[1:]

    inYamlFile = args[0]

    for yamlObject in yaml.load_all(open(inYamlFile)):
        dispatch(yamlObject)


if __name__ == '__main__':
    main()
