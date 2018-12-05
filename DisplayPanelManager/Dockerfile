FROM debian:stretch-20180716

#hardening
RUN chmod o-x /usr/bin/wall
RUN chmod o-rx /var/log /run/*
RUN sed -i 's/664/660/g' /var/lib/dpkg/info/base-files.postinst
RUN chmod 773 /tmp

#date
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update
RUN apt install -y xinetd
RUN adduser --disabled-password --force-badname --gecos '' chall

COPY chall /home/chall/
COPY service.conf /home/chall/
COPY flag.txt /home/chall/

WORKDIR /home/chall/
EXPOSE 2323

CMD ["/usr/sbin/xinetd", "-dontfork", "-f", "/home/chall/service.conf"]
