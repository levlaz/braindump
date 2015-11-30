Vagrant.configure("2") do | config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.synced_folder ".", "/var/www"
    config.vm.provision :shell, path: "bootstrap.sh"

    # Port Forwarding
    config.vm.network :forwarded_port, guest: 5000, host: 5000
end
