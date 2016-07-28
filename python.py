#!/usr/bin/env python
import sys

validPassword = 'secret'

inputPassword = raw_input('Please Enter Password: ')

if inputPassword == validPassword:
    print 'You have access!'
else:
    print 'Access denied!'
    sys.exit(0)

print 'Welcome!'
