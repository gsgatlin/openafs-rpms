# Module is built by dkms, we don't have any debuginfo at package build time
%global debug_package %{nil}
%define module openafs

# Define the OpenAFS sysname
%ifarch %{ix86} 
%define sysname i386_linux26
%endif
%ifarch ppc
%define sysname ppc_linux26
%endif
%ifarch ppc64
%define sysname ppc64_linux26
%endif
%ifarch x86_64
%define sysname amd64_linux26
%endif


%define basearchs i386 alpha ia64 ppc s390 x86_64

Summary:        OpenAFS Enterprise Network File System
Name:           %{module}-dkms
Version:        1.6.20.1
Release:        1%{?dist}
License:        IBM Public License
Group:          System Environment/Daemons
URL:            http://oss.software.ibm.com/developerworks/opensource/afs/downloads.html
Source0:        http://www.openafs.org/dl/openafs/%{version}/%{module}-%{version}-src.tar.bz2
Source1:        dkms-openafs.service
Source2:        dkms-openafs-rhelcleaner
Source3:        dkms-openafs
BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires:  krb5-devel, pam-devel, ncurses-devel, flex, byacc, bison, automake, autoconf
%if 0%{?rhel} == 7
BuildRequires:  systemd-units
%endif
Requires:       openafs-client = %{version}
Requires:       dkms
Requires:       kernel-devel
Provides:       openafs.ko

%description
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the DKMS enabled kernel modules for AFS.

%prep
%setup -q -n %{module}-%{version}


%build

./regen.sh

%configure --with-afs-sysname=%{sysname} --disable-kernel-module

make libafs_tree

%install
rm -rf ${RPM_BUILD_ROOT}

install -d -m 755 %{buildroot}%{_prefix}/src
cp -a libafs_tree %{buildroot}%{_prefix}/src/%{module}-%{version}

# Lifted from the Mandriva DKMS OpenAFS package
# Modified in the extreme by gsgatlin, 2/23/2015.
cat > %{buildroot}%{_prefix}/src/%{module}-%{version}/dkms.conf <<EOF

PACKAGE_VERSION="%{version}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="openafs"
MAKE[0]="( ./configure --with-linux-kernel-headers=\${kernel_source_dir}; make; mv src/libafs/MODLOAD-*/libafs.ko ./\$PACKAGE_NAME.ko )"
CLEAN="make -C src/libafs clean"
BUILT_MODULE_NAME[0]="\$PACKAGE_NAME"
DEST_MODULE_LOCATION[0]="/extra/\$PACKAGE_NAME/"
AUTOINSTALL=yes
EOF

# Fedora does not have "weak-updates" dir problem so these workarounds are RHEL only...

# Upstart init script (rhel 6 only, no fedora)
%if 0%{?rhel} == 6
mkdir -p $RPM_BUILD_ROOT/%{_initddir}/
install -D -m755 %{SOURCE3} $RPM_BUILD_ROOT/%{_initddir}/
%endif

# systemd unit file (rhel 7+ only, no fedora)
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}/
%if 0%{?rhel} > 6
install -D -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/
%endif

# actual clean up script and also another copy to be daily cron job (all RHEL only, no fedora)
%if 0%{?rhel:1}
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/dkms-openafs-rhelcleaner/
install -D -m755 %{SOURCE2} $RPM_BUILD_ROOT/%{_libexecdir}/dkms-openafs-rhelcleaner/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily/
install -D -m755 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily/
%endif


%post
%if 0%{?rhel} == 6
if [ $1 -eq 1 ] ; then
/sbin/chkconfig --add dkms-openafs >/dev/null 2>&1 || :
/sbin/chkconfig --level 2345 dkms-openafs on >/dev/null 2>&1 || :
/sbin/service dkms-openafs start >/dev/null 2>&1 || :
fi
%endif
%if 0%{?rhel} >= 7
if [ $1 -eq 1 ] ; then
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
/bin/systemctl enable dkms-openafs.service >/dev/null 2>&1 || :
/bin/systemctl start dkms-openafs.service >/dev/null 2>&1 || :
fi
%endif

