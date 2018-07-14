# Fedora spec file for php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
# API/ABI check

# Building of CGI SAPI is disabled by default. Use --with cgi to enable it
# tests are disabled by default. Use --with test to enable them

# by default all features are enabled
%global with_cli 0%{!?_without_cli:1}
%global with_xml 0%{!?_without_xml:1}
%global with_pgsql 0%{!?_without_pgsql:1}
%global with_opcache 0%{!?_without_opcache:1}
%global with_odbc 0%{!?_without_odbc:1}
%global with_ldap 0%{!?_without_ldap:1}
%global with_bcmath 0%{!?_without_bcmath:1}
%global with_posix 0%{!?_without_posix:1}
%global with_devel 0%{!?_without_devel:1}
%global with_common 0%{!?_without_common:1}

# we do not know for sure if any of shared module enabled
%global with_modules 0

# https://github.com/rpm-software-management/rpm/blob/master/doc/manual/conditionalbuilds
# php-cgi SAPI
%global with_cgi 0%{?_with_cgi:1}
%global with_fpm 0%{?_with_fpm:1}
%global with_test 0%{?_with_test:1}

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%global with_ap24 1
%else
%global with_ap24 0%{?_with_ap24:1}
# build could be tagged only on CentOS 6 where httpd-2.2 is default
%if %{with_ap24}
%global aptag .ap24
%endif # if %{with_ap24}
%endif # if 0%{?fedora} >= 18 || 0%{?rhel} >= 7

# we can not provide devel package without CLI (due to phpize)
%if %{with_devel}
%global with_cli 1
%endif

%global with_relocation 0%{?_with_relocation:1}

# with this flag set on we will build php with libmysqlclient library
%global with_libmysql 0%{?_with_libmysql:1}

%if %{with_libmysql}
%global mytag .my
%global with_cli 1
%global with_cgi 1
%endif

# _rundir is defined in RHEL/CentOS 7
%if 0%{?rhel} < 7
%global _rundir     /var/run
%endif

%if %{with_relocation}
%global program_suffix      7
%global main_name           php7
%global fpm_name            php7-fpm
%global php_sysconfdir      %{_sysconfdir}/php7
%global php_datadir         %{_datadir}/php7
%global pear_datadir        %{php_datadir}/pear
%global php_docdir          %{_docdir}/php7
%global tests_datadir       %{php_datadir}/tests
# configured by relocation patch (in other words - hardcoded)
%global fpm_config_name     php7-fpm.conf
%global fpm_config_d        %{php_sysconfdir}/php%{program_suffix}-fpm.d
%global bin_phar            phar%{program_suffix}
%global bin_cli             php%{program_suffix}
%global bin_cgi             php%{program_suffix}-cgi
%global bin_phpize          phpize%{program_suffix}
%global bin_phpdbg          phpdbg%{program_suffix}
%global bin_fpm             php%{program_suffix}-fpm
%global bin_php_config      php%{program_suffix}-config
%global fpm_datadir         %{_datadir}/php%{program_suffix}-fpm
%global php_includedir      %{_includedir}/php7
%else
%global main_name           php
%global fpm_name            php-fpm
%global php_sysconfdir      %{_sysconfdir}
%global php_datadir         %{_datadir}/php
%global pear_datadir        %{_datadir}/pear
%global php_docdir          %{_docdir}
%global tests_datadir       %{_datadir}/tests
%global fpm_config_name     php-fpm.conf
%global fpm_config_d        %{php_sysconfdir}/php-fpm.d
%global bin_phar            phar
%global bin_cli             php
%global bin_cgi             php-cgi
%global bin_phpize          phpize
%global bin_phpdbg          phpdbg
%global bin_fpm             php-fpm
%global bin_php_config      php-config
%global fpm_datadir         %{_datadir}/fpm
%global php_includedir      %{_includedir}/php
%endif

%global php_main            %{main_name}
%global php_common          %{php_main}-common
%global php_cli             %{php_main}-cli
%global php_cgi             %{php_main}-cgi
%global php_xml             %{php_main}-xml
%global php_opcache         %{php_main}-opcache
%global php_bcmath          %{php_main}-bcmath
%global php_mysql           %{php_main}-mysql
%global php_mysqlnd         %{php_main}-mysqlnd
%global php_libdir          %{_libdir}/%{main_name}
%global fpm_rundir          %{_rundir}/%{fpm_name}
%global php_sharedstatedir  %{_sharedstatedir}/%{main_name}
%global fpm_sharedstatedir  %{_sharedstatedir}/%{fpm_name}
%global fpm_logdir          %{_localstatedir}/log/%{fpm_name}
%global fpm_config          %{php_sysconfdir}/%{fpm_config_name}
%global fpm_service         %{fpm_name}
%global fpm_tmpfiles_d      %{fpm_service}.conf
%global fpm_service_d       %{fpm_service}.service.d
%global fpm_unit            %{fpm_service}.service
%global fpm_logrotate       %{fpm_service}

# API/ABI check
%global apiver      20160303
%global zendver     20160303
%global pdover      20150127
# Extension version
%global jsonver     1.5.0

# Adds -z now to the linker flags
%global _hardened_build 1

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%if 0%{?fedora}
%global mysql_config %{_bindir}/mysql_config
%else
%global mysql_config %{_libdir}/mysql/mysql_config
%endif

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

%if 0%{?fedora}
%global isasuffix -%{__isa_bits}
%else
%if 0%{?__isa:1}
%global isasuffix -%{__isa}
%else
%global isasuffix %nil
%endif
%endif

