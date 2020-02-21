#include:
#  - states.generate_ssh_key_pair
#  - states.aws_secrets_manager

python-pip3:
  pkg.installed:
    - pkgs:
      - python3-pip
      - python-pip

awscli:
  pip.installed:
    - name: awscli
    - bin_env: '/usr/bin/pip3'
    - require:
      - pkg: python-pip3

#Ensure AWS IAM user has the public key:
#  iam_support.iam_sshkey_exists:
#    - name: codecommit
#    - keypath: ~/.ssh/id_rsa_codecomit
#    - user: operations
#    - cf_logical_id: ScanningAutomationUser
