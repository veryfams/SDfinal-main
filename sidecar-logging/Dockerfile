FROM fluent/fluentd:v1.16-1

USER root

RUN apk add --no-cache --update --virtual .build-deps \
        sudo build-base ruby-dev \
 && sudo gem install fluent-plugin-record-modifier \
 && sudo gem sources --clear-all \
 && apk del .build-deps \
 && rm -rf /var/cache/apk/* \
           /home/fluent/.gem/ruby/*/cache/*.gem

COPY fluentd.conf /fluentd/etc/fluent.conf

RUN mkdir -p /shared/logs/consolidated \
    && mkdir -p /var/log/fluentd \
    && chown -R fluent:fluent /shared/logs \
    && chown -R fluent:fluent /var/log/fluentd

USER fluent
