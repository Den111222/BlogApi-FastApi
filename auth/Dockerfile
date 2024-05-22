FROM python:3.11

ARG WD=/opt/auth
ARG GROUP=auth
ARG USER=fastapi

WORKDIR $WD

ENV PYTHONPATH 'src/'

RUN groupadd -r $GROUP \
    && useradd -d $WD -r -g $GROUP $USER \
    && chown $USER:$GROUP -R $WD \
    && chown $USER:$GROUP /var/log

COPY --chown=$USER:$GROUP requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

RUN apt-get update \
    && apt-get -y install gettext \
    && apt-get -y install netcat-traditional

COPY --chown=$USER:$GROUP ./src /opt/auth/src
COPY --chown=$USER:$GROUP entrypoint.sh /opt/auth/entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/opt/auth/entrypoint.sh", "auth_pg", "5432"]