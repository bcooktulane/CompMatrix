# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("1") do |config|
  config.vm.box = "precise64"

  #config.vm.customize(["modifyvm", :id, "--nictype1", "Am79C973"])
  config.vm.forward_port(8000, 8000)

  config.vm.provision :chef_client do |chef|
      chef.log_level = :info
      chef.node_name = "pricecompare-vagrant"
      chef.validation_client_name = "lojack"
      chef.validation_key_path = "~/.chef/lojack.pem"
      chef.chef_server_url = "http://chef.bablmedia.com:4000"
      chef.run_list = ["role[vagrant]"]
  end
end
