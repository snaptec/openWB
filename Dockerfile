FROM debian

# PHP 7.0 repo
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q https://packages.sury.org/php/apt.gpg -O- | apt-key add -
RUN echo "deb https://packages.sury.org/php/ stretch main" | tee /etc/apt/sources.list.d/php.list

# packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y \
    apache2 \
    php7.0 php7.0-gd php7.0-xml \
    python-pip python3-pip \
    cron \
    curl \
    jq \
    mosquitto-clients \
    nano \
    socat \
    supervisor

# fix invoke-rc.d: policy-rc.d denied execution of start
RUN printf "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d
RUN apt-get install -y mosquitto

RUN pip install evdev
RUN pip3 install paho-mqtt
RUN pip install -U pymodbus

# DOCUMENT_ROOT
ENV APACHE_DOCUMENT_ROOT /var/www/html
ENV OWB ${APACHE_DOCUMENT_ROOT}/openWB
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf /etc/apache2/sites-enabled/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# sources
COPY . ${OWB}

# install
RUN touch /var/log/openWB.log

# dockerize atreboot.sh
RUN mkdir -p ${OWB}/ramdisk
RUN sed -ri -e 's!sudo !!g' ${OWB}/runs/atreboot.sh
RUN sed -ri -e 's!ifconfig .*!true!g' ${OWB}/runs/atreboot.sh
RUN sed -ri -e 's!service .*!true!g' ${OWB}/runs/atreboot.sh
RUN sed -ri -e 's!/pi!/root!g' ${OWB}/runs/atreboot.sh
RUN sed -ri -e 's!-u pi!-u root!g' ${OWB}/runs/atreboot.sh

RUN (crontab -l ; echo "* * * * * ${OWB}/regel.sh >> /var/log/openWB.log 2>&1") | crontab -
RUN (crontab -l ; echo "* * * * * sleep 10 && ${OWB}/regel.sh >> /var/log/openWB.log 2>&1") | crontab -
RUN (crontab -l ; echo "* * * * * sleep 20 && ${OWB}/regel.sh >> /var/log/openWB.log 2>&1") | crontab -
RUN (crontab -l ; echo "* * * * * sleep 30 && ${OWB}/regel.sh >> /var/log/openWB.log 2>&1") | crontab -
RUN (crontab -l ; echo "* * * * * sleep 40 && ${OWB}/regel.sh >> /var/log/openWB.log 2>&1") | crontab -
RUN (crontab -l ; echo "* * * * * sleep 50 && ${OWB}/regel.sh >> /var/log/openWB.log 2>&1") | crontab -

# http and mosquitto
EXPOSE 80
EXPOSE 1883

WORKDIR ${OWB}
COPY supervisord.conf /etc/supervisord.conf
CMD ["/usr/bin/supervisord"]
