# Author: noraj
# Author website: https://rawsec.ml

FROM debian:stretch-20180831
ARG DEBIAN_FRONTEND=noninteractive

# hardening
RUN chmod o-x /usr/bin/wall
RUN chmod o-rx /var/log /run/*
RUN sed -i 's/664/660/g' /var/lib/dpkg/info/base-files.postinst
#RUN chmod 773 /tmp

# date
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt update && apt install -y ruby2.3
# install dependencies
RUN gem install cinch pwned

# drop privileges
RUN groupadd -g 1337 appuser && \
    useradd -r -u 1337 -g appuser appuser
USER appuser

ENV ENV_IP $ENV_IP

COPY ./irc_cinch.rb /usr/src/app/irc_cinch.rb
COPY ./10k_most_common.txt /usr/src/app/10k_most_common.txt
COPY ./flag.txt /usr/src/app/flag.txt

WORKDIR /usr/src/app

CMD ruby ./irc_cinch.rb ${ENV_IP}
