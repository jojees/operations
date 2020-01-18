# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/xenial64"
    config.vm.hostname = "testvm"
    config.vm.box_check_update = false
    config.vm.define "ubuntu16.04"
    config.vm.provider "virtualbox" do |vb|
        vb.memory = "512"
        vb.name = "ubuntu-xenial64"
    end
    config.vm.network "private_network", type: "dhcp", subnet: "172.17.0.0/16", bridge: "bridge0"
    config.vm.synced_folder "../operations", "/ops"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
