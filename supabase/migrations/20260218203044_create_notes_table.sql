-- Create enum types for notes
CREATE TYPE note_entity_type AS ENUM ('batch', 'task', 'equipment', 'incident');
CREATE TYPE note_type AS ENUM ('general', 'safety_concern', 'quality_issue', 'process_deviation', 'handover');

-- Create notes table
CREATE TABLE IF NOT EXISTS notes (
    note_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type note_entity_type NOT NULL,
    entity_id UUID NOT NULL,
    note_type note_type NOT NULL DEFAULT 'general',
    content TEXT NOT NULL,
    photo_url TEXT,
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Index for fast lookups by entity
CREATE INDEX idx_notes_entity ON notes(entity_type, entity_id);
CREATE INDEX idx_notes_created_by ON notes(created_by);
