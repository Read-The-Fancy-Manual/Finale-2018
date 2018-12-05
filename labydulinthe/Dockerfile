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

RUN apt update && apt install -y python3 python3-dev xinetd python3-pip procps

RUN adduser --disabled-password --gecos "" chall

WORKDIR /home/chall
EXPOSE 10000

COPY ./requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "/home/chall/labydulinthe_server.py"]
# CMD ["/usr/sbin/xinetd", "-dontfork", "-filelog", "/home/chall/log.log","-f", "/home/chall/service.conf"]
