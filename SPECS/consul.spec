Name:           consul
Version:        0.2.0
Release:        1%{?dist}
Summary:        Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            http://www.consul.io
Source0:        https://dl.bintray.com/mitchellh/consul/%{version}_linux_amd64.zip
Source1:        %{name}.sysconfig
Source2:        %{name}.service
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  systemd-units
Requires:       systemd

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
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{_sourcedir}/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}/%{_unitdir}
cp %{_sourcedir}/%{name}.service %{buildroot}/%{_unitdir}/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sysconfdir}/%{name}.d
%{_sysconfdir}/sysconfig/%{name}
%{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service
%attr(755, root, root) %{_bindir}/consul

%doc



%changelog

