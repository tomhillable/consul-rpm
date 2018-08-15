%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      0.19.5
%endif

Name:           consul-template
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        consul-template watches a series of templates on the file system, writing new changes when Consul is updated. It runs until an interrupt is received unless the -once flag is specified.

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
consul-template watches a series of templates on the file system, writing new changes when Consul is updated. It runs until an interrupt is received unless the -once flag is specified.

%prep
%setup -q -c

%install
mkdir -p %{buildroot}/%{_bindir}
cp consul-template %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}.d
cp %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}.d/consul-template.json-dist
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
cp %{SOURCE3} %{buildroot}/%{_initrddir}/consul-template
cp %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
%endif

%pre
getent group consul-template >/dev/null || groupadd -r consul-template
getent passwd consul-template >/dev/null || \
    useradd -r -g consul-template -d /var/lib/consul-template -s /sbin/nologin \
    -c "consul-template user" consul-template
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
%dir %attr(750, root, consul-template) %{_sysconfdir}/%{name}.d
%attr(640, root, consul-template) %{_sysconfdir}/%{name}.d/consul-template.json-dist
%dir %attr(750, consul-template, consul-template) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%endif
%attr(755, root, root) %{_bindir}/consul-template

%doc


%changelog
* Sun Mar 25 2018 ambakshi ambakshi@gmail.com
- Bump version to 0.19.4
* Tue Aug 22 2017 mh <mh@immerda.ch> - 0.19.0-1
- Bumped version to 0.19.0
* Wed Apr 05 2017 mh <mh@immerda.ch>
- Bumped version to 0.18.2
- remove legacy location /etc/consul-template/
* Wed Sep 28 2016 Andy Bohne <andy@andrewbohne.com>
- Bumped version to 0.16.0
* Thu Jun 30 2016 Paul Lussier <pllsaph@gmail.com>
- Created new spec file to build consul-template for rhel7
