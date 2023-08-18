FROM octodns/octodns:2022.09

WORKDIR /opt/octodns
COPY requirements.txt requirements.txt

RUN set -ex \
  && pip install --no-cache-dir -r requirements.txt

ENV PATH=/opt/octodns/env/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
CMD [ "/bin/sh" ]
