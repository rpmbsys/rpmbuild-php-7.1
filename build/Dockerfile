ARG centos=7

FROM aursu/rpmbuild:${centos}-build

USER root
RUN yum -y install --enablerepo custom \
        php-cli \
        php-common \
        php-devel \
        php-process \
        php-xml \
    && yum clean all && rm -rf /var/cache/yum
