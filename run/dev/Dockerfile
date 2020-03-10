ARG centos=7.7.1908
ARG image=devbase
FROM aursu/php7build:${centos}-${image}

RUN curl -sSL https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
