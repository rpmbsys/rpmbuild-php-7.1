FROM aursu/centos:7-curl

COPY system/etc/yum.repos.d/bintray-custom.repo /etc/yum.repos.d/bintray-custom.repo

USER root
RUN yum -y --enablerepo=bintray-custom --enablerepo=bintray-php71custom install \
        php-bcmath \
        php-cli \
        php-fpm \
        php-opcache \
        php-pecl-apcu \
        php-pecl-geoip \
        php-pecl-imagick \
        php-pecl-memcached \
        php-pecl-redis4 \
        php-xml \
    && yum clean all && rm -rf /var/cache/yum
