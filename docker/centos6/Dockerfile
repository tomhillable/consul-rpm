FROM centos:centos6
MAINTAINER Sebastien Le Digabel "sledigabel@gmail.com"

ENV CONSULVER 1.7.2
ENV TEMPLATEVER 0.25.0

RUN yum update -y
RUN yum install -y rpmdevtools mock

RUN cd /root && rpmdev-setuptree
ADD SOURCES/* /root/rpmbuild/SOURCES/
ADD SPECS/* /root/rpmbuild/SPECS/
RUN ln -s /root/rpmbuild/RPMS /RPMS

VOLUME ["/RPMS"]

CMD set -x && \
    cd /root && \
    spectool --define "_version ${CONSULVER}" -g -R rpmbuild/SPECS/consul.spec && \
    rpmbuild --define "_version ${CONSULVER}" -ba rpmbuild/SPECS/consul.spec && \
    spectool --define "_version ${TEMPLATEVER}" -g -R rpmbuild/SPECS/consul-template.spec && \
    rpmbuild --define "_version ${TEMPLATEVER}" -ba rpmbuild/SPECS/consul-template.spec
