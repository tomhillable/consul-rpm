RPM Spec for Consul
======================

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/consul`
* Config: `/etc/consul.d/`
* Sysconfig: `/etc/sysconfig/consul`

To Build
---------

To build the RPM (non-root user):

1. Check out this repo
2. Install rpmdevtools and mock 

    ```
    sudo yum install rpmdevtools mock
    ```
3. Set up your rpmbuild directory tree

    ```
    rpmdev-setuptree
    ```
4. Link the spec file and sources from the repository into your rpmbuild/SOURCES directory

    ```
    ln -s ${repo}/SPECS/consul.spec rpmbuild/SPECS/
    ln -s ${repo}/SOURCES/* rpmbuild/SOURCES/
    ```
5. Download remote source files

    ```
    spectool -g -R rpmbuild/SPECS/consul.spec
    ```
6. Build the RPM

    ```
    rpmbuild -ba rpmbuild/SPECS/consul.spec
    ```

7. (Optional) Build for another Fedora release

    ```
    sudo mock -r fedora-19-x86_64 --resultdir rpmbuild/RPMS/x86_64/ rpmbuild/SRPMS/consul-0.2.0-1.fc20.src.rpm 
    ```

To run
---------------

1. Install the rpm
2. Put config files in `/etc/consul.d/`
3. Change command line arguments to consul in `/etc/sysconfig/consul`. **Note:** You should remove `-bootstrap` if this isn't the first server.
4. Start the service and tail the logs `systemctl start consul.service` and `journalctl -f`
  * To enable at reboot `systemctl enable consul.service`

More info
---------
See the [consul.io](http://www.consul.io) website.
