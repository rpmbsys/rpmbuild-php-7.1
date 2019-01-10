FROM aursu/centos:7-curl

COPY system/etc/yum.repos.d/bintray-custom.repo /etc/yum.repos.d/bintray-custom.repo

# install common build tools (autotools, compilers, parsers etc)
RUN yum -y --enablerepo bintray-custom install \
        php-fpm \
    && yum clean all && rm -rf /var/cache/yum
