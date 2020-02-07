CREATE SCHEMA IF NOT EXISTS sid_ci;

CREATE TABLE IF NOT EXISTS sid_ci.clients
(
    id                    int generated always as identity,
    identifier            text unique,
    password              text,
    created_at            timestamp,
    last_communication_at timestamp,
    last_status           text,
    active                boolean,
    is_admin              boolean,
    CONSTRAINT clients_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sid_ci.repos
(
    id       int generated always as identity,
    name     text    not null,
    ssh_url  text    not null unique,
    enabled  boolean not null,
    added_by int references sid_ci.clients (id),
    added_at timestamp,
    CONSTRAINT repos_pk PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS sid_ci.job
(
    job_uuid    text not null unique,
    status      boolean,
    image_url   text,
    git_hexsha  text,
    repo_url    text,
    received_at timestamp,
    CONSTRAINT jobs_pk PRIMARY KEY (job_uuid)
);

CREATE TABLE IF NOT EXISTS sid_ci.run_event
(
    id         int generated always as identity,
    event_type text,
    content    text,
    event_at   timestamp,
    run_by     int references sid_ci.clients (id),
    job_id     text references sid_ci.job (job_uuid),
    CONSTRAINT run_event_pk PRIMARY KEY (id)
);


