ARG centos=7.7.1908
FROM aursu/rpmbuild:${centos}-build

USER root

RUN yum -y install \
        libc-client \
    && yum clean all && rm -rf /var/cache/yum /var/lib/rpm/__db*

COPY system/etc/yum.repos.d/bintray-custom.repo /etc/yum.repos.d/bintray-custom.repo

RUN yum -y --enablerepo=custom --enablerepo=bintray-custom --enablerepo=bintray-php71custom install \
        php-cli \
        php-common \
        php-devel \
        php-process \
        php-xml \
    && yum clean all && rm -rf /var/cache/yum /var/lib/rpm/__db*
