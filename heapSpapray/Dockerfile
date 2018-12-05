FROM debian:stretch-20180831

# hardening
RUN chmod o-x /usr/bin/wall
RUN chmod o-rx /var/log /run/*
RUN sed -i 's/664/660/g' /var/lib/dpkg/info/base-files.postinst
RUN chmod 773 /tmp

# date
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN adduser --disabled-password --force-badname --gecos '' heapspapray

RUN apt-get update && apt-get install -y xinetd

WORKDIR /home/heapSpapray
ADD ./heapSpapray /home/heapSpapray/
ADD ./file.xinetd /etc/xinetd.d/shortest
ADD ./flag.txt /home/heapSpapray/
RUN chmod 773 /tmp

EXPOSE 8890

CMD service xinetd restart && sleep infinity
