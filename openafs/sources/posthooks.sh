#!/bin/bash

# openafs-posthooks.sh
#
# Copyright 2012  NC State University
# Written by Jack Neely <jjneely@ncsu.edu>
#
# SDG
#
# This script runs as a ExecStartPost from the openafs-client.service
# systemd unit.  It will source files in /etc/openafs/posthooks.d
# where an admin may place scripts to fine tune the OpenAFS client
# operations, such as turning on encryption.  The sysnames.sh script
# in that directory comes with this package.

HOOKS=/etc/openafs/posthooks.d

if [ -d $HOOKS ] ; then
    for i in $HOOKS/*.sh ; do
        if [ -r "$i" ]; then
            . $i
        fi
    done
    unset i
fi

