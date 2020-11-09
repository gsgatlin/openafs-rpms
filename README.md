# openafs-rpms

These are some openafs rpms which have been used at NC State University.

Originally the client/server packages came from rpmfusion. But the maintainer 
could not work on them any longer. The openafs-dkms and openafs-kmod packages 
came from the elrepo.org maintaner who also worked at NC State University at 
the time.


# Instructions

CentOS 8:

as root install various packages and groups before you start

```
dnf install epel-release
dnf groupinstall "Development Tools"
dnf groupinstall "RPM Development Tools"
dnf groupinstall "Fedora Packager"
```

Fedora:

```
dnf install @development-tools
dnf install @rpm-development-tools
dnf -y install fedora-packager rpm-sign createrepo_c
```

CentOS 7/6:

WARNING

You will not be able to build for el8/fedora on el7 or el6 due
to lack of "dnf" command on these distros.

```
yum install epel-release
yum groupinstall "Development Tools"
yum groupinstall "Fedora Packager"
```

All distros:

make sure you run

```
usermod -a -G mock YOURACCOUNTNAME
```

once before you start.

cd into the directory name of the rpm package name you wish to build for.

For this repository the choices are: openafs or openafs-dkms

Next type 

```
make
```

to build for all distros (EL6 EL7 EL8 and various fedora)

WARNING

"make" or "make all" may take a long time due to the large number of distros 
supported combined with the complexity of the openafs compile process.

type

```
make %dist
```

to build for a specific distro. Like:

```
make el8
```

for centos 8 / RHEL 8 for example.

```
make el6 el7 el8
```

would build binary and source rpms for CentOS 6/7/8 RHEL 6/7/8 in one command.

In the fedora distro, the %dist is called fcXX. Like Fedora 34 would have a 
%dist of fc34. "fc" once stood for "fedora core" and I think they just never 
changed it.

Binary / source rpms and logs will be found in the "dist" subdirectory.

The openafs-kmod package has been removed since it was not used and was 
technically obsolete with fedora going in a different direction with
pre packaged kernel modules such as akmods. We just chose to use dkms
since it was working well on other distros like ubuntu and arch linux.
Also the dkms based package already existed in a primitive form. (Mandriva 
package)

The Makefile needs to updated every time a new RHEL / CentOS is released or 
is dropped from support. The Makefile must also be edited whenever a new 
fedora release branches off of "rawhide." This usually happens a couple of 
months before a new fedora release. At most you will have 4 fedoras going at
one time right after a new release before the oldest version of fedora is
retired. We use numbers in the Makefile now that mock provides a symlink to
"fedora-rawhide" within the mock package.

There are some other targets in the makefile that are not included in 
target "all"

```
fcXXaarch64
el8aarch64
```

These need to be built on a aarch64 architecture machine! Either a real ARM 
server or within qemu emulator on x86_64. I have been using qemu since I do 
not have access to real ARM hardware that is powerful enough to build openafs. 
an example of arm complile:

```
make el8aarch64
```

We only support openafs i686 builds for CentOS 6. If you have trouble building
the openafs kernel module (libafs) on fedora or RHEL after a new kernel drops, 
check the arch linux openafs source packages in the AUR for useful patches to 
add to keep everything building all the time. Checking "rawhide" builds can 
catch this early.

