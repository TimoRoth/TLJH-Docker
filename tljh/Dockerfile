FROM ubuntu:24.04

RUN \
    set -x && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y full-upgrade && \
    apt-get -y install ca-certificates curl apt-transport-https && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" > /etc/apt/sources.list.d/docker.list && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get -y update && \
    apt-get -y install --no-install-recommends docker-ce-cli python3 python3-pip python3-venv git sqlite3 && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

ENV TLJH_INSTALL_PREFIX=/opt/tljh PATH=/opt/tljh/hub/bin:$PATH

RUN \
    set -x && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install --no-install-recommends nodejs && \
    python3 -m venv /opt/tljh/hub && \
    /opt/tljh/hub/bin/pip install --upgrade --no-cache pip setuptools && \
    /opt/tljh/hub/bin/pip install \
        git+https://github.com/jupyterhub/the-littlest-jupyterhub.git \
        git+https://github.com/TimoRoth/tljh-repo2docker.git@oggm \
        jupyterhub-nativeauthenticator \
        jupyterhub-idle-culler \
        jupyterhub-traefik-proxy \
        pycurl && \
    mkdir -p /opt/tljh/config/templates/extra-assets && \
    ln -s ../../../../templates/extra-assets /opt/tljh/hub/share/jupyterhub/static/extra-assets && \
    apt-get -y remove --purge nodejs npm && \
    apt-get -y autoremove --purge && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

RUN /opt/tljh/hub/bin/python3 -m jupyterhub_traefik_proxy.install --output=/opt/tljh/hub/bin

ARG TLJH_UID=1009
ARG TLJH_GID=1009
ARG DOCKER_GID=2375
RUN \
    groupadd -g $DOCKER_GID docker && \
    groupadd -g $TLJH_GID tljh && \
    useradd -g tljh -d /opt/tljh/state -m -G users,docker -u $TLJH_UID tljh && \
    mkdir -p /opt/tljh/state/rules && \
    chown -R tljh:tljh /opt/tljh/state

USER tljh
WORKDIR /opt/tljh/state

COPY jupyterhub_config.py /opt/tljh/jupyterhub_config.py
COPY config.yaml /opt/tljh/config/config.yaml

VOLUME /opt/tljh/state
VOLUME /opt/tljh/config

EXPOSE 8000

CMD ["/opt/tljh/hub/bin/python3", "-m", "jupyterhub", "-f", "/opt/tljh/jupyterhub_config.py", "--upgrade-db", "--ip", "0.0.0.0", "--port", "8000"]
