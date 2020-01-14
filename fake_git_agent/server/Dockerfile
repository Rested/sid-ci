FROM jkarlos/git-server-docker:latest

COPY repos/ /git-server/repos

RUN cd /git-server/repos && \
    mv bar-svc/git bar-svc/.git && mv foo-app/git foo-app/.git && \
    git clone bar-svc --bare && git clone foo-app --bare && cd /git-server/