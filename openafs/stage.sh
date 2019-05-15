

#!/bin/bash

echo "sign, cp, and createrepo the openafs server packages built via mock..."

if [ ! -d /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/ ]; then
echo "Please start openafs (sshfs?) and then try again..."
exit 1
fi

rpm --addsign ./dist/*rpm


if [ -x /usr/bin/fs ]; then
echo "quota begin:"
fs lq /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/
fi

cp -v ./dist/*el8.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel8/SRPMS/
cp -v ./dist/*el8.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel8/x86_64/
cp -v ./dist/*el7.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel7/SRPMS/
cp -v ./dist/*el7.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel7/x86_64/
cp -v ./dist/*el7.i686.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel7/i686/

createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel8/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel8/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel7/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs-server/rhel7/


if [ -x /usr/bin/fs ]; then
echo "quota end:"
fs lq /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/
fi

echo "All done."

