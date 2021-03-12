

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
cp -v ./dist/*fc32.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora32/SRPMS/
cp -v ./dist/*fc32.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora32/x86_64/
cp -v ./dist/*fc32.aarch64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora32/aarch64/
cp -v ./dist/*fc33.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora33/SRPMS/
cp -v ./dist/*fc33.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora33/x86_64/
cp -v ./dist/*fc33.aarch64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora33/aarch64/
cp -v ./dist/*fc34.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora34/SRPMS/
cp -v ./dist/*fc34.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora34/x86_64/
cp -v ./dist/*fc34.aarch64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora34/aarch64/
cp -v ./dist/*fc35.src.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora35/SRPMS/
cp -v ./dist/*fc35.x86_64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora35/x86_64/
cp -v ./dist/*fc35.aarch64.rpm /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora35/aarch64/

createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/rhel8/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/rhel8/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora32/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora32/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora33/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora33/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora34/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora34/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora35/SRPMS/
createrepo --update /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/fedora35/



if [ -x /usr/bin/fs ]; then
echo "quota end:"
fs lq /afs/eos.ncsu.edu/engrwww/linux.itecs/redhat/public/openafs/
fi

echo "All done."

