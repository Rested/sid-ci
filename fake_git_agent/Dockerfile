FROM alpine/git:1.0.7

RUN apk update && apk add openssh

COPY --chown=root:root be-a-dev.sh ./
COPY server/repos ./repos
COPY server/fake_keys/id_rsa /root/.ssh/id_rsa
RUN chmod 400 /root/.ssh/id_rsa
RUN chmod +x be-a-dev.sh

ENTRYPOINT [ "/bin/sh", "-c" ]
CMD [ "./be-a-dev.sh" ]ls