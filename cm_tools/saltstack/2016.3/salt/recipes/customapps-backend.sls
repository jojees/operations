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