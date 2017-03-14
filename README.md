# openafs-rpms

These are some openafs rpms which are used at NC State University.

Originally the client/server packages came from rpmfusion. But the maintainer 
could not work on them any longer. The openafs-dkms packages came from the
elrepo.org maintaner who also worked at NC. State University at the time.


# Instructions

make sure you run

usermod -a -G mock YOURACCOUNTNAME

before you start.

cd into the directory name of the rpm package name you wish to build for.

type 

make

to build for all distros (EL6 EL7 and fedora)

type

make %dist

to build for a specific distro. Like:

make el7