%global  _nginx_home    %{_localstatedir}/lib/nginx
# needed at srpm build time, when httpd-devel not yet installed
%{!?_httpd_mmn:         %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

%{!?_httpd_apxs: %global _httpd_apxs %{_sbindir}/apxs}
%{!?_httpd_contentdir: %global _httpd_contentdir /var/www}
%{!?_httpd_confdir: %global _httpd_confdir %{_sysconfdir}/httpd/conf.d}
%{!?_httpd_moddir: %global _httpd_moddir %{_libdir}/httpd/modules}

%global with_dtrace 1
%global with_zip    1

%if 0%{?fedora} || 0%{?rhel} >= 7
%global db_devel  libdb-devel
%else
%global db_devel  db4-devel
%endif

%if 0%{?fedora} >= 20 || 0%{?rhel} > 7
%global with_libzip 1
%else
%global with_libzip 0
%endif

%global rpmrel 3
%global baserel %{rpmrel}%{?dist}

Summary: PHP scripting language for creating dynamic web sites
Name: %{php_main}
Version: 7.1.19
Release: %{rpmrel}%{?mytag}%{?aptag}%{?dist}

# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
# ext/date/lib is MIT
License: PHP and Zend and BSD and MIT and ASL 1.0
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{version}.tar.xz
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source9: php.modconf
Source10: php-fpm.init
Source13: nginx-fpm.conf
Source14: nginx-php.conf
Source15: php-cgi-fcgi.ini
Source16: https://downloads.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz
# zend loader discontinued starting from PHP 7
# http://blog.zend.com/2016/10/10/zend-guard-and-php-7/

# Configuration files for some extensions
Source50: opcache.ini
Source51: opcache-default.blacklist

# relocation resources
Source101: php7-php.conf
Source103: php7-macros.php
Source104: php7-php-fpm.conf
Source105: php7-php-fpm-www.conf
Source106: php7-php-fpm.service
Source107: php7-php-fpm.logrotate
Source110: php7-php-fpm.init
Source113: php7-nginx-fpm.conf
Source114: php7-nginx-php.conf
Source150: php7-10-opcache.ini

# Build fixes
Patch1: php-7.1.7-httpd.patch
Patch5: php-7.0.0-includedir.patch
Patch8: php-7.0.2-libdb.patch

# Functional changes
Patch40: php-7.1.16-dlopen.patch
Patch42: php-7.1.0-systzdata-v14.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-7.1.15-ldap_r.patch
# Make php_config.h constant across builds
Patch46: php-7.1.14-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.6.3-phpinfo.patch
# Automatically load OpenSSL configuration file
Patch48: php-7.1.9-openssl-load-config.patch
Patch49: php-5.6.31-no-scan-dir-override.patch

# Upstream fixes (100+)

# Security fixes (200+)

# Fixes for tests (300+)
# Factory is droped from system tzdata
Patch300: php-5.6.3-datetests.patch

# relocation (400+)
Patch405: php7-php-7.0.0-includedir.patch
Patch409: php-7.0.8-relocation.patch

# No interactive mode for CLI/CGI - disable libedit
BuildRequires: autoconf
BuildRequires: bison
BuildRequires: bzip2-devel
BuildRequires: %{db_devel}
BuildRequires: flex
BuildRequires: freetype-devel
BuildRequires: gcc-c++
BuildRequires: gdbm-devel
%if %{with_ap24}
BuildRequires: httpd-devel >= 2.4
%else
BuildRequires: httpd-devel >= 2.2
BuildRequires: httpd-devel < 2.4
%endif
BuildRequires: libcurl-devel
BuildRequires: libc-client-devel
BuildRequires: libicu-devel
BuildRequires: libjpeg-devel
BuildRequires: libmcrypt-devel
BuildRequires: libpng-devel
BuildRequires: libstdc++-devel
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
BuildRequires: libwebp-devel
BuildRequires: libxml2-devel
%if %{with_libzip}
BuildRequires: libzip-devel >= 0.11
%endif
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: perl
BuildRequires: smtpdaemon
BuildRequires: sqlite-devel
BuildRequires: unixODBC-devel
BuildRequires: zlib-devel
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel
%endif
%if %{with_libmysql}
BuildRequires: mysql-devel
%endif
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}

Requires: httpd-mmn = %{_httpd_mmn}
%if %{with_ap24}
# to ensure we are using httpd with filesystem feature (see #1081453)
Requires: httpd-filesystem >= 2.4
%endif
Requires: libcurl

Requires(pre): httpd

# Don't provides extensions, which are not shared library, as .so
# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_libdir}/modules/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_libdir}/modules/.*\\.so$

