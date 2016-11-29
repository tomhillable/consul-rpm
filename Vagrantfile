# -*- mode: ruby -*-
# vi: set ft=ruby :

$rpmbuild_script = <<SCRIPT

echo "Provisioning started, installing packages..."
sudo yum -y install rpmdevtools mock

echo "Setting up rpm dev tree..."
rpmdev-setuptree

echo "Linking files..."
ln -s /vagrant/SPECS/consul.spec $HOME/rpmbuild/SPECS/
find /vagrant/SOURCES -type f -exec ln -s {} $HOME/rpmbuild/SOURCES/ \\;

echo "Downloading dependencies..."
spectool -g -R rpmbuild/SPECS/consul.spec

echo "Building rpm..."
rpmbuild -ba rpmbuild/SPECS/consul.spec

echo "Copying rpms back to shared folder..."
mkdir /vagrant/RPMS
find $HOME/rpmbuild -type d -name "RPMS" -exec cp -r {} /vagrant/ \\;
find $HOME/rpmbuild -type d -name "SRPMS" -exec cp -r {} /vagrant/ \\;

SCRIPT


Vagrant.configure(2) do |config|

  config.vm.box = ""

  config.vm.provision "shell", inline: $rpmbuild_script, privileged: false

end
