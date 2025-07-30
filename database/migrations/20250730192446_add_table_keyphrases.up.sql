CREATE TABLE
    user_keyphrases (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        user_id BIGINT NOT NULL,
        keyphrases TEXT,
        normalized_keyphrases TEXT,
        UNIQUE (user_id)
    );