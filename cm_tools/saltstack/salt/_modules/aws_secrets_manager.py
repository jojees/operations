# -*- coding: utf-8 -*-
'''
Support for the Amazon Secrets Manager.
'''

# Import Python libs
#from __future__ import absolute_import, print_function, unicode_literals
#import logging

# Import salt libs
#import salt.utils.json
#import salt.utils.path
#from salt.ext import six

#log = logging.getLogger(__name__)

_OUTPUT = '--output json'

def __virtual__():
    '''
    Only load if aws is available.
    '''
    if __salt__['cmd.has_exec']('aws'):
        return 'aws_secrets_manager'
    return False, 'The module aws_sqs could not be loaded: aws command not found'

def list():
    return 1
