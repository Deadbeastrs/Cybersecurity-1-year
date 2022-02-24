FROM ubuntu:focal

# Create workspace dir
ARG WS_DIR=/ws

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Portugal

# Install required/useful packages
RUN apt update && apt upgrade -y && apt install \
    sudo \
    wireless-tools \
    iproute2 \
    pciutils \
    apache2 \
    tmux \
    mysql-server \
    php \
    libapache2-mod-php \
    php-mysql \
    python3 \
    wget \
    cron \
    openssh-server \
    rsync \
    vim -y

RUN /bin/bash -c "mkdir /home/jovemguilhas"

COPY source_code /ws/source_code
COPY configs/personalProgram /home/jovemguilhas/personalProgram
COPY configs/to_do.txt /home/jovemguilhas/to_do.txt
COPY configs/create_db.sql /ws/create_db.sql
COPY configs/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY configs/apache2.conf /etc/apache2/apache2.conf
COPY configs/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
COPY configs/ports.conf /etc/apache2/ports.conf
COPY configs/secure_mysql.sql /ws/secure_mysql.sql
COPY configs/config.sh /ws/config.sh
COPY configs/autostart.sh /autostart.sh
COPY configs/auto_backup.sh /home/jovemguilhas/auto_backup.sh

RUN /bin/bash -c "chmod +x /ws/config.sh && cd .. && chmod +x autostart.sh"

RUN /bin/bash -c "cd ws && ./config.sh"

ENTRYPOINT ["./autostart.sh"]

CMD ["./autostart.sh"]
EXPOSE 3000
