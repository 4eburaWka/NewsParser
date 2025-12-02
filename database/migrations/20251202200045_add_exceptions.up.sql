CREATE TABLE
    user_exeptions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        user_id BIGINT NOT NULL,
        exeptions TEXT,
        UNIQUE (user_id)
    );