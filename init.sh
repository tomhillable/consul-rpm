#!/bin/bash

rpmdir=$1
job_name=$2
workspace=$3
build_number=$4
build_target=$5

test -d SRPMS && rm -rf SRPMS
test -f SOURCES/*.zip && rm -f SOURCES/*.zip

files=$(spectool -l -S SPECS/consul.spec | grep -E '^Source[0-9]*: http(s)?://'  | sed 's/Source[0-9]*: //' | while read line; do echo -n "${line} "; done)
/var/lib/jenkins/tools/rpm/fetch_rpms.sh SOURCES $files
sed -i "s/^Release:\(.*\)%{?dist}/Release:\1.${build_number}%{?dist}/" SPECS/consul.spec
output=$(rpmbuild --define '_topdir %(pwd)' -bs SPECS/consul.spec 2>&1)

if [ $? -gt 0 ]; then
  echo "Failed to build SRPM: ${output}"
  exit 1
fi

srpm=$(echo $output | grep 'Wrote:' | cut -d: -f 2)

/var/lib/jenkins/tools/rpm/build_with_mock.sh $build_target $srpm

find $WORKSPACE/rpms-${build_target}/ -type f \( -iname "*.rpm" ! -iname "*.src.rpm" \) -exec mv {} $rpmdir \;
ret=$?
git checkout SPECS/consul.spec

exit $ret

