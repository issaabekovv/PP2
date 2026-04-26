CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
END;
$$;