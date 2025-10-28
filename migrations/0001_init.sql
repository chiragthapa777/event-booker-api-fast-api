-- Enable UUID extension for unique IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- FILE TABLE
-- ============================================================
CREATE TABLE file (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_path TEXT NOT NULL,
    type VARCHAR(50),
    size BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- USER TABLE
-- ============================================================
CREATE TABLE app_user (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name VARCHAR(255),
    dob DATE,
    roles TEXT, 
    gender VARCHAR(20),
    phone_number VARCHAR(20),
    phone_verified_at TIMESTAMP,
    email_verified_at TIMESTAMP,
    profile_id UUID REFERENCES file(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);




-- ============================================================
-- EVENT TABLE
-- ============================================================
CREATE TABLE event (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    admin_id UUID REFERENCES app_user(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    seo_meta_data JSONB,
    date TIMESTAMP NOT NULL,
    venue VARCHAR(255),
    lng DECIMAL(10, 6),
    lat DECIMAL(10, 6),
    description TEXT,
    terms_and_condition TEXT,
    event_layout_photo_id UUID REFERENCES file(id) ON DELETE SET NULL,
    event_banner_photo_id UUID REFERENCES file(id) ON DELETE SET NULL,
    event_photo_id UUID REFERENCES file(id) ON DELETE SET NULL,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- EVENT_CATEGORY TABLE
-- ============================================================
CREATE TABLE category (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE event_category (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES category(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (event_id, category_id) 
);

-- ============================================================
-- EVENT_TICKET TABLE
-- ============================================================
CREATE TABLE event_ticket (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES event(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0,
    total_qty INTEGER NOT NULL DEFAULT 0,
    total_booked INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- BOOKING TABLE
-- ============================================================
CREATE TABLE booking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES app_user(id) ON DELETE CASCADE,
    event_id UUID REFERENCES event(id) ON DELETE CASCADE,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- BOOKING_TICKET TABLE
-- ============================================================
CREATE TABLE booking_ticket (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id UUID REFERENCES booking(id) ON DELETE CASCADE,
    event_ticket_id UUID REFERENCES event_ticket(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- PAYMENT TABLE
-- ============================================================
CREATE TABLE payment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES app_user(id) ON DELETE SET NULL,
    booking_id UUID REFERENCES booking(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    payment_detail JSONB,
    transaction_id TEXT UNIQUE,
    method VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
