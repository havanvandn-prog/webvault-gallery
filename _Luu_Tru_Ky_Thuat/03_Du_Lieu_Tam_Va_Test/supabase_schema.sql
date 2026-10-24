-- ==============================================================================
-- WEBVAULT SUPABASE DATABASE SCHEMA
-- Bảng lưu trữ kho mẫu website và phân loại đa tầng
-- ==============================================================================

-- 1. Bảng websites
CREATE TABLE IF NOT EXISTS public.websites (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(150),
    url TEXT NOT NULL,
    domain VARCHAR(150),
    industry VARCHAR(100) DEFAULT 'su-kien',
    industry_name VARCHAR(150) DEFAULT 'Sự kiện & Activation',
    vibe VARCHAR(100) DEFAULT 'dark-luxury',
    vibe_name VARCHAR(150) DEFAULT 'Dark Mode & Sang trọng',
    category VARCHAR(150),
    location VARCHAR(150),
    description TEXT,
    thumb_url TEXT NOT NULL,
    full_url TEXT NOT NULL,
    thumb_kb NUMERIC(8, 2),
    full_kb NUMERIC(8, 2),
    orig_kb NUMERIC(8, 2),
    status VARCHAR(50) DEFAULT 'approved',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Chỉ mục tìm kiếm nhanh
CREATE INDEX IF NOT EXISTS idx_websites_industry ON public.websites(industry);
CREATE INDEX IF NOT EXISTS idx_websites_vibe ON public.websites(vibe);
CREATE INDEX IF NOT EXISTS idx_websites_status ON public.websites(status);

-- 3. Chính sách bảo mật hàng (Row Level Security - RLS)
ALTER TABLE public.websites ENABLE ROW LEVEL SECURITY;

-- Cho phép mọi người đọc dữ liệu công khai (để xem trên WebVault)
CREATE POLICY "Public Read Access" 
ON public.websites FOR SELECT 
USING (status = 'approved');

-- Chỉ cho phép người dùng có quyền API ghi dữ liệu
CREATE POLICY "Service Role Full Access" 
ON public.websites FOR ALL 
USING (auth.role() = 'service_role');
