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

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN adduser --disabled-password --gecos "" chall

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt
USER chall
EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
