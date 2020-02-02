# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.define "ubuntu16.04" do |testvm|
        testvm.vm.provider "virtualbox" do |vb|
            vb.memory = "512"
            vb.name = "ubuntu-xenial64"
        end
        testvm.vm.hostname = "testvm"
        testvm.vm.box_check_update = false
        testvm.vm.box = "ubuntu/xenial64"
        testvm.vm.network "private_network", type: "dhcp", subnet: "172.17.0.0/16", bridge: "bridge0"
        testvm.vm.synced_folder "../operations", "/ops"
    end

    
    config.vm.define "containers" do | container|
       container.vm.provider "docker" do |d|
           d.force_host_vm = false
           d.build_dir = "./docker"
           d.dockerfile = "testsetup"
           d.has_ssh = true
           d.name = 
       end
    end
end