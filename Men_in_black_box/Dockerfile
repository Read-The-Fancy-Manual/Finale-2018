# Author: noraj
# Author website: https://rawsec.ml

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

RUN apt update && apt install -y ruby2.3 ruby2.3-dev sqlite3 libsqlite3-dev cmake openssl libssl-dev g++
# install dependencies
RUN gem install sinatra thin sqlite3

# drop privileges
RUN groupadd -g 1337 appuser && \
    useradd -r -u 1337 -g appuser appuser
USER appuser

COPY ./webserver.rb /usr/src/app/webserver.rb
COPY ./database.db /usr/src/app/database.db
COPY ./public /usr/src/app/public
COPY ./views /usr/src/app/views

WORKDIR /usr/src/app

EXPOSE 4567

CMD ruby ./webserver.rb
