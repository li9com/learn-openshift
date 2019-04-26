FROM        python:3
LABEL       maintainer.name="Dmitrii Mostovshchikov" \
            maintainer.email="Dmitrii.Mostovshchikov@li9.com" \
            maintainer.company="Li9, Inc." \
            company.website="https://www.li9.com" \
            s2i.app="flask" \
            io.openshift.s2i.scripts-url="image:///usr/libexec/s2i"
ENV         LISTEN_PORT 9000
WORKDIR     /app

ADD         ./s2i/bin /usr/libexec/s2i
ADD         ./app .
RUN         pip install --no-cache-dir -r requirements.txt

EXPOSE      ${LISTEN_PORT}/tcp

CMD         [ "/usr/libexec/s2i/usage" ]

