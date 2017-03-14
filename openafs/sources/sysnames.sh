#!/bin/bash

# /usr/libexec/openafs/sysnames
# Set custom sysnames after starting the afsd service.
# Runs as "ExecStartPost" in openafs-client.service.

# Figure out what we are
_ARCH=`uname -i | sed 's/x86_64/amd64/'`
_KERN=`uname -r | sed 's/\([0-9]\+\)\.\([0-9]\+\)\..*/\1\2/'`
_DIST=""

for d in fedora centos redhat ; do
    if [ -f "/etc/$d-release" ] ; then
        _DIST=$d
        break
    fi
done

# What version of the distribution are we?  Cut off the Client|Server
# mess from RHEL
_REL=`/bin/rpm -qf --qf '%{version}\n' /etc/${_DIST}-release | sed 's/\([0-9]\+\)[a-zA-Z]\+/\1/'`

# Sysname list.  The order here is from specific to general, with a
# fallback to the compiled-in value from /usr/bin/sys.  This will be
# used as the sysname search path.
SYSNAMELIST="${_ARCH}_${_DIST}_${_REL} ${_ARCH}_linux${_KERN} $(/usr/bin/sys)"

# Set the sysname
if [ -n "$SYSNAMELIST" ] ; then
    _FLAG=0
    _CMD=""
    for SYSNAME in $SYSNAMELIST ; do
        if [ $_FLAG == "1" ] ; then
            _CMD="$_CMD -newsys $SYSNAME"
        else
            _FLAG=1
            _CMD="/usr/bin/fs sysname $SYSNAME"
        fi
    done
fi
$_CMD > /dev/null
