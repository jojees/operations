include:
    - pkgs.openssh-client

generate_ssh_key:
  cmd.run:
    - name: ssh-keygen -t rsa -m PEM -b 4096 -C "custom_apps" -P "sampleq" -q -f ~/.ssh/id_rsa_codecomit
    - runas: operations
    - unless: test -f ~/.ssh/id_rsa_codecomit
