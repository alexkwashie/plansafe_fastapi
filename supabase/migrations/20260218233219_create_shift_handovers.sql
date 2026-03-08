-- Create shift handovers table
CREATE TABLE IF NOT EXISTS shift_handovers (
    handover_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outgoing_user_id UUID REFERENCES auth.users(id),
    incoming_user_id UUID REFERENCES auth.users(id),
    shift_date DATE NOT NULL,
    batch_status_summary TEXT,
    outstanding_issues TEXT,
    tasks_completed TEXT,
    tasks_remaining TEXT,
    equipment_notes TEXT,
    incidents_occurred TEXT,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_handovers_outgoing ON shift_handovers(outgoing_user_id);
CREATE INDEX idx_handovers_incoming ON shift_handovers(incoming_user_id);
CREATE INDEX idx_handovers_date ON shift_handovers(shift_date);
