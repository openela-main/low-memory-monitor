Name:           low-memory-monitor
Version:        2.1
Release:        4%{?dist}
Summary:        Monitors low-memory conditions

License:        GPLv3+
URL:            https://gitlab.freedesktop.org/hadess/low-memory-monitor
Source0:        https://gitlab.freedesktop.org/hadess/low-memory-monitor/uploads/9c201566253ed52a9054f514f9904e48/low-memory-monitor-2.1.tar.xz

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  gtk-doc
BuildRequires:  systemd

%description
The Low Memory Monitor is an early boot daemon that will monitor memory
pressure information coming from the kernel, and, first, send a signal
to user-space applications when memory is running low, and then activate
the kernel's OOM killer when memory is running really low.

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc

This package contains the documentation for %{name}.

%prep
%autosetup


%build
%meson -Dgtk_doc=true -Dtrigger_kernel_oom=false
%meson_build


%install
%meson_install


%post
%systemd_post low-memory-monitor.service

%preun
%systemd_preun low-memory-monitor.service

%postun
%systemd_postun_with_restart low-memory-monitor.service

%triggerun -- low-memory-monitor < 2.0-6

# This is for upgrades from previous versions before low-memory-monitor became part
# of the system daemons.
systemctl --no-reload preset low-memory-monitor.service &>/dev/null || :

%files
%license COPYING
%doc NEWS README.md
%{_unitdir}/low-memory-monitor.service
%{_libexecdir}/low-memory-monitor
%{_datadir}/dbus-1/system.d/org.freedesktop.LowMemoryMonitor.conf

%files doc
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/%{name}/

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2.1-4
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2.1-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 17 2020 Bastien Nocera <bnocera@redhat.com> - 2.1-1
+ low-memory-monitor-2.1-1
- Update to 2.1
- Don't poke at sysrq proc file (#1898524)

* Wed Oct 28 2020 Bastien Nocera <bnocera@redhat.com> - 2.0-6
+ low-memory-monitor-2.0-6
- Reload presets when updating from an older version to enable daemon

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 19 2019 Bastien Nocera <bnocera@redhat.com> - 2.0-3
+ low-memory-monitor-2.0-3
- Disable OOM killer by default for now
- Import into Fedora (#1769843)

* Mon Nov 18 2019 Bastien Nocera <bnocera@redhat.com> - 2.0-2
+ low-memory-monitor-2.0-2
- Rename -docs subpackage to -doc

* Thu Nov 14 2019 Bastien Nocera <bnocera@redhat.com> - 2.0-1
+ low-memory-monitor-2.0-1
- Update to 2.0

* Thu Nov 07 2019 Bastien Nocera <bnocera@redhat.com> - 1.1-2
+ low-memory-monitor-1.1-2
- Add missing requires for the main package in the docs one
- Add config tag for low-memory-monitor.conf

* Thu Nov 07 2019 Bastien Nocera <bnocera@redhat.com> - 1.1-1
+ low-memory-monitor-1.1-1
- Initial Fedora packaging
