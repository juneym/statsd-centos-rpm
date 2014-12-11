statsd-centos-rpm
=================

CentOS/Redhat files that can help you build a statsd RPM using the latest StatsD release (v0.7.2)


Instructions:
```
sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm
sudo yum install rpm-build rpmdevtools
rpmdev-setuptree
./misc/copy-for-building.sh
wget https://github.com/etsy/statsd/archive/v0.7.2.tar.gz -O ~/rpmbuild/SOURCES/statsd-0.7.2.tar.gz
rpmbuild --clean -ba ~/rpmbuild/SPECS/statsd.spec # Add "--with systemd" for CentOS7
sudo yum install --nogpgcheck ~/rpmbuild/RPMS/noarch/statsd-0.7.2-1.noarch.rpm
>>>>>>> Stashed changes
```