# php engine for Apache httpd webserver
Provides: php(httpd)
Provides: mod_php = %{version}-%{release}

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# libmagic, onigurama are licensed under BSD
License: PHP and BSD
# ABI/API check - Arch specific
Provides: php(api) = %{apiver}%{isasuffix}
Provides: php(zend-abi) = %{zendver}%{isasuffix}
Provides: php(language) = %{version}, php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
# Bzip2 support in PHP is not enabled by default. You will need to use the --with-bz2
Provides: php-bz2, php-bz2%{?_isa}
# To get these functions to work, you have to compile PHP with --enable-calendar
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
# Beginning with PHP 4.2.0 these functions are enabled by default
Provides: php-ctype, php-ctype%{?_isa}
# To use PHP's cURL support you must also compile PHP --with-curl
Provides: php-curl, php-curl%{?_isa}
Provides: php_database
# part of the PHP core
Provides: php-date, php-date%{?_isa}
Provides: bundled(timelib)
# using the --enable-dba configuration option you can enable PHP for basic support of dbm-style databases
# To enable support for gdbm add --with-gdbm
# To enable support for Oracle Berkeley DB 4 or 5 add --with-db4
Provides: php-dba, php-dba%{?_isa}
# php-ereg DEPRECATED in PHP 5.3.0, and REMOVED in PHP 7.0.0 (no --with-regex flag anymore)
# To enable exif-support configure PHP with --enable-exif
Provides: php-exif, php-exif%{?_isa}
# This extension is enabled by default as of PHP 5.3.0
Provides: php-fileinfo, php-fileinfo%{?_isa}
Provides: bundled(libmagic) = 5.29
# the filter extension is enabled by default as of PHP 5.2.0
Provides: php-filter, php-filter%{?_isa}
# to use FTP functions with your PHP configuration, you should add the --enable-ftp
Provides: php-ftp, php-ftp%{?_isa}
# To enable GD-support configure PHP --with-gd
Provides: php-gd, php-gd%{?_isa}
Provides: bundled(gd) = 2.0.35
# To include GNU gettext support in your PHP build you must add the option --with-gettext
Provides: php-gettext, php-gettext%{?_isa}
# As of PHP 5.1.2, the Hash extension is bundled and compiled into PHP by default
Provides: php-hash, php-hash%{?_isa}
# This extension is enabled by default
Provides: php-iconv, php-iconv%{?_isa}
# To get these functions to work, you have to compile PHP with --with-imap
Provides: php-imap, php-imap%{?_isa}
# extension may be installed using the bundled version as of PHP 5.3.0, --enable-intl will enable the bundled version
Provides: php-intl, php-intl%{?_isa}
# As of PHP 5.2.0, the JSON extension is bundled and compiled into PHP by default
Provides: php-json, php-json%{?_isa}
%if %{with_relocation}
Provides: %{php_main}-json, %{php_main}-json%{?_isa}
%endif
Provides: bundled(libmbfl) = 1.3.2
# The libxml extension is enabled by default
Provides: php-libxml, php-libxml%{?_isa}
# mbstring is a non-default extension. --enable-mbstring : Enable mbstring functions
Provides: php-mbstring, php-mbstring%{?_isa}
# You need to compile PHP with the --with-mcrypt[=DIR] parameter to enable this extension
# mcrypt extension has been deprecated as of PHP 7.1.0 and moved to PECL as of PHP 7.2.0
Provides: php-mcrypt, php-mcrypt%{?_isa}
Provides: php-mysqli%{?_isa} = %{version}-%{baserel}
Provides: php-mysqli = %{version}-%{baserel}
# mysql extension was DEPRECATED in PHP 5.5.0, and it was removed in PHP 7.0.0 (comented out therefore)
# As of 5.4.0 The MySQL Native Driver is now the default for all MySQL extensions
%if ! %{with_libmysql}
Provides: php-mysqlnd = %{version}-%{baserel}
Provides: php-mysqlnd%{?_isa} = %{version}-%{baserel}
%endif
Provides: bundled(oniguruma) = 5.9.6
# To use PHP's OpenSSL support you must also compile PHP --with-openssl
Provides: php-openssl, php-openssl%{?_isa}
# core PHP extension, so it is always enabled
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-pdo = %{version}-%{baserel}
Provides: php-pdo%{?_isa} = %{version}-%{baserel}
Provides: php-pdo-abi  = %{pdover}
Provides: php(pdo-abi) = %{pdover}
Provides: php-pdo-abi  = %{pdover}%{isasuffix}
Provides: php(pdo-abi) = %{pdover}%{isasuffix}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
# PDO and the PDO_SQLITE driver is enabled by default as of PHP 5.1.0
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}
Provides: php-pecl-json          = %{jsonver}
Provides: php-pecl(json)         = %{jsonver}
Provides: php-pecl-json%{?_isa}  = %{jsonver}
Provides: php-pecl(json)%{?_isa} = %{jsonver}
# The Phar extension is built into PHP as of PHP version 5.3.0
Provides: php-phar, php-phar%{?_isa}
# they are part of the PHP core
Provides: php-reflection, php-reflection%{?_isa}
# Session support is enabled in PHP by default
Provides: php-session, php-session%{?_isa}
# enable SOAP support, configure PHP with --enable-soap
Provides: php-soap = %{version}-%{baserel}
Provides: php-soap%{?_isa} = %{version}-%{baserel}
# As of PHP 5.3.0 this extension can no longer be disabled and is therefore always available
Provides: php-spl, php-spl%{?_isa}
# The SQLite3 extension is enabled by default as of PHP 5.3.0
Provides: php-sqlite3, php-sqlite3%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
# these functions are enabled by default
Provides: php-tokenizer, php-tokenizer%{?_isa}
# XML-RPC support in PHP is not enabled by default. You will need to use the --with-xmlrpc
Provides: php-xmlrpc, php-xmlrpc%{?_isa}
%if %{with_zip}
# compile PHP with zip support by using the --enable-zip
Provides: php-zip, php-zip%{?_isa}
%endif
# Zlib support in PHP is not enabled by default. You will need to configure PHP --with-zlib
Provides: php-zlib, php-zlib%{?_isa}
%if %{with_ap24} || %{with_libmysql}
Provides: %{php_common}%{?_isa} = %{version}-%{baserel}
%endif

%description common
The %{php_common} package contains files used by both the php
package and the %{php_cli} package.

%if %{with_cli}
%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
%if %{with_ap24}
Provides: %{php_cli}%{?_isa} = %{version}-%{baserel}
%endif

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php.
%endif

