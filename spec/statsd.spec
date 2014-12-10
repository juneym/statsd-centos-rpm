%bcond_with systemd

Name:           statsd
Version:        0.7.2
Release:        1%{?dist}
Summary:        monitoring daemon, that aggregates events received by udp in 10 second intervals
Group:          Applications/Internet
License:        Etsy open source license
URL:            https://github.com/renecunningham/statsd-rpm
Vendor:         Etsy
Packager:       Rene Cunningham <rene@compounddata.com>
Source0:        %{name}-%{version}.tar.gz
Source1:	statsd-sysvinit
Source2:        statsd-systemd
Source3:        config.js
Source4:        statsd-defaults
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
Requires:       nodejs

%if %{with systemd}
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units
%endif

%description
Simple daemon for easy stats aggregation  

%prep
%setup -q

%build

%install
%{__mkdir_p} %{buildroot}/usr/share/statsd/backends %{buildroot}/usr/share/statsd/lib %{buildroot}/usr/share/statsd/bin
%{__install} -Dp -m0644 stats.js %{buildroot}/usr/share/statsd/
%{__install} -Dp -m0644 lib/config.js lib/logger.js lib/set.js lib/process_metrics.js %{buildroot}/usr/share/statsd/lib/
%{__install} -Dp -m0644 lib/helpers.js lib/process_mgmt.js lib/mgmt_console.js %{buildroot}/usr/share/statsd/lib/
%{__install} -Dp -m0644 backends/{console.js,graphite.js} %{buildroot}/usr/share/statsd/backends/
%{__install} -Dp -m0655 bin/statsd %{buildroot}/usr/share/statsd/bin/

%{__install} -Dp -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/%{name}
%if %{with systemd}
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%else
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif

%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__install} -Dp -m0644 %{SOURCE3}  %{buildroot}%{_sysconfdir}/%{name}/config.js

%{__mkdir_p} %{buildroot}%{_localstatedir}/lock/subsys
touch %{buildroot}%{_localstatedir}/lock/subsys/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_localstatedir}/lib/%{name} \
    -s /sbin/nologin -c "%{name} daemon" %{name}
exit 0

%preun
%if %{with systemd}
systemctl stop %{name}
%systemd_preun $name.service
%else
service %{name} stop
%endif
exit 0

%postun
if [ $1 = 0 ]; then
%if %{with systemd}
%systemd_postun
%else
	chkconfig --del %{name}
	getent passwd %{name} >/dev/null && \
	userdel -r %{name} 2>/dev/null
%endif
fi
exit 0

%post
%if %{with systemd}
%systemd_post ${name}.service
systemctl start %{name}
%else
chkconfig --add %{name}
service %{name} start
%endif

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%doc exampleConfig.js
%doc exampleProxyConfig.js
%doc Changelog.md

/usr/share/%{name}/*
%{_sysconfdir}/default/%{name}
%if %{with systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

%config %{_sysconfdir}/%{name}
%ghost %{_localstatedir}/lock/subsys/%{name}

%changelog
* Wed Dec 10 2014 Scott O'Neil <scott@cpanel.net> 0.7.2-1
- Updating from upstream
* Mon Dec  1 2014 Scott O'Neil <scott@cpanel.net> 0.7.0-4
- Adding support for systemd with --with-systemd build option
* Mon Dec  1 2014 Scott O'Neil <scott@cpanel.net> 0.7.0-3
- Adding sysconfig file for init script to allow for customizing without
  editing init script
* Thu Nov 27 2014 Scott O'Neil <scott@cpanel.net> 0.7.0-2
- Fixing stop part of init script
* Sun Jun 10 2012 Rene Cunningham <rene@compounddata.com> 0.3.0-1
- initial build
