-- Chunk 3: Enrich existing tables with new columns

-- ============================================================
-- 1. MACHINERY — add serial_number, purchase_date, warranty_expiry, photo_url, notes
-- ============================================================

ALTER TABLE public.machinery
  ADD COLUMN IF NOT EXISTS serial_number text,
  ADD COLUMN IF NOT EXISTS purchase_date date,
  ADD COLUMN IF NOT EXISTS warranty_expiry date,
  ADD COLUMN IF NOT EXISTS photo_url text,
  ADD COLUMN IF NOT EXISTS notes text;

-- ============================================================
-- 2. BATCH_TABLE — add priority, production_line
-- ============================================================

DO $$ BEGIN
  CREATE TYPE public.batch_priority AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

ALTER TABLE public.batch_table
  ADD COLUMN IF NOT EXISTS priority public.batch_priority DEFAULT 'medium',
  ADD COLUMN IF NOT EXISTS production_line text;

-- ============================================================
-- 3. TASK_TABLE — add sequence_order, depends_on_task_id, sop_document_url
-- ============================================================

ALTER TABLE public.task_table
  ADD COLUMN IF NOT EXISTS sequence_order integer,
  ADD COLUMN IF NOT EXISTS depends_on_task_id uuid REFERENCES public.task_table(task_id),
  ADD COLUMN IF NOT EXISTS sop_document_url text;

-- ============================================================
-- 4. INCIDENTS — add location, personnel_involved, immediate_actions, witness_info, is_anonymous
-- ============================================================

ALTER TABLE public.incidents
  ADD COLUMN IF NOT EXISTS location text,
  ADD COLUMN IF NOT EXISTS personnel_involved text,
  ADD COLUMN IF NOT EXISTS immediate_actions text,
  ADD COLUMN IF NOT EXISTS witness_info text,
  ADD COLUMN IF NOT EXISTS is_anonymous boolean DEFAULT false;

-- ============================================================
-- 5. RAW_MATERIALS — add supplier, unit_of_measure, lot_number
-- ============================================================

ALTER TABLE public.raw_materials
  ADD COLUMN IF NOT EXISTS supplier text,
  ADD COLUMN IF NOT EXISTS unit_of_measure text,
  ADD COLUMN IF NOT EXISTS lot_number text;