%if %{with_cgi}
%package cgi
Group: Development/Languages
Summary: CGI interface for PHP
# for monolithic config use we need ensure that all extensions are installed
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}

%description cgi
The php-cgi package contains the CGI interface executing
PHP scripts, /usr/bin/php-cgi

%package ioncube
Summary: ionCube extension for PHP
Group: Development/Languages
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}

%description ioncube
ionCube Loader extensions for PHP. The ionCube
Loader is loaded as a PHP engine extension. This extension
transparently detects and loads encoded files.
%endif

%if %{with_fpm}
%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
BuildRequires: libacl-devel
BuildRequires: nginx-filesystem
%if 0%{?rhel} >= 7
BuildRequires: systemd-units
BuildRequires: systemd-devel
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
Requires(pre): /usr/sbin/useradd
# for /etc/nginx ownership
Requires(pre): nginx-filesystem
Requires: nginx-filesystem

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.
%endif

%if %{with_devel}
%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: %{php_cli}%{?_isa} = %{version}-%{baserel}
Requires: autoconf, automake
Requires: pcre-devel%{?_isa}

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.
%endif

%if %{with_opcache}
%package opcache
Summary:   The Zend OPcache
Group:     Development/Languages
License:   PHP
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
Provides:  php-pecl-zendopcache = %{version}
Provides:  php-pecl-zendopcache%{?_isa} = %{version}
Provides:  php-pecl(opcache) = %{version}
Provides:  php-pecl(opcache)%{?_isa} = %{version}
%global with_modules 1

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.
%endif

%if %{with_xml}
%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
# This extension is enabled by default
Provides: php-dom, php-dom%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
# This extension is enabled by default.
Provides: php-simplexml, php-simplexml%{?_isa}
# compile PHP with --enable-wddx
Provides: php-wddx, php-wddx%{?_isa}
# enabled by default as of PHP 5.1.2
Provides: php-xmlreader, php-xmlreader%{?_isa}
# This extension is enabled by default.
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
# PHP 5 includes the XSL extension by default and can be enabled by adding the argument --with-xsl
Provides: php-xsl, php-xsl%{?_isa}
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
Requires: libxslt
%global with_modules 1

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.
%endif

%if %{with_pgsql}
%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: postgresql-devel
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
Requires: postgresql-libs
%global with_modules 1

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.
%endif

%if %{with_odbc}
%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
BuildRequires: unixODBC-devel
%global with_modules 1

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.
%endif

%if %{with_bcmath}
%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
# only available if PHP was configured with --enable-bcmath
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
%global with_modules 1

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.
%endif

%if %{with_ldap}
%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
BuildRequires: cyrus-sasl-devel
BuildRequires: openldap-devel
%global with_modules 1

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.
%endif

%if %{with_posix}
%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{php_common}%{?_isa} = %{version}-%{baserel}
Provides: php-posix, php-posix%{?_isa}
Provides: php-shmop, php-shmop%{?_isa}
Provides: php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}
Provides: php-sysvmsg, php-sysvmsg%{?_isa}
%global with_modules 1

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.
%endif

%prep
%setup -q -n php-%{version}

%if %{with_cgi}
# ionCube Loader
%setup -q -n php-%{version} -T -D -a 16
%endif

%patch1 -p1

%if %{with_relocation}
%patch405 -p1
%else
%patch5 -p1
%endif # if %{with_relocation}

%patch8 -p1

%if %{with_relocation}
%patch409 -p1
%endif # if %{with_relocation}

%patch42 -p1
%patch43 -p1
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1
%endif
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1

# upstream patches

# security patches

# Fixes for tests
%patch300 -p1

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING
cp ext/date/lib/LICENSE.rst timelib_LICENSE

# Multiple builds for multiple SAPIs
mkdir build-apache
%if %{with_cgi}
mkdir build-cgi
%endif
%if %{with_fpm}
mkdir build-fpm
%endif

# ----- Manage known as failed test -------
# affected by systzdata patch
rm ext/date/tests/timezone_location_get.phpt
rm ext/date/tests/timezone_version_get.phpt
rm ext/date/tests/timezone_version_get_basic1.phpt
# fails sometime
rm -f ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt
rm Zend/tests/bug68412.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}.
   : Update the version macros and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the %{jsonver} macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# php-fpm configuration files for tmpfiles.d
%if %{with_fpm} && 0%{?rhel} >= 7
echo "d %{fpm_rundir} 755 root root" >php-fpm.tmpfiles
%endif

%if %{with_opcache}
# Some extensions have their own configuration file
%if %{with_relocation}
cat %{SOURCE150} > 10-opcache.ini
%else
cat %{SOURCE50} > 10-opcache.ini
%endif

# according to https://forum.remirepo.net/viewtopic.php?pid=8407#p8407
%if 0%{?rhel} >= 7
%ifarch x86_64
sed -e '/opcache.huge_code_pages/s/0/1/' -i 10-opcache.ini
%endif # ifarch x86_64
%endif # if 0%{?rhel} >= 7
%endif # if %{with_opcache}

%build
# Set build date from https://reproducible-builds.org/specs/source-date-epoch/
export SOURCE_DATE_EPOCH=$(date +%s -r NEWS)

# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4

# Force use of system libtool:
libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{php_libdir}/modules.
EXTENSION_DIR=%{php_libdir}/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{pear_datadir}; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend

