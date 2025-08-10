-- SQL schema for Supabase to replace SQLAlchemy models

create table "user" (
  id serial primary key,
  username text,
  email text,
  password text
);

create table batch (
  id serial primary key,
  batch_title text,
  color_tag text,
  start_date timestamp,
  end_date timestamp,
  description text,
  created_by integer references "user"(id)
);

create table tasks (
  id serial primary key,
  task_name text,
  task_description text,
  username text,
  status text,
  task_notes text,
  updated_at timestamp,
  created_by integer references "user"(id),
  batch_id integer references batch(id)
);
