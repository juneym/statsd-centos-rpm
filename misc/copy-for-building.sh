#!/bin/sh

if [ ! -d spec ]; then 
  cd ..
fi
if [ ! -d spec ]; then
  echo "Please run this script in the project's working directory"
  exit 1
fi

/bin/cp spec/statsd.spec ~/rpmbuild/SPECS
/bin/cp sources/statsd ~/rpmbuild/SOURCES/statsd-init.d
/bin/cp sources/config.js ~/rpmbuild/SOURCES/config.js
/bin/cp sources/config.js ~/rpmbuild/SOURCES/exampleConfig.js
/bin/cp sources/exampleProxyConfig.js ~/rpmbuild/SOURCES/exampleProxyConfig.js
