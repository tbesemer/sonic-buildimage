#!/bin/bash

#  If the extensions are not in place, install.
#
if [ ! -f /usr/bin/git.bin ]
then
    sudo cp /usr/bin/git /usr/bin/git.bin
    sudo cp /usr/bin/git.logging /usr/bin/git
    if [ $? -ne 0 ]
    then
        echo "Failed to install git.logging"
        exit 1
    fi
fi

if [ ! -f /usr/bin/wget.bin ]
then
    sudo cp /usr/bin/wget /usr/bin/wget.bin
    sudo cp /usr/bin/wget.logging /usr/bin/wget
    if [ $? -ne 0 ]
    then
        echo "Failed to install wget.logging"
        exit 1
    fi
fi

sudo cp /etc/pip.conf.log_runtime /etc/pip.conf
if [ $? -ne 0 ]
then
    echo "Failed to install pip.conf"
    exit 1
fi

echo "Logging Enabled"
exit 0