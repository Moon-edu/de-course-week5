FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        freetds-bin \
        krb5-user \
        ldap-utils \
        libffi7 \
        libsasl2-2 \
        libsasl2-modules \
        libssl1.1 \
        locales  \
        lsb-release \
        sasl2-bin \
        sqlite3 \
        unixodbc \
        curl \
        python3-dev \
        libpq-dev \
        libffi-dev \
        build-essential

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN curl -k https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py

ADD install-airflow.sh /install-airflow.sh
RUN /install-airflow.sh
ADD airflow.cfg2 /root/airflow/airflow.cfg

ADD entrypoint.sh /entrypoint.sh

RUN python -m pip install virtualenv

ENTRYPOINT /entrypoint.sh