

#!/bin/bash

echo "sign, cp, and createrepo the openafs packages built via mock..."

if [ ! -d /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/ ]; then
echo "Please start openafs (sshfs?) and then try again..."
exit 1
fi

if [ -x $HOME/bin/switchkeys ]; then
switchkeys eos
fi

rpm --addsign ./dist/*rpm


if [ -x /usr/bin/fs ]; then
echo "quota begin:"
fs lq /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/
fi

cp -v ./dist/*el8.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/rhel8/SRPMS/
cp -v ./dist/*el8.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/rhel8/x86_64/
cp -v ./dist/*el8.aarch64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/rhel8/aarch64/
cp -v ./dist/*fc29.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora29/SRPMS/
cp -v ./dist/*fc29.i686.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora29/i686/
cp -v ./dist/*fc29.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora29/x86_64/
cp -v ./dist/*fc29.aarch64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora29/aarch64/
cp -v ./dist/*fc30.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora30/SRPMS/
cp -v ./dist/*fc30.i686.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora30/i686/
cp -v ./dist/*fc30.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora30/x86_64/
cp -v ./dist/*fc30.aarch64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora30/aarch64/
cp -v ./dist/*fc31.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora31/SRPMS/
cp -v ./dist/*fc31.i686.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora31/i686/
cp -v ./dist/*fc31.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora31/x86_64/
cp -v ./dist/*fc31.aarch64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora31/aarch64/

createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/rhel8/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/rhel8/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora29/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora29/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora30/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora30/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora31/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora31/


if [ -x /usr/bin/fs ]; then
echo "quota end:"
fs lq /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/
fi

echo "All done."

