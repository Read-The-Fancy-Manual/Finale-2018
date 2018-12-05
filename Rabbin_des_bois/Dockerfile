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

RUN apt update
RUN apt install -y python2.7 python-pip
RUN apt install -y g++ gcc make libffi-dev libssl-dev

RUN apt install -y socat
RUN adduser --gecos '' --disabled-password dock;

ADD requirements.txt /home/dock/requirements.txt
RUN pip install -r /home/dock/requirements.txt
RUN rm /home/dock/requirements.txt
ADD chall.py /home/dock/rabbin
RUN chmod 505 /home/dock/rabbin
COPY flag.py /home/dock/flag.py
RUN chmod 444 /home/dock/flag.py

USER dock

EXPOSE 8888

ENTRYPOINT ["socat", "TCP-LISTEN:8888,fork","EXEC:python /home/dock/rabbin"]
