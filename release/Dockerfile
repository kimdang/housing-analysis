from python:3.7 as builder

WORKDIR /root

RUN pip3 install \
    pymysql \
    mysqlclient==1.4.6 \
    Django \
    pandas \
    matplotlib \
    seaborn \
    numpy \
    scipy \
    scikit-learn

COPY . /root

#ENTRYPOINT ["python3", "manage.py", "runserver"]
#CMD ["0.0.0.0:8000"]
RUN wget https://releases.hashicorp.com/consul-template/0.25.1/consul-template_0.25.1_linux_amd64.tgz && \
    tar xvf consul-template_0.25.1_linux_amd64.tgz  && \
    chmod +x consul-template && \
    mv consul-template /usr/bin/


ENTRYPOINT ["./bin/controller.sh"]