# Always static:
# date, filter, libxml, reflection, spl: not supported
# hash: for PHAR_SIG_SHA256 and PHAR_SIG_SHA512
# session: dep on hash, used by soap and wddx
# pcre: used by filter, zip
# openssl: for PHAR_SIG_OPENSSL
# zlib: used by image

ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --disable-debug \
    --disable-phpdbg \
    --enable-calendar \
    --enable-dba --with-db4=%{_prefix} --with-gdbm \
    --enable-exif \
    --enable-ftp \
    --enable-gd-native-ttf \
    --enable-intl \
    --enable-mbstring \
    --enable-mbregex \
    --enable-pdo \
    --enable-soap \
%if %{with_zip}
    --enable-zip \
%if %{with_libzip}
    --with-libzip \
%endif
%endif
    --libdir=%{php_libdir} \
%if %{with_relocation}
    --sysconfdir=%{php_sysconfdir} \
%endif
    --with-bz2 \
    --with-config-file-path=%{php_sysconfdir} \
    --with-curl=%{_prefix} \
    --with-freetype-dir=%{_prefix} \
    --with-gd \
    --with-gettext \
    --with-icu-dir=%{_prefix} \
    --with-imap \
    --with-imap-ssl \
    --with-kerberos \
    --with-jpeg-dir=%{_prefix} \
    --with-layout=GNU \
    --with-libdir=%{_lib} \
    --with-mcrypt=%{_prefix} \
    --with-mysql-sock=%{mysql_sock} \
%if %{with_libmysql}
    --with-mysqli=%{mysql_config} \
    --with-pdo-mysql=%{_prefix} \
%else
    --with-mysqli=mysqlnd \
    --with-pdo-mysql=mysqlnd \
%endif
    --with-openssl \
    --without-pear \
    --with-pdo-odbc=unixODBC,%{_prefix} \
    --with-pic \
    --with-png-dir=%{_prefix} \
    --with-system-ciphers \
    --with-system-tzdata \
    --with-xmlrpc \
    --with-zlib \
%if %{with_dtrace}
    --enable-dtrace \
%endif
%if %{with_opcache}
    --enable-opcache \
%else
    --disable-opcache \
%endif
%if %{with_xml}
    --enable-dom=shared \
    --enable-simplexml=shared \
    --enable-wddx=shared \
    --enable-xmlreader=shared \
    --enable-xmlwriter=shared \
    --with-xsl=shared,%{_prefix} \
%endif
%if %{with_pgsql}
    --with-pdo-pgsql=shared,%{_prefix} \
    --with-pgsql=shared \
%endif
%if %{with_odbc}
    --with-unixODBC=shared,%{_prefix} \
%endif
%if %{with_bcmath}
    --enable-bcmath=shared \
%endif
%if %{with_ldap}
    --with-ldap=shared --with-ldap-sasl \
%endif
%if %{with_posix}
    --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
    --enable-shmop=shared \
    --enable-posix=shared \
%endif
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
%if %{with_cgi}
pushd build-cgi

build \
%if %{with_relocation}
      --program-suffix=%{program_suffix} \
%endif
      --disable-cli \
      --with-config-file-scan-dir=%{php_sysconfdir}/php-cgi-fcgi.d
popd
%endif

without_shared="--disable-bcmath --disable-dom --disable-opcache \
      --disable-posix --disable-shmop \
      --disable-simplexml \
      --disable-sysvmsg --disable-sysvsem --disable-sysvshm \
      --disable-wddx --disable-xmlreader --disable-xmlwriter --without-ldap \
      --without-pdo-pgsql --without-pgsql \
      --without-unixODBC --without-xsl"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} --disable-cgi \
%if %{with_relocation}
    --program-suffix=%{program_suffix} \
%endif
%if %{with_cgi}
    ${without_shared} \
%endif
%if ! %{with_cli}
    --disable-cli \
%endif
    --with-config-file-scan-dir=%{php_sysconfdir}/php.d
popd

# Build php-fpm
%if %{with_fpm}
pushd build-fpm
build --enable-fpm \
%if %{with_relocation}
      --program-suffix=%{program_suffix} \
%endif
      --with-fpm-acl \
%if 0%{?rhel} >= 7
      --with-fpm-systemd \
%endif
      --disable-cgi \
      --disable-cli \
      ${without_shared} \
      --with-config-file-scan-dir=%{php_sysconfdir}/php.d
popd
%endif

%check
%if %{with_test}
cd build-apache

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      cat "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
# Install everything from the CGI SAPI build
%if %{with_cgi}
make -C build-cgi install-cgi  \
%if %{with_modules}
    install-modules \
%endif
    INSTALL_ROOT=$RPM_BUILD_ROOT
%else
%if %{with_modules}
make -C build-apache install-modules INSTALL_ROOT=$RPM_BUILD_ROOT
%endif # if %{with_modules}
%endif # if %{with_cgi}

# all except install-sapi - use apxs for rpmbuild is failed (httpd.conf is missed)
make -C build-apache  install-binaries \
%if %{with_devel}
    install-build install-headers install-pdo-headers \
%endif
%if %{with_cli}
    install-pharcmd \
%endif
%if %{with_devel} || %{with_cli}
    install-programs \
%endif
    INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
%if %{with_fpm}
make -C build-fpm install-fpm \
    INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the default configuration file and icons
%if %{with_common}
install -m 755 -d $RPM_BUILD_ROOT%{php_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{php_sysconfdir}/php.ini
%endif # if %{with_common}

install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 *.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php.gif

%if %{with_common}
# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{php_libdir}/pear \
                  $RPM_BUILD_ROOT%{php_datadir}
%endif

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}

