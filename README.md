# RPM Spec for Consul

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/consul`
* Config: `/etc/consul/`
* Shared state: `/var/lib/consul/`
* Sysconfig: `/etc/sysconfig/consul`
* WebUI: `/usr/share/consul/`

# Build

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
    wget $URL/${VER}_linux_amd64.zip -O $HOME/rpmbuild/SOURCES/${VER}_linux_amd64.zip
    wget $URL/${VER}_web_ui.zip -O $HOME/rpmbuild/SOURCES/${VER}_web_ui.zip
    ```

* Build the RPM.
    ```
    rpmbuild -ba rpmbuild/SPECS/consul.spec
    ```

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
