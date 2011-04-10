#!/bin/bash

apt-get -y update
apt-get -y install git-core curl nginx ruby-full p7zip-full

userdel -f -r runner
userdel -f -r runners_boss
userdel -f -r maintainer

useradd -d /home/runner -m runner -p runner -s /bin/bash
useradd -d /home/runners_boss -m runners_boss -p runners_boss -s /bin/bash
useradd -d /home/maintainer -m maintainer -p \$6\$yMeG4jC9\$1iE1/9mCAqkSqFvus7cGFjGeRfiYdkQ0ME0X02fxMv48.5jZcj1mDjm30klZm4aTXI7cuaRs1t2a2bYjdfEUU. -r -G ssh,sudo -s /bin/bash


cp machine_scripts/bashrc /home/maintainer/.bashrc
cp machine_scripts/fastcgi-mono-server4.sh /home/maintainer
chown maintainer:maintainer /home/maintainer/fastcgi-mono-server4.sh

crontab -u maintainer machine_scripts/crontab

cp machine_scripts/sshd_config /etc/ssh/sshd_config
mkdir -p /home/maintainer/.ssh
mkdir -p /root/.ssh
cp machine_scripts/id_rsa.pub /home/maintainer/.ssh/authorized_keys
chmod 444 /home/maintainer/.ssh/authorized_keys
cp machine_scripts/root_id_rsa.pub /root/.ssh/authorized_keys
chmod 444 /root/.ssh/authorized_keys

/etc/init.d/ssh reload


