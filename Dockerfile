ARG BUILD_FROM
FROM ${BUILD_FROM}
ARG RPM_VERSION
ENV RPM_VERSION=${RPM_VERSION}

ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN echo "${BUILD_FROM} is the key"
RUN if command -v apt-get >/dev/null 2>&1; then \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            ca-certificates \
            curl \
            python3 \
            python3-pip \
            python3-venv \
            rsync \
            python3-dev \
            build-essential \
            libffi-dev \
            libssl-dev \
        && rm -rf /var/lib/apt/lists/*; \
    elif command -v apk >/dev/null 2>&1; then \
        apk add --no-cache \
            ca-certificates \
            curl \
            python3 \
            py3-pip \
            py3-virtualenv \
            rsync \
            python3-dev \
            build-base \
            libffi-dev \
            openssl-dev; \
    else \
        echo "No supported package manager found (apt-get or apk)." >&2; \
        exit 1; \
    fi

RUN test -n "$RPM_VERSION" \
    && mkdir -p /opt/remote-project-manager \
    && curl -fL "https://codeload.github.com/drachul/remote-project-manager/tar.gz/${RPM_VERSION}" \
        -o /tmp/remote-project-manager.tar.gz \
    && tar -xzf /tmp/remote-project-manager.tar.gz -C /opt/remote-project-manager --strip-components=1 \
    && rm /tmp/remote-project-manager.tar.gz

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r /opt/remote-project-manager/requirements.txt \
    && cp -R /opt/remote-project-manager/app /app/app \
    && rm -rf /opt/remote-project-manager
COPY addon_entrypoint.py ./addon_entrypoint.py

EXPOSE 8000

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

CMD ["/opt/venv/bin/python", "-u", "/app/addon_entrypoint.py"]
