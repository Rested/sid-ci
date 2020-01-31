FROM jkarlos/git-server-docker:latest

COPY ./ ./
RUN ls

COPY fake_keys/id_rsa.pub /git-server/keys/id_rsa.pub
RUN cd /git-server/repos && \
    mv bar-svc/git bar-svc/.git && mv foo-app/git foo-app/.git && \
    git clone bar-svc --bare && git clone foo-app --bare && cd /git-server/
