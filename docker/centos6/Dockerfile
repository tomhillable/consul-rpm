FROM centos:centos6
MAINTAINER Sebastien Le Digabel "sledigabel@gmail.com"

ENV RPMVER 1.7.2

RUN yum update -y
RUN yum install -y rpmdevtools mock

RUN cd /root && rpmdev-setuptree
ADD SOURCES/* /root/rpmbuild/SOURCES/
ADD SPECS/* /root/rpmbuild/SPECS/
RUN ln -s /root/rpmbuild/RPMS /RPMS

VOLUME ["/RPMS"]

CMD set -x && cd /root && spectool --define "_version ${RPMVER}" -g -R rpmbuild/SPECS/consul.spec && rpmbuild --define "_version ${RPMVER}" -ba rpmbuild/SPECS/consul.spec
