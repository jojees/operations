'''
Manage custom IAM resources which are not available in the salt-server 2016.3.
'''

__virtualname__ = 'iam_support'

def get_region_instanceid(name, username=None, region=None):
    ret = {'name': name, 'result': False, 'comment': '', 'changes': {}}
    region, instance_id = __salt__['cloudutils.get_region_instanceid']()
    ret['comment'] = region
    return ret

def iam_sshkey_exists(name, keypath=None, user=None, cf_logical_id=None):
    ret = {'name': name, 'result': False, 'comment': '', 'changes': {}}
    does_exist = __salt__['cloudutils.secret_exists'](name, keypath=keypath, user=user)
    
    if does_exist['first_run']:
        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'SSH Public key is set to uploaded to the iam user.'
            return ret

        start_upload = __salt__['cloudutils.upload_secret'](
            name,
            sshkey=keypath,
            user=user,
            cf_resource=cf_logical_id,
            region=does_exist['region'],
            stackname=does_exist['stackname']
        )
        if start_upload['iam_upload_status']:
            ret['comment'] = 'Uploaded the private key to IAM user and also to AWS Secrets Manager.'
            ret['result'] = True
            ret['changes']['new'] = start_upload['iam_ssh_username']
        else:
            ret['comment'] = 'Upload failed.'
            ret['result'] = False
    else:
        ret['comment'] = 'Keys have been already generated and uploaded to AWS Secrets Manager.'
        ret['result'] = True
    return ret