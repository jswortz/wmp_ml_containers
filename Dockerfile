FROM ubuntu:16.04
MAINTAINER Jeremy Wortz <jwortz@wmp.com>

ENV TERM=xterm
ENV LANG en_US.UTF-8
RUN apt-get update -y && apt-get install build-essential -y
RUN apt-get update

ADD apt-packages.txt /tmp/apt-packages.txt
RUN xargs -a /tmp/apt-packages.txt apt-get install -y
ENV LC_ALL=C
RUN pip install virtualenv
RUN /usr/local/bin/virtualenv /opt/ds --distribute --python=/usr/bin/python3

ADD /requirements/ /tmp/requirements
RUN /opt/ds/bin/pip install --upgrade pip
RUN /opt/ds/bin/pip install -r /tmp/requirements/pre-requirements.txt
RUN /opt/ds/bin/pip install -r /tmp/requirements/requirements.txt

RUN useradd --create-home --home-dir /home/ds --shell /bin/bash ds
RUN chown -R ds /opt/ds
RUN adduser ds sudo

ADD run_airflow.sh /home/ds
RUN chmod +x /home/ds/run_airflow.sh
RUN chown ds /home/ds/run_airflow.sh

ADD .bashrc.template /home/ds/.bashrc

EXPOSE 8888
RUN usermod -a -G sudo ds
RUN echo "ds ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER ds
RUN mkdir -p /home/ds/notebooks
ENV HOME=/home/ds
ENV SHELL=/bin/bash
ENV USER=ds
VOLUME /home/ds/notebooks
WORKDIR /home/ds/notebooks
RUN mkdir /home/ds/trained_models


RUN /opt/ds/bin/pip install tornado --upgrade
ADD ANSWERS_airflow_101_iris_group_activity.py /home/ds
RUN /opt/ds/bin/python /home/ds/ANSWERS_airflow_101_iris_group_activity.py; exit 0
CMD ["/opt/ds/bin/python", "/home/ds/ANSWERS_airflow_101_iris_group_activity.py"]
