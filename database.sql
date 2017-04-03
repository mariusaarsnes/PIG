CREATE TABLE users (
    id              serial primary key,
    firstname       varchar(100),
    lastname        varchar(100),
    email           varchar(100),
    password        varchar(100)
);
CREATE TABLE groups (
    id              serial primary key,
    division_id     integer references division on delete set null,
    leader_id       integer references users on delete set null,
    number          integer
);

-- To fix circular deps:
--  alter table groups add foreign key (leader_id) references users on delete set null;

CREATE TABLE division (
    id              serial primary key,
    name            varchar(50),
    creator_id      integer references users
);


CREATE TABLE division_parameter (
    division_id     integer references division on delete cascade,
    parameter_id    integer references parameter on delete cascade,
    priority        integer,
    primary key (division_id, parameter_id)
);
CREATE TABLE value (
    id              serial primary key,
    value           integer,
    description     varchar(300)
);
CREATE TABLE parameter (
    id              serial primary key,
    description     varchar(300)
);
CREATE TABLE number_param (
    min             integer,
    max             integer,
    parameter_id    integer primary key references parameter on delete cascade
);
CREATE TABLE enum_variant (
    name            varchar(50),
    parameter_id    integer references parameter on delete cascade,
    primary key ( name, parameter_id )
);
CREATE TABLE parameter_value (
    parameter_id    integer references parameter on delete cascade,
    value_id        integer references value on delete cascade,
    primary key ( parameter_id, value_id )
);
CREATE TABLE user_division (
    user_id         integer references users on delete cascade,
    division_id     integer references division on delete cascade,
    role            varchar(300),
    primary key ( user_id, division_id )
);
CREATE TABLE user_division_parameter_value (
    user_id         integer references users on delete cascade,
    division_id     integer references division on delete cascade,
    parameter_id    integer references parameter on delete cascade,
    value_id        integer references value on delete cascade,
    primary key (user_id, division_id, parameter_id, value_id)
);
CREATE TABLE user_group (
    user_id         integer references users on delete cascade,
    group_id        integer references groups on delete cascade
);
