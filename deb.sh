#!/bin/sh

ARCH=`dpkg --print-architecture`

install -d build/sha2wordlist/usr/bin build/sha2wordlist/DEBIAN
install -m 555 sha2wordlist build/sha2wordlist/usr/bin

sed -e "s/_ARCH_/${ARCH}/" <sha2wordlist.control >build/sha2wordlist/DEBIAN/control

dpkg-deb --build build/sha2wordlist

mv build/sha2wordlist.deb .
