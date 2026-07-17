create extension if not exist on vector;

create table if not exist documents(
    id SERIAL primary key,
    filename TEXT not null,
    chunk TEXT not null,
    embedding VECTOR(1024),
    created_at TIMESTAP default CURRENT_TIMESTAP
);