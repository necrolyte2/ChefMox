#!/bin/bash

mkdir $1/etc/chef
knife configure client $1/etc/chef/

chroot $1 sudo apt-get update
chroot $1 sudo apt-get install --force-yes -y ruby ruby-dev libopenssl-ruby rdoc ri irb build-essential wget ssl-cert lsb-release 

chroot $1 wget http://production.cf.rubygems.org/rubygems/rubygems-1.7.2.tgz -O /tmp/rubygems-1.7.2.tgz
chroot $1 tar zxf /tmp/rubygems-1.7.2.tgz -C /tmp
chroot $1 sudo ruby /tmp/rubygems-1.7.2/setup.rb --no-format-executable

chroot $1 sudo gem install chef --no-ri --no-rdoc
