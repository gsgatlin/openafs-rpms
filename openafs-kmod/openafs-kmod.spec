# Define the kmod package name here.
%define  kmod_name openafs

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

# Define the pre macro to build OpenAFS pre releases
# define pre pre1.1
%define pre %nil

%if 0%{?rhel} == 6
# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 2.6.32-696.1.1.el6.%{_target_cpu}}
%endif

%if 0%{?rhel} == 7
# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 3.10.0-514.16.1.el7.%{_target_cpu}}
%endif


Name:           %{kmod_name}-kmod
Version:        1.6.20.2
Release:        1%{?pre}%{?dist}
Group:          System Environment/Kernel
License:        IBM
Summary:        %{kmod_name} kernel module(s)
URL:            http://www.openafs.org

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build-%(%{__id_u} -n)
ExclusiveArch:  i586 i686 x86_64 ppc ppc64
BuildRequires:  pam-devel, ncurses-devel, flex, byacc, bison, automake
BuildRequires:  kernel-devel, kernel-headers

# This actually gets set in kmodtool-*-openafs.sh  
# so the next line is not really working like you would expect it to.
Provides:       openafs.ko
Conflicts:      openafs-dkms
%if 0%{?fedora:1}
BuildRequires:  kmodtool
BuildRequires:  buildsys-build-rpmfusion-kerneldevpkgs-current
%endif
# Sources.
Source0:  	    http://www.openafs.org/dl/openafs/%{version}/%{kmod_name}-%{version}%{?pre}-src.tar.bz2
Source5:	    LICENSE
Source10: 	    kmodtool-el6-%{kmod_name}.sh
Source15: 	    kmodtool-el7-%{kmod_name}.sh
Source20:       kmodtool-fedora-%{kmod_name}.sh
Patch0:         gcc-7.0.1-STRUCT_GROUP_INFO_HAS_GID-always.patch



# Magic hidden below.

# Taken from: http://elrepo.org/tiki/kmodtool-el6
# Modified for our own purposes.
# Because of how this works patching was not an option.
%if 0%{?rhel} == 6
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}
%endif

# Taken from: http://elrepo.org/tiki/kmodtool-el7
# Modified for our own purposes.
# Because of how this works patching was not an option.
%if 0%{?rhel} == 7
%{expand:%(sh %{SOURCE15} rpmtemplate %{kmod_name} %{kversion} "")}
%endif

# Taken from: kmodtool-1-23 package from rpmfusion yum repository.
# Modified for our own purposes.
# Because of how this works patching was not an option.
%if 0%{?fedora:1}
# kmodtool does its magic here
%{expand:%(%{SOURCE20} --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }
%endif

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provides the %{kmod_name} kernel module(s).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep

%if 0%{?fedora:1}
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
%{SOURCE20}  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


%setup -q -c -T -a 0

# apply patches and do other stuff here
pushd %{kmod_name}-%{version}%{pre}
./regen.sh
popd

for kernel_version in %{?kernel_versions} ; do
    cp -a %{kmod_name}-%{version}%{pre} _kmod_build_${kernel_version%%___*}
done
%else

%setup -q -n %{kmod_name}-%{version}%{?pre}
echo "override %{kmod_name} * weak-updates/%{kmod_name}" \
    > kmod-%{kmod_name}.conf
%endif

%if 0%{?fedora:1}
%patch0 -p1 -b .411fix
%endif

%build
%if 0%{?fedora:1}
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}
    %{configure} --with-afs-sysname=%{sysname} --enable-kernel-module \
        --disable-linux-syscall-probing  \
        --with-linux-kernel-headers="${kernel_version##*__}"
    make MPS=MP only_libafs
    popd
done
%else
ksrc=%{_usrsrc}/kernels/%{kversion}

%{configure} --with-afs-sysname=%{sysname} --enable-kernel-module \
    --disable-linux-syscall-probing  \
    --with-linux-kernel-headers="${ksrc}"
%{__make} MPS=MP only_libafs
%endif

%install
%if 0%{?fedora:1}
rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do

    install -d -m 755 ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install -m 755 _kmod_build_${kernel_version%%___*}/src/libafs/MODLOAD-${kernel_version%%___*}-MP/libafs.ko \
        ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{kmod_name}.ko
    chmod u+x ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{kmod_name}.ko
done

%{?akmod_install}

%else
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=/lib/modules/%{kversion}/extra/%{kmod_name}
ksrc=%{_usrsrc}/kernels/%{kversion}

%{__install} -d ${RPM_BUILD_ROOT}/${INSTALL_MOD_DIR}
%{__install} -m 755 src/libafs/MODLOAD-%{kversion}-MP/libafs.ko \
    ${RPM_BUILD_ROOT}/${INSTALL_MOD_DIR}/%{kmod_name}.ko

%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/

%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} %{SOURCE5} \
    %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/

# Set the module(s) to be executable, so that they will be 
# stripped when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} a+x \{\} \;