# Apache config fragment
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_confdir}
# Due to posibility of use apache 2.2 and 2.4 we copy it locally
%if %{with_relocation}
cat %{SOURCE101} > httpd-php.conf
%else
cat %{SOURCE1} > httpd-php.conf
%endif
install -D -m 644 httpd-php.conf $RPM_BUILD_ROOT%{_httpd_confdir}/02-php.conf

# Dual config file with httpd >= 2.4 (fedora >= 18)
%if %{with_ap24}
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%else
cat %{SOURCE9} httpd-php.conf > $RPM_BUILD_ROOT%{_httpd_confdir}/02-php.conf
%endif

%if %{with_common}
install -m 755 -d $RPM_BUILD_ROOT%{php_sysconfdir}/php.d
install -m 755 -d $RPM_BUILD_ROOT%{php_sharedstatedir}
install -m 755 -d $RPM_BUILD_ROOT%{php_sharedstatedir}/peclxml
install -m 700 -d $RPM_BUILD_ROOT%{php_sharedstatedir}/session
install -m 700 -d $RPM_BUILD_ROOT%{php_sharedstatedir}/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{php_sharedstatedir}/opcache
install -m 755 -d $RPM_BUILD_ROOT%{php_docdir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{tests_datadir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{php_sysconfdir}/php-cgi-fcgi.d
%endif

%if %{with_cgi}
# install ioncube
install -D -m 755 ioncube/ioncube_loader_lin_7.1.so $RPM_BUILD_ROOT%{php_libdir}/modules/ioncube_loader_lin_7.1.so

# install config
sed "s,@LIBDIR@,%{_libdir},g" \
    < %{SOURCE15} > php-cgi-fcgi.ini
install -D -m 644 php-cgi-fcgi.ini \
           $RPM_BUILD_ROOT%{php_sysconfdir}/php-cgi-fcgi.ini
%endif

# PHP-FPM stuff
# Log
%if %{with_fpm}
install -m 700 -d $RPM_BUILD_ROOT%{fpm_sharedstatedir}/session
install -m 700 -d $RPM_BUILD_ROOT%{fpm_sharedstatedir}/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{fpm_sharedstatedir}/opcache
install -m 755 -d $RPM_BUILD_ROOT%{fpm_logdir}
install -m 755 -d $RPM_BUILD_ROOT%{fpm_rundir}
# Config
install -m 755 -d $RPM_BUILD_ROOT%{fpm_config_d}
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%if %{with_relocation}
install -m 644 %{SOURCE104} $RPM_BUILD_ROOT%{fpm_config}
install -m 644 %{SOURCE105} $RPM_BUILD_ROOT%{fpm_config_d}/www.conf
install -m 644 %{SOURCE107} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{fpm_logrotate}
# Nginx configuration
install -D -m 644 %{SOURCE113} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/%{fpm_name}.conf
install -D -m 644 %{SOURCE114} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/%{main_name}.conf
%else
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{fpm_config}
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{fpm_config_d}/www.conf
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{fpm_logrotate}
# Nginx configuration
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/%{fpm_name}.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/%{main_name}.conf
%endif  # if %{with_relocation}

mv $RPM_BUILD_ROOT%{fpm_config}.default .
mv $RPM_BUILD_ROOT%{fpm_config_d}/www.conf.default .

%if 0%{?rhel} >= 7
# tmpfiles.d
install -m 755 -d $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 php-fpm.tmpfiles $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/%{fpm_tmpfiles_d}
# install systemd unit files and scripts for handling server startup
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/%{fpm_service_d}
install -m 755 -d $RPM_BUILD_ROOT%{_unitdir}
%if %{with_relocation}
install -m 644 %{SOURCE106} $RPM_BUILD_ROOT%{_unitdir}/%{fpm_unit}
%else
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/%{fpm_unit}
%endif  # if %{with_relocation}
%else
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/init.d
%if %{with_relocation}
install -m 755 %{SOURCE110} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{fpm_service}
%else
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{fpm_service}
%endif  # with_relocation
%endif  # rhel >= 7
%endif  # with_fpm

%if %{with_modules}
# Generate files lists and stub .ini files for each subpackage
for mod in \
%if %{with_bcmath}
    bcmath \
%endif
%if %{with_xml}
    dom simplexml wddx xmlreader xmlwriter xsl \
%endif
%if %{with_opcache}
    opcache \
%endif
%if %{with_pgsql}
    pgsql pdo_pgsql \
%endif
%if %{with_odbc}
    odbc \
%endif
%if %{with_ldap}
    ldap \
%endif
%if %{with_posix}
    posix shmop sysvshm sysvsem sysvmsg \
%endif
    ; do
    case $mod in
      opcache)
        # Zend extensions
        ini=10-${mod}.ini;;
      xsl|dom|wddx|xmlreader|xmlwriter|simplexml)
        # Extensions with dependencies on 20-*
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        ini=20-${mod}.ini;;
    esac
    # some extensions have their own config file
    if [ -f ${ini} ]; then
      install -D -m 644 ${ini} $RPM_BUILD_ROOT%{php_sysconfdir}/php.d/${ini}
    else
      install -d -m 755 $RPM_BUILD_ROOT%{php_sysconfdir}/php.d
      cat > $RPM_BUILD_ROOT%{php_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    fi
%if %{with_cgi}
    install -d -m 755 $RPM_BUILD_ROOT%{php_sysconfdir}/php-cgi-fcgi.d
    cp -p $RPM_BUILD_ROOT%{php_sysconfdir}/{php.d,php-cgi-fcgi.d}/${ini}
    cat > files.${mod} <<EOF
%{php_libdir}/modules/${mod}.so
%config(noreplace) %{php_sysconfdir}/php.d/${ini}
%config(noreplace) %{php_sysconfdir}/php-cgi-fcgi.d/${ini}
EOF
%else
    cat > files.${mod} <<EOF
%{php_libdir}/modules/${mod}.so
%config(noreplace) %{php_sysconfdir}/php.d/${ini}
EOF
%endif # if %{with_cgi}
done
%endif # if %{with_modules}

%if %{with_xml}
# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx \
    files.simplexml >> files.xml
%endif

%if %{with_posix}
# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process
%endif

%if %{with_pgsql}
# postgres support as separate php-pgsql package
cat files.pdo_pgsql >> files.pgsql
%endif

%if %{with_opcache}
# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{php_sysconfdir}/php.d/opcache-default.blacklist
%endif

%if %{with_devel}
%if %{with_relocation}
cat %{SOURCE103} > macros.php
%else
cat %{SOURCE3} > macros.php
%endif

# Install the macros file:
sed -i -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
    -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
    -e "s/@PHP_VERSION@/%{version}/" macros.php
%if 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.%{php_main}
%else
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -m 644 -c macros.php \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.%{php_main}
%endif # if 0%{?rhel} >= 7
%endif # if %{with_devel}

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{php_libdir}/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{pear_datadir} \
       $RPM_BUILD_ROOT%{_libdir}/libphp7.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%if %{with_fpm}
%pre fpm
getent group nginx >/dev/null || \
  groupadd -r nginx
getent passwd nginx >/dev/null || \
    useradd -r -d %{_nginx_home} -g nginx \
    -s /sbin/nologin -c "Nginx web server" nginx
exit 0

%post fpm
%if 0%{?rhel} >= 7
%systemd_post %{fpm_unit}
%else
if [ $1 = 1 ]; then
    # Initial installation
    /sbin/chkconfig --add %{fpm_service} 2>/dev/null
fi
%endif

%preun fpm
%if 0%{?rhel} >= 7
%systemd_preun %{fpm_unit}
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /usr/sbin/service %{fpm_service} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{fpm_service} 2>/dev/null
fi
%endif

%postun fpm
%if 0%{?rhel} >= 7
%systemd_postun_with_restart %{fpm_unit}
%else
if [ $1 -ge 1 ]; then
    /usr/sbin/service %{fpm_service} condrestart >/dev/null 2>&1 || :
fi
%endif
%endif # if %{with_fpm}

%files
%{_httpd_moddir}/libphp7.so
%config(noreplace) %{_httpd_confdir}/02-php.conf
%if %{with_ap24}
%config(noreplace) %{_httpd_modconfdir}/15-php.conf
%endif
%{_httpd_contentdir}/icons/*.gif

%if %{with_common}
%files common
%doc CODING_STANDARDS CREDITS EXTENSIONS NEWS README*
%doc LICENSE TSRM_LICENSE libmagic_LICENSE phar_LICENSE timelib_LICENSE
%doc php.ini-*
%config(noreplace) %{php_sysconfdir}/php.ini
%dir %{php_sysconfdir}/php.d
%dir %{php_sysconfdir}/php-cgi-fcgi.d
%dir %{php_libdir}
%dir %{php_libdir}/modules
%dir %{php_sharedstatedir}
%dir %{php_sharedstatedir}/peclxml
%dir %{php_datadir}
%dir %{php_docdir}/pecl
%dir %{tests_datadir}
%dir %{tests_datadir}/pecl
%attr(0770,root,apache) %dir %{php_sharedstatedir}/session
%attr(0770,root,apache) %dir %{php_sharedstatedir}/wsdlcache
%attr(0770,root,apache) %dir %{php_sharedstatedir}/opcache
%endif

%if %{with_cli}
%files cli
%{_bindir}/%{bin_cli}
%{_bindir}/phar.%{bin_phar}
%{_bindir}/%{bin_phar}
# provides phpize here (not in -devel) for pecl command
%{_bindir}/%{bin_phpize}
%{_mandir}/man1/%{bin_cli}.1*
%{_mandir}/man1/%{bin_phar}.1*
%{_mandir}/man1/phar.%{bin_phar}.1*
%{_mandir}/man1/%{bin_phpize}.1*
%doc sapi/cli/README
# move php-config here in case if devel package disabled
%if ! %{with_devel}
%exclude %{_bindir}/%{bin_php_config}
%exclude %{_mandir}/man1/%{bin_php_config}.1*
%endif # if ! %{with_devel}
%endif # if %{with_cli}

%if %{with_cgi}
%files cgi
%{_bindir}/%{bin_cgi}
%config(noreplace) %{php_sysconfdir}/php-cgi-fcgi.ini
%{_mandir}/man1/%{bin_cgi}.1*
%doc sapi/cgi/README*

%files ioncube
%attr(755,root,root) %{php_libdir}/modules/ioncube_loader_lin_7.1.so
%endif

%if %{with_fpm}
%files fpm
%doc %{fpm_config_name}.default www.conf.default
%doc fpm_LICENSE
%{_sbindir}/%{bin_fpm}
%attr(0770,root,nginx) %dir %{fpm_sharedstatedir}/session
%attr(0770,root,nginx) %dir %{fpm_sharedstatedir}/wsdlcache
%attr(0770,root,nginx) %dir %{fpm_sharedstatedir}/opcache
%config(noreplace) %{_sysconfdir}/nginx/conf.d/%{fpm_name}.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/%{main_name}.conf
%config(noreplace) %{fpm_config}
%config(noreplace) %{fpm_config_d}/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{fpm_logrotate}
%if 0%{?rhel} >= 7
%dir %{_sysconfdir}/systemd/system/%{fpm_service_d}
%{_prefix}/lib/tmpfiles.d/%{fpm_tmpfiles_d}
%{_unitdir}/%{fpm_unit}
%else
%{_sysconfdir}/init.d/%{fpm_service}
%endif
%dir %{fpm_config_d}
# log owned by apache for log
%attr(770,nginx,root) %dir %{fpm_logdir}
%dir %{fpm_rundir}
%{_mandir}/man8/%{bin_fpm}.8*
%dir %{fpm_datadir}
%{fpm_datadir}/status.html
%endif

%if %{with_devel}
%files devel
%{_bindir}/%{bin_php_config}
%{php_includedir}
%{php_libdir}/build
%{_mandir}/man1/%{bin_php_config}.1*
%if 0%{?rhel} >= 7
%{_rpmconfigdir}/macros.d/macros.%{php_main}
%else
%{_sysconfdir}/rpm/macros.%{php_main}
%endif
%endif # if %{with_devel}

%if %{with_xml}
%files xml -f files.xml
%doc libmbfl_LICENSE
%doc oniguruma_COPYING
%doc ucgendat_LICENSE
%endif

%if %{with_bcmath}
%files bcmath -f files.bcmath
%doc libbcmath_COPYING
%endif

%if %{with_opcache}
%files opcache -f files.opcache
%config(noreplace) %{php_sysconfdir}/php.d/opcache-default.blacklist
%endif

%if %{with_posix}
%files process -f files.process
%endif

%if %{with_pgsql}
%files pgsql -f files.pgsql
%endif

%if %{with_odbc}
%files odbc -f files.odbc
%endif

%if %{with_ldap}
%files ldap -f files.ldap
%endif

%changelog
* Sat Jul 14 2018 Alexander Ursu <alexander.ursu@gmail.com> 7.1.19-3
- added --with-kerberos option for CentOS 6 build as well
- added httpd macros (not defined in CentOS 6)

* Thu Jul 05 2018 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.19-2
- Fixed bug with unresolved php-common dependency for libmysql
  build

* Thu Jun 21 2018 Remi Collet <remi@remirepo.net> - 7.1.19-1
- Update to 7.1.19 - http://www.php.net/releases/7_1_19.php

* Thu May 24 2018 Remi Collet <remi@remirepo.net> - 7.1.18-1
- Update to 7.1.18 - http://www.php.net/releases/7_1_18.php

* Wed Apr 25 2018 Remi Collet <remi@remirepo.net> - 7.1.17-1
- Update to 7.1.17 - http://www.php.net/releases/7_1_17.php

* Wed Feb 28 2018 Remi Collet <remi@remirepo.net> - 7.1.15-1
- Update to 7.1.15 - http://www.php.net/releases/7_1_15.php

* Fri Feb 16 2018 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.14-2
- Added support for libmysqlclient

* Wed Jan 31 2018 Remi Collet <remi@remirepo.net> - 7.1.14-1
- Update to 7.1.14 - http://www.php.net/releases/7_1_14.php
- define SOURCE_DATE_EPOCH for reproducible build

* Thu Dec  7 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.12-2
- added patch for PHP_INI_SCAN_DIR

* Wed Nov 22 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.12-1
- upgrade to 7.1.12
- added process subpackage

* Mon Oct 02 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.10-2
- added fix for EL6 for opcache.huge_code_pages

* Mon Oct 02 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.10-1
- Update to 7.1.10 - http://www.php.net/releases/7_1_10.php

* Wed Sep 27 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.9-3
- disabled sockets extension
- added CGI scan directory

* Thu Sep 21 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.9-2
- disabe PHP functions logging output to browser
- added release tags .ap24

* Wed Sep 13 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.9-1
- Automatically load OpenSSL configuration file, from PHP 7.2
- Update to 7.1.9 - http://www.php.net/releases/7_1_9.php
- php-fpm: drop unneeded "pid" from default configuration
- disable httpd MPM check
- enable PHP execution of .phar files, see #1117140

* Tue Sep 12 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.6-4
- moved xmlrpc into php-common
- removed pgsql extension from CGI config

* Wed Jun 28 2017 Alexander Ursu <alexander.ursu@gmail.com> - 7.1.6-2
- made relocation feature optional (disabled by default)
- made fpm sapi optional (disabled by default)

* Wed Jun  7 2017 Remi Collet <remi@fedoraproject.org> - 7.1.6-1
- Update to 7.1.6 - http://www.php.net/releases/7_1_6.php
- add upstream security patches for oniguruma

* Tue Apr 11 2017 Remi Collet <remi@fedoraproject.org> - 7.1.4-1
- Update to 7.1.4 - http://www.php.net/releases/7_1_4.php

* Wed Mar 15 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-2
- remove %%attr, see #1432372

* Fri Nov 24 2016 Remi Collet <remi@fedoraproject.org> 7.0.13-2
- disable pcre.jit everywhere as it raise AVC #1398474

* Wed Nov  9 2016 Remi Collet <remi@fedoraproject.org> 7.0.13-1
- Update to 7.0.13 - http://www.php.net/releases/7_0_13.php
- update tzdata patch to v14, improve check for valid tz file

* Fri Jul 22 2016 Alexander Ursu <alexander.ursu@gmail.com> - 7.0.9-1
- Update to 7.0.9 - http://www.php.net/releases/7_0_9.php
- wddx: add upstream patch for https://bugs.php.net/72564

* Thu Jul 21 2016 Alexander Ursu <alexander.ursu@gmail.com> - 7.0.8-1
- initial build
