%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      1.5.2
%endif

Name:           consul
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            http://www.consul.io
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init
Source4:        %{name}.json
Source5:        %{name}.logrotate
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%else
Requires:       logrotate
%endif
Requires(pre): shadow-utils


%description
Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register themselves and to discover other services via a DNS or HTTP interface. External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert operators about any issues in a cluster. The integration with service discovery prevents routing traffic to unhealthy hosts and enables service level circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination, leader election and more. The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support any number of regions without complex configuration.

%prep
%setup -q -c

%install
mkdir -p %{buildroot}/%{_bindir}
cp consul %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}.d
cp %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}.d/consul.json-dist
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
cp %{SOURCE3} %{buildroot}/%{_initrddir}/consul
cp %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
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
%dir %attr(750, root, consul) %{_sysconfdir}/%{name}.d
%attr(640, root, consul) %{_sysconfdir}/%{name}.d/consul.json-dist
%dir %attr(750, consul, consul) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%endif
%attr(755, root, root) %{_bindir}/consul



%doc


%changelog
* Thu May 08 2019 Igor Krutyakov <lebriquet@gmail.com>
- Bump version to 1.4.4

* Sun Feb 24 2019 Ilya Voronin <ivoronin@gmail.com>
- Bump version to 1.4.2

* Fri Nov 30 2018 Michael Mraz <michaelmraz@gmail.com>
- Bump version to 1.4.0

* Sun Mar 25 2018 ambakshi ambakshi@gmail.com
- Bump version to 1.0.6

* Fri Aug 18 2017 leeuwenrjj leeuwenrjj@gmail.com
- Bump version to 0.9.2
- Fix issue with prep

* Tue Jul 25 2017 atumasov multibutterbread@gmail.com
- Bump version to 0.9.0
- Remove outdated UI package https://github.com/hashicorp/consul/blob/master/CHANGELOG.md#090-july-20-2017

* Mon Apr 24 2017 mh <mh@immerda.ch>
- Bump to 0.8.1
- Fix init script to check for http port to be listening

* Wed Apr 05 2017 mh <mh@immerda.ch>
- Bump to 0.8.0
- remove legacy location /etc/consul/

* Tue Feb 21 2017 Rumba <ice4o@hotmail.com>
- Bump to 0.7.5

* Wed Feb 8 2017 Jasper Lievisse Adriaanse <j@jasper.la>
- Bump to 0.7.4

* Thu Jan 26 2017 mh <mh@immerda.ch>
- Bump to 0.7.3

* Fri Dec 23 2016 Michael Mraz <michaelmraz@gmail.com>
- Change default configs directory to /etc/consul.d and /etc/consul-template.d
  while the old ones are still supported

* Thu Dec 22 2016 Rumba <ice4o@hotmail.com>
- Bump to 0.7.2

* Wed Dec 14 2016 Rumba <ice4o@hotmail.com>
- Bump to 0.7.1

* Wed Sep 21 2016 Rumba <ice4o@hotmail.com>
- Bump to 0.7.0

* Tue Jun 28 2016 Konstantin Gribov <grossws@gmail.com>
- Bump to v0.6.4

* Sun Jan 31 2016 mh <mh@immerda.ch>
- Bump to v0.6.3

* Fri Dec 11 2015 mh <mh@immerda.ch>
- Bump to v0.6

* Sun Oct 18 2015 mh <mh@immerda.ch>
- logrotate logfile on EL6 - fixes #14 & #15

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
