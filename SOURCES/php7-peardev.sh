#!/bin/sh
exec /usr/bin/php7 -C -q \
    -d memory_limit="-1" \
    -d include_path=/usr/share/php7/pear \
    -d date.timezone=UTC \
    -d output_buffering=1 \
    -d variables_order=EGPCS \
    -d safe_mode=0 \
    -d register_argc_argv="On" \
    -d open_basedir="" \
    -d auto_prepend_file="" \
    -d auto_append_file=""  \
    /usr/share/php7/pear/pearcmd.php "$@"