dkms add -m %{module} -v %{version} --rpm_safe_upgrade
dkms build -m %{module} -v %{version} --rpm_safe_upgrade
dkms install -m %{module} -v %{version} --rpm_safe_upgrade

%preun
%if 0%{?rhel} == 6
if [ $1 -eq 0 ] ; then
/sbin/service dkms-openafs stop >/dev/null 2>&1 || :
/sbin/chkconfig --level 2345 dkms-openafs off >/dev/null 2>&1 || :
/sbin/chkconfig --del dkms-openafs >/dev/null 2>&1 || :
fi
%endif
%if 0%{?rhel} >= 7
%systemd_preun dkms-openafs.service
%endif
dkms remove -m %{module} -v %{version} --rpm_safe_upgrade --all ||:

%postun
%if 0%{?rhel} >= 7
%systemd_postun_with_restart dkms-openafs.service
%endif

%files
%defattr(-, root, root)
%{_prefix}/src/%{module}-%{version}
%if 0%{?rhel} == 6
%{_initddir}/dkms-openafs
%endif
%if 0%{?rhel} > 6
%{_unitdir}/dkms-openafs.service
%endif
%if 0%{?rhel:1}
%{_libexecdir}/dkms-openafs-rhelcleaner/dkms-openafs-rhelcleaner
%{_sysconfdir}/cron.daily/dkms-openafs-rhelcleaner
%endif



%changelog
* Thu Dec 29 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.20.1-1
- Update to 1.6.20.1
- fix for dkms-openafs-rhelcleaner running under RHEL 6.

* Fri Nov 18 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.19-1
- Update to 1.6.19

* Fri Nov 18 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.18.3-2
- fix a problem on rhel with dkms-openafs-rhelcleaner so 
  that it deletes superfluous initramfs files from /boot.

* Sun Sep 4 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.18.3-1
- Update to 1.6.18.3

* Fri Jul 22 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.18.2-1
- Update to 1.6.18.2
- Remove all 4.5 patches.

* Sat Jun 4 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.18-2
- add ./regen.sh to build section. Special thanks to
  Michael Laß from Arch Linux AUR project for the fix for 4.5 kernels.

* Tue May 31 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.18-1
- Update to 1.6.18
- Borrow 4 patches from gerrit 12264, 12265, 12268, 12274 for fedora 23+.

* Tue Mar 22 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.17-1
- Update to 1.6.17
- CVS-2016-2860
- OPENAFS-SA-2016-001

* Thu Mar 17 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.16-1
- Update to 1.6.16
- logs at /var/lib/dkms/openafs/*/build/make.log
- add conditional patches for > f23. Should be "safe"
- Add fix for RHEL 6/7 builds and "weak-updates"

* Wed Oct 28 2015 Gary Gatling <gsgatlin@ncsu.edu> 1.6.15-1
- Update to 1.6.15
- OPENAFS-SA-2015-007
- CVE-2015-7762
- CVE-2015-7763

* Thu Oct 8 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.14.1-1
- Update to OpenAFS 1.6.14.1

* Mon Aug 17 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.14-1
- Update to OpenAFS 1.6.14.

* Tue May 26 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.11.1-1
- Update to OpenAFS 1.6.11.1 for 4.0 kernels.

* Tue Mar 3 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.11-1
- Update to OpenAFS 1.6.11
- remove patch for 3.18/3.19 kernels.

* Mon Mar 2 2015 Gary Gatling <gsgatlin@ncsu.edu> 1.6.10-1
- Fix to make more like "kmod-openafs" module name and
  also changes to generated dkms.conf file.
- Lets see if this works on fedora 21+...?

* Wed Oct 18 2006 Jack Neely <jjneely@ncsu.edu>
- Created this DKMS spec file based off the openafs-2.6.spec and work
  from Mandriva's DKMS OpenAFS packages.

