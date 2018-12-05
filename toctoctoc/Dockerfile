FROM debian:stretch-20180831
MAINTAINER The lsd
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update --fix-missing
RUN apt install -y socat python3 locales cron

RUN chmod o-x /usr/bin/wall
RUN chmod o-rx /var/log /run/*
RUN sed -i 's/664/660/g' /var/lib/dpkg/info/base-files.postinst
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN chmod 773 /tmp

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="en_US.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

# Clean the /tmp folder every 5 minutes
RUN (crontab -l 2>/dev/null; echo "*/5 * * * * /bin/rm -rf /tmp/*") | crontab -

RUN adduser --disabled-password --gecos '' chall

COPY flag.txt main.py flag.py /home/chall/
USER chall
ENV LC_ALL en_US.utf-8

WORKDIR /home/chall
EXPOSE 30000

ENTRYPOINT [ "socat" ]
CMD [ "TCP-LISTEN:30000,fork", "SYSTEM:\"python3 /home/chall/main.py\"" ]
