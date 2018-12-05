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

#update
RUN apt update --fix-missing

# python
RUN apt install -y python2.7 python-pip
RUN pip install pycryptodome

# chall user
RUN adduser --home /home/chall --disabled-password --gecos "" chall

# Dirs
WORKDIR /home/chall
COPY ./chall /home/chall

EXPOSE 4445

ENTRYPOINT [ "/usr/bin/python2.7" ]
CMD ["server.py"]
