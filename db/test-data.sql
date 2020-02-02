insert into sid_ci.clients(identifier, active, is_admin) values ('admin', true, true);
insert into sid_ci.repos (name, ssh_url, enabled, added_by)
    values ('foo-app', 'ssh://git@git-server:22/git-server/repos/foo-app.git', true, 1);
insert into sid_ci.repos (name, ssh_url, enabled, added_by)
    values ('bar-svc', 'ssh://git@git-server:22/git-server/repos/bar-svc.git', true, 1);

