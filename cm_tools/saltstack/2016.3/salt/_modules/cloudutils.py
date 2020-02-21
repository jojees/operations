'''
Custom resources support for MVision Cloud Infrastructure.
'''

_OUTPUT = '--output json'

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def __virtual__():
    '''
    Only load if aws is available.
    '''
    if __salt__['cmd.has_exec']('aws'):
        return 'cloudutils'
    return False, 'The module mvision_resources could not be loaded: aws command not found'


def _region(region):
    '''
    Return the region argument.
    '''
    return ' --region {r}'.format(r=region)

def _run_aws(cmd, region, opts, user='root', **kwargs):
    receipthandle = kwargs.pop('receipthandle', None)
    cmd = 'aws {cmd} {args} {region} {out}'.format(
        cmd=cmd,
        args=opts,
        region=_region(region),
        out=_OUTPUT)
    rtn = __salt__['cmd.run'](cmd, runas=user, python_shell=False)
    blank_return = '{}'

    try:
        if rtn:
            return json.loads(rtn)
    except:
        return json.loads(blank_return)
    
    
def get_region_instanceid():
    #r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
    r = requests.get("https://raw.githubusercontent.com/jojees/pydocker-tools/master/dummy.json", verify=False)
    response_json = r.json()
    region = response_json.get('region')
    instance_id = response_json.get('instanceId')
    return [region, instance_id]
    

def _get_cfn_stack_name(user=None):
    r = requests.get("https://raw.githubusercontent.com/jojees/pydocker-tools/master/dummy.json", verify=False)
    response_json = r.json()
    region = response_json.get('region')
    instance_id = response_json.get('instanceId')
    opts = '--instance-id {INSTANCE_ID} --query "Reservations[*].Instances[*].Tags[?Key==`aws:cloudformation:stack-name`].Value"'.format(
        INSTANCE_ID=instance_id
    )
    stackname = _run_aws("ec2 describe-instances", region, opts, user)
    return [stackname, region]
    

def _get_iam_name(stack=None, user=None, logical_id=None, region=None):
    opts = '--stack-name {stackname} --logical-resource-id {resource}'.format(
        stackname=stack,
        resource=logical_id
    )
    resource = _run_aws("cloudformation describe-stack-resource", region, opts, user)
    return resource.get('StackResourceDetail')['PhysicalResourceId']
    
    
def verify_key(name, keypath=None, user=None, cf_resource=None):
    #####  DUMMY CALL ######
    iam_username = 'test_custom_apps_trial'
    #########################
    return iam_username


def ssm_has_key(region, environment=None, app=None):
    secret = [environment, app, 'privatekey']
    opts = "--secret-id {secret_name}".format(secret_name="/".join(secret))
    response = _run_aws("secretsmanager describe-secret", region, opts)
    return True if response else False


def secret_exists(name, keypath=None, user=None):
    stackname, region = _get_cfn_stack_name(user=user)
    #####  DUMMY CALL ######
    stackname = 'corpshared-EnvSpecificResources-G61VVHRWR54W'
    environment = stackname.split('-')[0]
    app_name = stackname.split('-')[1]
    if ssm_has_key(region, environment=environment, app=app_name):
        first_run = False
    else:
        first_run = True
    data = {}
    data['stackname'] = stackname
    data['environment'] = environment
    data['app'] = app_name
    data['first_run'] = first_run
    data['region'] = region
    return data


def _uploadkey_to_ssm(region, cred_name=None, keyfile=None, user=None):
    opts = "--name {name} --secret-string file://{secret_string} --description '{desc}'".format(
        name=cred_name + '/privatekey',
        secret_string=keyfile,
        desc="Private Key file of {app}".format(app=cred_name)
    )
    response = _run_aws("secretsmanager create-secret", region, opts, user)
    if response:
        return True
    else:
        return False


def _upload_name_to_ssm(region, cred_name=None, msg=None, user=None):
    opts = "--name '{name}' --type 'String' --value '{msg}'".format(
        name=cred_name + '-iam_ssh_username',
        msg=msg
    )
    response = _run_aws("ssm put-parameter", region, opts, user)
    if response:
        return True
    else:
        return False
    
    
def upload_secret(name, sshkey=None, stackname=None, cf_resource=None, region=None, user=None):
    iam_username = _get_iam_name(
        stack=stackname,
        user=user,
        logical_id=cf_resource,
        region=region
    )
    #####  DUMMY CALL ######
    iam_username = 'test_custom_apps_trial'
    stackname = "corpshared-EnvSpecificResources-G61VVHRWR54W"
    #########################
    
    opts = '--user-name  {username} --ssh-public-key-body file://{keyfile}'.format(
        username=iam_username,
        keyfile=sshkey + '.pub'
    )
    iam_upload = _run_aws("iam upload-ssh-public-key", region, opts, user)
    status = {}
    if iam_upload:
        status['iam_ssh_username'] = iam_upload.get('SSHPublicKey')['SSHPublicKeyId']
        status['iam_upload_status'] = True
        status['iam_username'] = iam_username
        credential_name = stackname.split('-')[0] + '/' + stackname.split('-')[1]
        uploaded = _uploadkey_to_ssm(
            region=region,
            cred_name=credential_name,
            keyfile=sshkey,
            user=user
        )
        uploaded = True
        if uploaded:
            status['secret_in_ssm'] = True
        else:
            status['secret_in_ssm'] = False
        upload_username = _upload_name_to_ssm(
            region=region,
            cred_name=credential_name.replace('/', '-'),
            msg=status['iam_ssh_username'],
            user=user
        )
        if upload_username:
            status['username_in_ssm_params'] = True
        else:
            status['username_in_ssm_params'] = False
        
        
    else:
        status['iam_ssh_username'] = None
        status['iam_upload_status'] = False
        status['iam_username'] = iam_username
    return status
    