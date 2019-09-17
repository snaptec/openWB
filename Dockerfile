FROM debian

# packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y \
    apache2 \
    php php-gd php-xml \
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
ENV APACHE_DOCUMENT_ROOT /var/www/html/openWB
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf /etc/apache2/sites-enabled/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# sources
COPY . ${APACHE_DOCUMENT_ROOT}
RUN ln -s ${APACHE_DOCUMENT_ROOT} /openWB

# install
RUN touch /var/log/openWB.log

# dockerize atreboot.sh
RUN mkdir -p ${APACHE_DOCUMENT_ROOT}/ramdisk
RUN sed -ri -e 's!sudo !!g' ${APACHE_DOCUMENT_ROOT}/runs/atreboot.sh
RUN sed -ri -e 's!ifconfig .*!true!g' ${APACHE_DOCUMENT_ROOT}/runs/atreboot.sh
RUN sed -ri -e 's!service .*!true!g' ${APACHE_DOCUMENT_ROOT}/runs/atreboot.sh
RUN sed -ri -e 's!/pi!/root!g' ${APACHE_DOCUMENT_ROOT}/runs/atreboot.sh
RUN sed -ri -e 's!-u pi!-u root!g' ${APACHE_DOCUMENT_ROOT}/runs/atreboot.sh

# http and mosquitto
EXPOSE 80
EXPOSE 1883

WORKDIR ${APACHE_DOCUMENT_ROOT}
COPY supervisord.conf /etc/supervisord.conf
CMD ["/usr/bin/supervisord"]
