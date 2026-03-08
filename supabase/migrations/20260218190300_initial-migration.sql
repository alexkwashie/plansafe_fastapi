-- PlanSafe360 Database Schema
-- This migration is idempotent and can be run against a fresh database.
-- Run order matters: enums → users → independent tables → dependent tables → junction tables → triggers

-- ============================================================
-- 1. ENUM TYPES
-- ============================================================

DO $$ BEGIN
  CREATE TYPE public.task_status AS ENUM ('pending', 'in_progress', 'completed', 'paused', 'skipped');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE public.machine_status AS ENUM ('available', 'in_use', 'maintenance', 'out_of_service');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE public.incident_severity AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ============================================================
-- 2. USERS (must be first — referenced by all other tables)
-- ============================================================

CREATE TABLE IF NOT EXISTS public.users (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  uid uuid NOT NULL DEFAULT gen_random_uuid(),
  username text,
  email text,
  "firstName" text,
  "lastName" text,
  CONSTRAINT users_pkey PRIMARY KEY (uid)
);

-- Auto-create a public.users row when a new auth.users row is inserted
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.users (uid, email, username, "firstName", "lastName")
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
    NEW.raw_user_meta_data->>'firstname',
    NEW.raw_user_meta_data->>'lastname'
  )
  ON CONFLICT (uid) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================================
-- 3. INDEPENDENT TABLES (reference only users)
-- ============================================================

CREATE TABLE IF NOT EXISTS public.batch_table (
  batch_id uuid NOT NULL DEFAULT gen_random_uuid(),
  batch_title text NOT NULL,
  batch_description text,
  batch_status text,
  start_date date,
  start_time time without time zone,
  end_date date,
  end_time time without time zone,
  location text,
  color text,
  created_at timestamp with time zone,
  created_by uuid,
  updated_at timestamp with time zone,
  updated_by uuid,
  estimated_duration integer,
  process_duration integer,
  CONSTRAINT batch_table_pkey PRIMARY KEY (batch_id),
  CONSTRAINT batch_table_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(uid),
  CONSTRAINT batch_table_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(uid)
);

CREATE TABLE IF NOT EXISTS public.machinery (
  machinery_id uuid NOT NULL DEFAULT gen_random_uuid(),
  machine_name text NOT NULL,
  machine_type text,
  machine_manufacture text,
  location text,
  status public.machine_status DEFAULT 'available',
  capacity numeric,
  power_rating numeric,
  created_at timestamp with time zone DEFAULT now(),
  created_by uuid,
  updated_at timestamp with time zone DEFAULT now(),
  updated_by uuid,
  CONSTRAINT machinery_pkey PRIMARY KEY (machinery_id),
  CONSTRAINT machinery_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(uid),
  CONSTRAINT machinery_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(uid)
);

CREATE TABLE IF NOT EXISTS public.raw_materials (
  raw_material_id uuid NOT NULL DEFAULT gen_random_uuid(),
  raw_material_name text NOT NULL,
  raw_material_code text UNIQUE,
  category text,
  quantity numeric DEFAULT 0,
  reorder_level numeric DEFAULT 0,
  unit_cost numeric,
  created_at timestamp with time zone DEFAULT now(),
  created_by uuid,
  updated_at timestamp with time zone DEFAULT now(),
  updated_by uuid,
  CONSTRAINT raw_materials_pkey PRIMARY KEY (raw_material_id),
  CONSTRAINT raw_materials_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(uid),
  CONSTRAINT raw_materials_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(uid)
);

-- ============================================================
-- 4. DEPENDENT TABLES (reference batch_table or other tables)
-- ============================================================

CREATE TABLE IF NOT EXISTS public.task_table (
  task_id uuid NOT NULL DEFAULT gen_random_uuid(),
  batch_id uuid,
  task_name text NOT NULL,
  task_description text,
  task_notes text,
  status public.task_status DEFAULT 'pending',
  output_product text,
  outputs_quantity numeric,
  start_time text,
  end_time text,
  created_at timestamp with time zone,
  created_by uuid,
  updated_at timestamp with time zone,
  updated_by uuid,
  estimated_duration integer,
  CONSTRAINT task_table_pkey PRIMARY KEY (task_id),
  CONSTRAINT task_table_batch_id_fkey FOREIGN KEY (batch_id) REFERENCES public.batch_table(batch_id),
  CONSTRAINT task_table_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(uid),
  CONSTRAINT task_table_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(uid)
);

CREATE TABLE IF NOT EXISTS public.incidents (
  incident_id uuid NOT NULL DEFAULT gen_random_uuid(),
  incident_name text NOT NULL,
  incident_type text,
  incident_video_id uuid,
  incident_voice_id uuid,
  incident_photo_id uuid,
  incident_time timestamp with time zone,
  incident_notes text,
  incident_severity public.incident_severity,
  incident_created_by uuid DEFAULT auth.uid(),
  incident_created_at timestamp with time zone,
  task_incident_id uuid,
  CONSTRAINT incidents_pkey PRIMARY KEY (incident_id),
  CONSTRAINT incidents_incident_created_by_fkey FOREIGN KEY (incident_created_by) REFERENCES public.users(uid),
  CONSTRAINT incidents_task_incident_id_fkey FOREIGN KEY (task_incident_id) REFERENCES public.task_table(task_id)
);

-- ============================================================
-- 5. JUNCTION / ASSIGNMENT TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS public.batch_assignees (
  batch_assignees_id uuid NOT NULL DEFAULT gen_random_uuid(),
  batch_id uuid,
  user_id uuid,
  CONSTRAINT batch_assignees_pkey PRIMARY KEY (batch_assignees_id),
  CONSTRAINT batch_assignees_batch_id_fkey FOREIGN KEY (batch_id) REFERENCES public.batch_table(batch_id),
  CONSTRAINT batch_assignees_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(uid)
);

CREATE TABLE IF NOT EXISTS public.task_assignees (
  assignees_id uuid NOT NULL DEFAULT gen_random_uuid(),
  task_id uuid,
  user_id uuid,
  CONSTRAINT task_assignees_pkey PRIMARY KEY (assignees_id),
  CONSTRAINT task_assignees_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task_table(task_id),
  CONSTRAINT task_assignees_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(uid)
);

CREATE TABLE IF NOT EXISTS public.task_machinery (
  task_machinery_id uuid NOT NULL DEFAULT gen_random_uuid(),
  task_id uuid,
  machinery_id uuid,
  CONSTRAINT task_machinery_pkey PRIMARY KEY (task_machinery_id),
  CONSTRAINT task_machinery_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task_table(task_id),
  CONSTRAINT task_machinery_machinery_id_fkey FOREIGN KEY (machinery_id) REFERENCES public.machinery(machinery_id)
);

CREATE TABLE IF NOT EXISTS public.task_raw_materials (
  task_raw_material_id uuid NOT NULL DEFAULT gen_random_uuid(),
  task_id uuid,
  raw_material_id uuid,
  material_name text,
  assigned_quantity numeric,
  CONSTRAINT task_raw_materials_pkey PRIMARY KEY (task_raw_material_id),
  CONSTRAINT task_raw_materials_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task_table(task_id),
  CONSTRAINT task_raw_materials_raw_material_id_fkey FOREIGN KEY (raw_material_id) REFERENCES public.raw_materials(raw_material_id)
);
