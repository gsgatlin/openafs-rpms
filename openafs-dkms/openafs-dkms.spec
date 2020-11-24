# Module is built by dkms, we don't have any debuginfo at package build time
%global debug_package %{nil}
%define module openafs

# Define the OpenAFS sysname
%ifarch %{ix86} 
%define sysname i386_linux26
%endif
%ifarch ppc64
%define sysname ppc64_linux26
%endif
%ifarch ppc64le
%define sysname ppc64le_linux26
%endif
%ifarch x86_64
%define sysname amd64_linux26
%endif
%ifarch aarch64
%define sysname arm64_linux26
%endif



%define basearchs i386 ppc64 ppc64le s390 x86_64 aarch64

Summary:        OpenAFS Enterprise Network File System
Name:           %{module}-dkms
Version:        1.8.6
Release:        1%{?dist}
License:        IBM Public License
Group:          System Environment/Daemons
URL:            http://oss.software.ibm.com/developerworks/opensource/afs/downloads.html

Source0:        http://www.openafs.org/dl/openafs/%{version}/%{module}-%{version}-src.tar.bz2

Patch0:        openafs-1.8.6-GCC-10.patch
Patch1:        openafs-1.8.6-replace-kernel5.8_setsockopt-with-new-funcs.patch
Patch2:        openafs-1.8.6-kernel5.8-do-not-set-name-field-in-backing_dev_info.patch
Patch3:        openafs-1.8.6-kernel5.8-use-lru_cache_add.patch
Patch4:        openafs-1.8.6-kernel5.9-Remove-HAVE_UNLOCKED_IOCTL-COMPAT_IOCTL.patch


BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires:  krb5-devel, pam-devel, ncurses-devel, flex, byacc, bison, automake, autoconf
%if 0%{?_with_systemd}
BuildRequires: systemd-units
%endif
BuildRequires:  libtool
Requires:       openafs-client = %{version}
Requires:       dkms
Requires:       elfutils-libelf-devel
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

%if 0%{?fedora} >= 31
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%endif



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
AUTOINSTALL="yes"
EOF

%pre
%if 0%{?fedora} >= 31
dkms remove -m %{module} -v %{version} &>/dev/null
%else
dkms remove -m %{module} -v %{version} --rpm_safe_upgrade --all &>/dev/null
%endif
exit 0

%post
%if 0%{?fedora} >= 31
dkms add -m %{module} -v %{version} &>/dev/null
dkms build -m %{module} -v %{version} &>/dev/null
dkms install -m %{module} -v %{version} &>/dev/null
%else
dkms add -m %{module} -v %{version} --rpm_safe_upgrade &>/dev/null
dkms build -m %{module} -v %{version} --rpm_safe_upgrade &>/dev/null
dkms install -m %{module} -v %{version} --rpm_safe_upgrade &>/dev/null
%endif
exit 0

%preun
%if 0%{?fedora} >= 31
dkms remove -m %{module} -v %{version} &>/dev/null
%else
dkms remove -m %{module} -v %{version} --rpm_safe_upgrade --all &>/dev/null
%endif
exit 0
%postun

%files
%defattr(-, root, root)
%{_prefix}/src/%{module}-%{version}


%changelog
* Mon Nov 23 2020 Gary Gatling <gsgatlin@ncsu.edu> 1.8.6-2
- fix for kernel 5.9

* Thu Sep 24 2020 Gary Gatling <gsgatlin@ncsu.edu> 1.8.6-1
- Try to build newest version. 1.8.6
- fix for dkms issues on fedora distro and fix for kernel 5.8

* Sat Oct 26 2019 Gary Gatling <gsgatlin@ncsu.edu> 1.8.5-1
- Try to build newest version. 1.8.5

* Thu Oct 17 2019 Gary Gatling <gsgatlin@ncsu.edu> 1.8.4-1
- Try to build newest version. 1.8.4

* Wed Aug 7 2019 Gary Gatling <gsgatlin@ncsu.edu> 1.8.3-1
- Try to build newest version. 1.8.3

* Mon Mar 25 2019 Gary Gatling <gsgatlin@ncsu.edu> 1.8.2-4
- Fix for compile issues on fedora29 5.0 kernel.

* Fri Feb 15 2019 Gary Gatling <gsgatlin@ncsu.edu> 1.8.2-3
- Fixes for selinux issues on rhel 8 beta.

* Thu Feb 14 2019 Gary Gatling <gsgatlin@ncsu.edu> 1.8.2-2
- Fixes for aarch64 platform.

* Tue Feb 12 2019 Gary Gatling <gsgatlin@ncsu.edu> 1.8.2-1
- Try to build newest version. 1.8.2

* Sat Mar 10 2018 Gary Gatling <gsgatlin@ncsu.edu> 1.8.0pre5-1
- Try to build newest version. 1.8.X

* Fri Mar 2 2018 Gary Gatling <gsgatlin@ncsu.edu> 1.6.22.2-2
- add rh75enotdir patch for rhel/centos 7.5.

* Wed Feb 7 2018 Gary Gatling <gsgatlin@ncsu.edu> 1.6.22.2-1
- Update to 1.6.22.2 for 4.15 kernel.

* Sun Dec 10 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.22-1
- Update to 1.6.22 for 4.14 kernel.

* Thu Oct 5 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.21.1-1
- Update to 1.6.21.1 for 4.13 kernel.

* Tue Jul 25 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.21-1
- Update to 1.6.21 for 4.12 kernel.

* Fri May 26 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.20.2-1
- remove "NO_WEAK_MODULES=yes" to dkms.conf file.
- remove Linux-4.10-have_submounts-is-gone.patch.
- add gcc-7.0.1-STRUCT_GROUP_INFO_HAS_GID-always.patch for gcc >= 7.0.1
- Update to 1.6.20.2

* Mon May 08 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.20.1-4
- add "NO_WEAK_MODULES=yes" to dkms.conf file.

* Tue Mar 21 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.20.1-3
- add patch for 4.10 kernels on fedora distro.

* Tue Mar 14 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.20.1-2
- remove all services and unit files. Its not the best way to fix the 
  problem of superfluous initramfs files from /boot. Lets try something else.
- Test add another remove in pre scriptlet.

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

