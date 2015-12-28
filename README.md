# RPM Spec for Consul

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/consul`
* Config: `/etc/consul/`
* Shared state: `/var/lib/consul/`
* Sysconfig: `/etc/sysconfig/consul`
* WebUI: `/usr/share/consul/`

# Using

Create the RPMs using one of the techniques outlined in the Build section below.

## Pre-built packages

Pre-built packages are maintained via the [Fedora Copr](https://copr.fedoraproject.org/coprs/) system. For more information, please see the [duritong/consul](https://copr.fedoraproject.org/coprs/duritong/consul/) repository on Copr.

# Build

There are various methods how you can build the consul & consul-ui RPMs, currently we have Manual & Vagrant based builds documented.

## Manual

Or, do it manually by building the RPM as a non-root user from your home directory:

* Check out this repo. Seriously - check it out. Nice.
    ```
    git clone <this_repo_url>
    ```

* Install `rpmdevtools` and `mock`.
    ```
    sudo yum install rpmdevtools mock
    ```

* Set up your rpmbuild directory tree.
    ```
    rpmdev-setuptree
    ```

* Link the spec file and sources.
    ```
    ln -s $HOME/consul-rpm/SPECS/consul.spec $HOME/rpmbuild/SPECS/
    find $HOME/consul-rpm/SOURCES -type f -exec ln -s {} $HOME/rpmbuild/SOURCES/ \;
    ```

* Download remote source files.
    ```
    spectool -g -R rpmbuild/SPECS/consul.spec
    ```

* Spectool may fail if your distribution has an older version of cURL (CentOS
  6.x, for example) - if so, use Wget instead.
    ```
    VER=`grep Version rpmbuild/SPECS/consul.spec | awk '{print $2}'`
    URL='https://dl.bintray.com/mitchellh/consul'
    wget $URL/consul_${VER}_linux_amd64.zip -O $HOME/rpmbuild/SOURCES/consul_${VER}_linux_amd64.zip
    wget $URL/consul_${VER}_web_ui.zip -O $HOME/rpmbuild/SOURCES/consul_${VER}_web_ui.zip
    ```

* Build the RPM.
    ```
    rpmbuild -ba rpmbuild/SPECS/consul.spec
    ```

## Vagrant

If you have Vagrant installed:

* Check out this repo.
    ```
    git clone https://github.com/tomhillable/consul-rpm
    ```

* Edit Vagrantfile to point to your favourite box (Bento CentOS7 in this example).
    ```
    config.vm.box = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_centos-7.0_chef-provisionerless.box"
    ```

* Vagrant up! The rpms will be copied to working directory after provisioning.
    ```
    vagrant up
    ```

## Docker

If you prefer building it with docker:

* Build the docker image
    Amend the ```Dockerfile``` header if you want a specific OS build. Default is centos7
    ```
    docker build -t consul:build .
    ```

* Run the build
    ```
    docker run -v $HOME/consul-rpms:/RPMS consul:build
    ```

* Retrieve the built RPMs from ```$HOME/consul-rpms```


## Result

Two RPMS: one each for the Consul binary and the WebUI.

# Run

* Install the RPM.
* Put config files in `/etc/consul/`.
* Change command line arguments to consul in `/etc/sysconfig/consul`.
  * Add `-bootstrap` **only** if this is the first server and instance.
* Start the service and tail the logs `systemctl start consul.service` and `journalctl -f`.
  * To enable at reboot `systemctl enable consul.service`.
* Consul may complain about the `GOMAXPROCS` setting. This is safe to ignore;
  however, the warning can be supressed by uncommenting the appropriate line in
  `/etc/sysconfig/consul`.

## Config

Config files are loaded in lexicographical order from the `config-dir`. Some
sample configs are provided.

# More info

See the [consul.io](http://www.consul.io) website.
