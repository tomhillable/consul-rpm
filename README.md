# RPM Spec for Consul

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/consul`
* Config: `/etc/consul/`
* Shared state: `/var/lib/consul/`
* Sysconfig: `/etc/sysconfig/consul`
* WebUI: `/usr/share/consul/`

# Build

Build the RPM as a non-root user from your home directory:

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
    ln -s $HOME/consul-rpm/SPECS/consul.spec rpmbuild/SPECS/
    find $HOME/consul-rpm/SOURCES -type f -exec ln -s {} rpmbuild/SOURCES/ \;
    ```

* Download remote source files
    ```
    spectool -g -R rpmbuild/SPECS/consul.spec
    ```

* Build the RPM
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

## Config

Config files are loaded in lexicographical order from the `config-dir`. Some
sample configs are provided.

# More info

See the [consul.io](http://www.consul.io) website.
