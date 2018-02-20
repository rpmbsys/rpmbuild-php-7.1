#!/bin/sh
exec /usr/bin/php7 -C \
    -d include_path=/usr/share/php7/pear \
    -d date.timezone=UTC \
    -d output_buffering=1 \
    -d variables_order=EGPCS \
    -d safe_mode=0 \
    -d register_argc_argv="On" \
    /usr/share/php7/pear/peclcmd.php "$@"
