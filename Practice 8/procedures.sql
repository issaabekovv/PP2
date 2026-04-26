-- 1. Upsert: Добавление или обновление телефона, если имя уже есть
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Массовая вставка с валидацией телефона (только цифры, длина > 5)
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        -- Валидация через регулярное выражение (только цифры)
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) > 5 THEN
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone format for user %: %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact_proc(p_data VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_data OR phone = p_data;
END;
$$;