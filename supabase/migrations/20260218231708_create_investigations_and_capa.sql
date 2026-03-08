-- Create enum types
CREATE TYPE investigation_status AS ENUM ('open', 'in_progress', 'closed');
CREATE TYPE investigation_type AS ENUM ('five_why', 'fishbone', 'root_cause');
CREATE TYPE capa_action_type AS ENUM ('corrective', 'preventive');
CREATE TYPE capa_status AS ENUM ('open', 'in_progress', 'completed', 'overdue');

-- Create investigations table
CREATE TABLE IF NOT EXISTS investigations (
    investigation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
    assigned_to UUID REFERENCES auth.users(id),
    status investigation_status NOT NULL DEFAULT 'open',
    investigation_type investigation_type,
    findings TEXT,
    root_cause TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    closed_at TIMESTAMPTZ
);

CREATE INDEX idx_investigations_incident ON investigations(incident_id);
CREATE INDEX idx_investigations_assigned ON investigations(assigned_to);
CREATE INDEX idx_investigations_status ON investigations(status);

-- Create CAPA actions table
CREATE TABLE IF NOT EXISTS capa_actions (
    capa_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    investigation_id UUID NOT NULL REFERENCES investigations(investigation_id) ON DELETE CASCADE,
    action_type capa_action_type NOT NULL,
    description TEXT NOT NULL,
    assigned_to UUID REFERENCES auth.users(id),
    due_date DATE,
    status capa_status NOT NULL DEFAULT 'open',
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_capa_investigation ON capa_actions(investigation_id);
CREATE INDEX idx_capa_status ON capa_actions(status);
CREATE INDEX idx_capa_assigned ON capa_actions(assigned_to);
