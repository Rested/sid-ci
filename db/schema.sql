CREATE SCHEMA IF NOT EXISTS sid_ci;

CREATE TABLE IF NOT EXISTS sid_ci.clients (
    id int generated always as identity,
    identifier text,
    token text,
    created_at timestamp,
    last_communication_at timestamp,
    active boolean,
    CONSTRAINT clients_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sid_ci.repos (
    id int generated always as identity,
    name text not null,
    ssh_url text not null,
    enabled boolean not null,
    added_by int references sid_ci.clients(id),
    added_at timestamp,
    CONSTRAINT repos_pk PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS sid_ci.results (
    suceeded boolean,
    run_log text,
    image_digest text,
    git_hexsha text,
    run_by int references sid_ci.clients(id),
    repo int references sid_ci.repos(id),
    received_at timestamp
);