# Remove the files that we do not require.
%{__rm} -f %{buildroot}/lib/modules/%{kversion}/modules.*
%endif

%clean
%{__rm} -rf %{buildroot}

%changelog
* Fri May 26 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.20.2-1
- add gcc-7.0.1-STRUCT_GROUP_INFO_HAS_GID-always.patch for gcc >= 7.0.1
- Update to 1.6.20.2

* Tue Mar 14 2017 Gary Gatling <gsgatlin@ncsu.edu> 1.6.20.1-1
- Update to 1.6.20.1

* Fri Mar 25 2016 Gary Gatling <gsgatlin@ncsu.edu> 1.6.17-1
- Update to 1.6.17
- CVS-2016-2860
- OPENAFS-SA-2016-001

* Wed Feb 17 2016 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.16-1
- Update to new version.

* Wed Oct 28 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.15-1
- Update to new version.
- OPENAFS-SA-2015-007
- CVE-2015-7762
- CVE-2015-7763

* Mon Aug 17 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.14-1
- Update to new version.

* Wed Jun 10 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.11.1-1
- Update to new version.

* Tue Mar 31 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.11-4
- Fix for RHEL 7 kernel version.

* Mon Mar 23 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.11-3
- Fixes for fedora 20, 21, 22. This rpm now works for RHEL 6/7 and fedora.

* Fri Mar 20 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.11-0.2
- Fix for RHEL 7 kernel version.

* Tue Mar 3 2015 Gary Gatling <gsgatlin@ncsu.edu> - 1.6.11-0.1
- Update to OpenAFS 1.6.11
- remove patch for 3.18/3.19 kernels.
- Fix a typo in the spec file for el5/6 kmod-el*-openafs.sh
- Remove kmodtool-el5-openafs.sh. The packaging is just too different...

* Mon Mar 2 2015 Gary Gatling <gsgatlin@ncsu.edu> 0:1.6.10-1
- Add kmodtool-el7-openafs.sh source.
- Update to 1.6.10
- Modify kmodtool-el7-openafs.sh and kmodtool-el6-openafs.sh 
  provides lines to match dkms rpm.
- Add a kmodtool-el5-openafs.sh

* Fri Feb 06 2015 Gary Gatling <gsgatlin@ncsu.edu> 0:1.6.7-2
- Rebuild for el7 distro.

* Mon Apr 14 2014 Gary Gatling <gsgatlin@ncsu.edu> 0:1.6.7-1
- Update to 1.6.7
- CVE-2014-0159

* Sun Nov 24 2013 Gary Gatling <gsgatlin@ncsu.edu> 0:1.6.5-5
- Rebuild package for RHEL 6.5.

* Wed Jul 24 2013 Jack Neely <jjneely@ncsu.edu> 0:1.6.5-1
- Update to 1.6.5
- CVE-2013-4134
- CVE-2013-4135

* Thu Jun 27 2013 Jack Neely <jjneely@ncsu.edu> 0:1.6.4-1
- Update to 1.6.4

* Mon Mar 04 2013 Jack Neely <jjneely@ncsu.edu> 0:1.6.2-1
- Bump to 1.6.2 to fix CVE-2013-1794 and CVE-2013-1795

* Thu Feb 21 2013 Jack Neely <jjneely@ncsu.edu> 0:1.6.1-5
- Rebuild with kernel 2.6.32-358.el6
- The binary kmods set Requires: kernel >= 2.6.32-358.el6 as they
  only work with those kernels

* Wed Aug 15 2012 Jack Neely <jjneely@ncsu.edu> 0:1.6.1-2
- Rebuild

* Tue Apr 03 2012 Jack Neely <jjneely@ncsu.edu> 0:1.6.1-1
- Update to 1.6.1 final

* Thu Jan 26 2012 Jack Neely <jjneely@ncsu.edu> 0:1.6.1-0.pre1.1
- Update to OpenAFS 1.6.1pre2 -- or what I think will be released
  as 1.6.1pre2

* Thu Sep 15 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0-1
- Update to OpenAFS 1.6.0 final

* Mon Jul 25 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0-0.pre7
- Update to OpenAFS 1.6.0 pre-release 7

* Wed Jun 08 2011 Jack Neely <jjneely@ncsu.edu> 0:1.6.0-0.pre6
- Update to OpenAFS 1.6.0 pre-release 6

* Fri Jan 07 2011 Jack Neely <jjneely@ncsu.edu> 0:1.4.14-1
- Build OpenAFS 1.4.14
- Update kmodtool to the latest EL6 kmodtool from ELRepo
- Update spec to conform better to ELRepo's EL6 kmodspec

* Fri Nov 12 2010 Jack Neely <jjneely@ncsu.edu> 0:1.4.12.1-6
- Rebuild for RHEL 6 final

* Thu Aug 05 2010 Jack Neely <jjneely@ncsu.edu> 0:1.4.12.1-5
- Initial build of openafs-kmod using ELRepo's kABI templates

