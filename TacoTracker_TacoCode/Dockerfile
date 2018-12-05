FROM debian:stretch-20180831
ARG DEBIAN_FRONTEND=noninteractive

# hardening
RUN chmod o-x /usr/bin/wall
RUN chmod o-rx /var/log /run/*
RUN sed -i 's/664/660/g' /var/lib/dpkg/info/base-files.postinst
RUN chmod 773 /tmp

# date
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN chmod 773 /tmp && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt update && \
    apt install nginx supervisor php7.0-sqlite php7.0-fpm=7.0.30* -y && \
    mkdir /var/run/php && \
    sed -i -e"s/worker_processes  1/worker_processes 5/" /etc/nginx/nginx.conf && \
    sed -i -e"s/keepalive_timeout\s*65/keepalive_timeout 2/" /etc/nginx/nginx.conf && \
    sed -i -e"s/keepalive_timeout 2/keepalive_timeout 2;\n\tclient_max_body_size 100m/" /etc/nginx/nginx.conf && \
    echo "daemon off;" >> /etc/nginx/nginx.conf && \
    sed -i -e "s/;daemonize\s*=\s*yes/daemonize = no/g" /etc/php/7.0/fpm/php-fpm.conf && \
    sed -i -e "s/;catch_workers_output\s*=\s*yes/catch_workers_output = yes/g" /etc/php/7.0/fpm/pool.d/www.conf && \
    sed -i -e "s/pm.max_requests = 500/pm.max_requests = 10/g" /etc/php/7.0/fpm/pool.d/www.conf && \
    sed -i -e "s/;security.limit_extensions =.*/security.limit_extensions = .php .encoded/g" /etc/php/7.0/fpm/pool.d/www.conf && \
    echo "extension=/var/www/tacoder.so;" >> /etc/php/7.0/fpm/php.ini && \
    chown -R www-data:www-data /var/www/ && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    rm -Rf /etc/nginx/conf.d/* && \
    rm -Rf /etc/nginx/sites-enabled/default && \
    rm -Rf /etc/nginx/sites-available/default

ADD ./default /etc/nginx/sites-available/default
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

COPY www /var/www
ADD  ./supervisord.conf /etc/supervisord.conf
ADD  ./start.sh /start.sh
RUN chmod 755 /start.sh

CMD ["/bin/bash", "/start.sh"]
