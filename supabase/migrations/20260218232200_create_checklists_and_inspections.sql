-- Create enum types
CREATE TYPE checklist_type AS ENUM ('pre_shift', 'equipment', 'area');
CREATE TYPE inspection_status AS ENUM ('pending', 'in_progress', 'completed');
CREATE TYPE inspection_response_value AS ENUM ('pass', 'fail', 'na');

-- Checklist templates
CREATE TABLE IF NOT EXISTS checklist_templates (
    template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type checklist_type NOT NULL DEFAULT 'pre_shift',
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Checklist template items
CREATE TABLE IF NOT EXISTS checklist_template_items (
    item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID NOT NULL REFERENCES checklist_templates(template_id) ON DELETE CASCADE,
    item_text TEXT NOT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    required BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_template_items_template ON checklist_template_items(template_id);

-- Inspections
CREATE TABLE IF NOT EXISTS inspections (
    inspection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID NOT NULL REFERENCES checklist_templates(template_id),
    inspector_id UUID REFERENCES auth.users(id),
    status inspection_status NOT NULL DEFAULT 'pending',
    scheduled_date DATE,
    completed_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_inspections_template ON inspections(template_id);
CREATE INDEX idx_inspections_inspector ON inspections(inspector_id);
CREATE INDEX idx_inspections_status ON inspections(status);

-- Inspection responses
CREATE TABLE IF NOT EXISTS inspection_responses (
    response_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inspection_id UUID NOT NULL REFERENCES inspections(inspection_id) ON DELETE CASCADE,
    template_item_id UUID NOT NULL REFERENCES checklist_template_items(item_id),
    response inspection_response_value NOT NULL,
    notes TEXT,
    photo_url TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_inspection_responses_inspection ON inspection_responses(inspection_id);
