Name:           consul
Version:        0.5.2
Release:        2%{?dist}
Summary:        Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            http://www.consul.io
Source0:        https://dl.bintray.com/mitchellh/%{name}/%{version}_linux_amd64.zip
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init
Source4:        https://dl.bintray.com/mitchellh/%{name}/%{version}_web_ui.zip
Source5:        %{name}.json
Source6:        %{name}-ui.json
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%endif
Requires(pre): shadow-utils

%package ui
Summary: Consul Web UI
Requires: consul = %{version}

%description
Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register themselves and to discover other services via a DNS or HTTP interface. External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert operators about any issues in a cluster. The integration with service discovery prevents routing traffic to unhealthy hosts and enables service level circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination, leader election and more. The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support any number of regions without complex configuration.

%description ui
Consul comes with support for a beautiful, functional web UI. The UI can be used for viewing all services and nodes, viewing all health checks and their current status, and for reading and setting key/value data. The UI automatically supports multi-datacenter.

%prep
%setup -q -c -b 4

%install
mkdir -p %{buildroot}/%{_bindir}
cp consul %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
cp %{SOURCE5} %{buildroot}/%{_sysconfdir}/%{name}/consul.json-dist
cp %{SOURCE6} %{buildroot}/%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}/%{_datadir}/%{name}-ui
cp -r dist/* %{buildroot}/%{_prefix}/share/%{name}-ui

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
mkdir -p %{buildroot}/%{_initrddir}
cp %{SOURCE3} %{buildroot}/%{_initrddir}/consul
%endif

%pre
getent group consul >/dev/null || groupadd -r consul
getent passwd consul >/dev/null || \
    useradd -r -g consul -d /var/lib/consul -s /sbin/nologin \
    -c "consul.io user" consul
exit 0

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %attr(750, root, consul) %{_sysconfdir}/%{name}
%attr(640, root, consul) %{_sysconfdir}/%{name}/consul.json-dist
%dir %attr(750, consul, consul) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%attr(755, root, root) %{_bindir}/consul

%files ui
%config(noreplace) %attr(-, root, consul) %{_prefix}/share/%{name}-ui
%attr(640, root, consul) %{_sysconfdir}/%{name}/consul-ui.json


%doc


%changelog
* Sun Oct 18 2015 mh <mh@immerda.ch>
- log to syslog by default - fixes #14 & #15

* Tue May 19 2015 nathan r. hruby <nhruby@gmail.com>
- Bump to v0.5.2

* Fri May 15 2015 Dan <phrawzty@mozilla.com>
- Bump to v0.5.1

* Mon Mar 9 2015 Dan <phrawzty@mozilla.com>
- Internal maintenance (bump release)

* Fri Mar 6 2015 mh <mh@immerda.ch>
- update to 0.5.0
- fix SysV init on restart
- added webui subpackage
- include statedir in package
- run as unprivileged user
- protect deployed configs from overwrites

* Thu Nov 6 2014 Tom Lanyon <tom@netspot.com.au>
- updated to 0.4.1
- added support for SysV init (e.g. EL <7)

* Wed Oct 8 2014 Don Ky <don.d.ky@gmail.com>
- updated to 0.4.0
