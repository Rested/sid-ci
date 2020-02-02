FROM alpine/git:1.0.7

COPY be-a-dev.sh ./
COPY server/repos ./repos
COPY server/fake_keys/id_rsa /root/.ssh/id_rsa
RUN chmod 400 /root/.ssh/id_rsa
RUN apk update && apk add openssh

ENTRYPOINT [ "/bin/sh", "-c" ]
CMD [ "./be-a-dev.sh" ]