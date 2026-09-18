-- CCMIMS ORGANIZATIONAL SEED DATA
-- Source: Tanzania Catholic Directory 2020 (TEC)
-- Verified against the supplied Django models.
-- Includes:
--   34 dioceses from the Directory contents
--   36 deaneries explicitly identified in the supplied Directory sections
--   140 actual parishes with explicit parish-to-deanery mappings
-- Quasi-parishes are excluded from members_parish.
-- Dar es Salaam deaneries include St Agostino and St Francis Asizi,
-- which are listed in the Directory's deanery table.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

BEGIN;

INSERT INTO members_diocese
    (id, name, description, is_active, created_at, updated_at)
VALUES
    (gen_random_uuid(), 'Archdiocese of Arusha', 'Archdiocese of Arusha', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Bukoba', 'Diocese of Bukoba', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Bunda', 'Diocese of Bunda', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Archdiocese of Dar es Salaam', 'Archdiocese of Dar es Salaam', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Archdiocese of Dodoma', 'Archdiocese of Dodoma', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Geita', 'Diocese of Geita', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Ifakara', 'Diocese of Ifakara', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Iringa', 'Diocese of Iringa', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Kahama', 'Diocese of Kahama', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Kayanga', 'Diocese of Kayanga', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Kigoma', 'Diocese of Kigoma', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Kondoa', 'Diocese of Kondoa', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Lindi', 'Diocese of Lindi', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Mahenge', 'Diocese of Mahenge', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Archdiocese of Mbeya', 'Archdiocese of Mbeya', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Mbinga', 'Diocese of Mbinga', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Mbulu', 'Diocese of Mbulu', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Morogoro', 'Diocese of Morogoro', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Moshi', 'Diocese of Moshi', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Mpanda', 'Diocese of Mpanda', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Mtwara', 'Diocese of Mtwara', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Musoma', 'Diocese of Musoma', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Archdiocese of Mwanza', 'Archdiocese of Mwanza', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Njombe', 'Diocese of Njombe', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Rulenge-Ngara', 'Diocese of Rulenge-Ngara', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Same', 'Diocese of Same', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Shinyanga', 'Diocese of Shinyanga', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Singida', 'Diocese of Singida', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Archdiocese of Songea', 'Archdiocese of Songea', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Sumbawanga', 'Diocese of Sumbawanga', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Archdiocese of Tabora', 'Archdiocese of Tabora', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Tanga', 'Diocese of Tanga', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Tunduru-Masasi', 'Diocese of Tunduru-Masasi', TRUE, NOW(), NOW()),
    (gen_random_uuid(), 'Diocese of Zanzibar', 'Diocese of Zanzibar', TRUE, NOW(), NOW())
ON CONFLICT (name) DO NOTHING;

INSERT INTO members_deanery
    (id, diocese_id, name, description, is_active, created_at, updated_at)
VALUES

-- =========================================================
-- ARCHDIOCESE OF ARUSHA — 8 DEANERIES
-- =========================================================

(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Arusha'),
    'East Arusha Municipality',
    'East Arusha Municipality Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Arusha'),
    'West Arusha Municipality',
    'West Arusha Municipality Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Arusha'),
    'Monduli',
    'Monduli Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Arusha'),
    'Arumeru',
    'Arumeru Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Arusha'),
    'Ngorongoro',
    'Ngorongoro Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Arusha'),
    'Simanjiro',
    'Simanjiro Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Arusha'),
    'Kiteto',
    'Kiteto Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Arusha'),
    'Longido',
    'Longido Deanery',
    TRUE,
    NOW(),
    NOW()
),

-- =========================================================
-- ARCHDIOCESE OF DAR ES SALAAM — 12 DEANERIES
-- =========================================================

(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'St Joseph',
    'St Joseph Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'Segerea',
    'Segerea Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'St Gaspar',
    'St Gaspar Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'St Peter',
    'St Peter Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'Ubungo',
    'Ubungo Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'Kilima Hewa',
    'Kilima Hewa Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'Ukonga',
    'Ukonga Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'Kibaha',
    'Kibaha Deanery',
    TRUE,
    NOW(),
    NOW()
),

-- =========================================================
-- DIOCESE OF KAHAMA — 5 DEANERIES
-- =========================================================

(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Kahama'),
    'Kahama Town',
    'Kahama Town Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Kahama'),
    'Ngaya',
    'Ngaya Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Kahama'),
    'Ushirombo',
    'Ushirombo Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Kahama'),
    'Iboja',
    'Iboja Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Kahama'),
    'Masumbwe',
    'Masumbwe Deanery',
    TRUE,
    NOW(),
    NOW()
),

-- =========================================================
-- DIOCESE OF SAME — 3 DEANERIES
-- =========================================================

(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Same'),
    'Chambogho',
    'Chambogho Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Same'),
    'Shengena',
    'Shengena Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Same'),
    'Kindoroko',
    'Kindoroko Deanery',
    TRUE,
    NOW(),
    NOW()
),

-- =========================================================
-- DIOCESE OF SUMBAWANGA — 4 ZONE/DEANERIES
-- =========================================================

(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Sumbawanga'),
    'Central',
    'Central Zone/Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Sumbawanga'),
    'Southern',
    'Southern Zone/Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Sumbawanga'),
    'Nkansi',
    'Nkansi Zone/Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Sumbawanga'),
    'Kalambo',
    'Kalambo Zone/Deanery',
    TRUE,
    NOW(),
    NOW()
),

-- =========================================================
-- DIOCESE OF TANGA — 4 DEANERIES
-- =========================================================

(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Tanga'),
    'Tanga',
    'Tanga Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Tanga'),
    'Korogwe',
    'Korogwe Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Tanga'),
    'Handeni',
    'Handeni Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Diocese of Tanga'),
    'Lushoto',
    'Lushoto Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),

    (SELECT id
     FROM members_diocese
     WHERE name = 'Archdiocese of Dar es Salaam'),

    'Mbezi Luis',

    'Mbezi Luis Deanery',

    TRUE,

    NOW(),

    NOW()

),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'St Agostino',
    'St Agostino Deanery',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    (SELECT id FROM members_diocese WHERE name = 'Archdiocese of Dar es Salaam'),
    'St Francis Asizi',
    'St Francis Asizi Deanery',
    TRUE,
    NOW(),
    NOW()
),

(

    gen_random_uuid(),

    (SELECT id
     FROM members_diocese
     WHERE name = 'Archdiocese of Dar es Salaam'),

    'Kigamboni',

    'Kigamboni Deanery',

    TRUE,

    NOW(),

    NOW()

)

ON CONFLICT (diocese_id, name) DO NOTHING;

-- CCMIMS: Verified parish seed data from Tanzania Catholic Directory 2020
-- Source: Tanzania Catholic Directory, 2020 Edition (TEC)
-- This script inserts only parishes whose deanery relationship is explicitly
-- identifiable from the Directory. It does NOT guess missing deanery mappings.
-- Verified groups included here:
--   Archdiocese of Arusha: 55
--   Diocese of Kahama: 27
--   Diocese of Sumbawanga: 21
--   Diocese of Tanga: 37
-- Total: 140 parishes

CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- Archdiocese of Arusha
-- Archdiocese of Arusha

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Theresa Cathedral Parish',
    'St. Theresa Cathedral Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Family Parish - Njiro',
    'Holy Family Parish - Njiro',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Simon Parish - Loruvani',
    'St. Simon Parish - Loruvani',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Peter and Paul Parish - Kijenge',
    'St. Peter and Paul Parish - Kijenge',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Francis of Assisi Parish - Kwangulelo',
    'St. Francis of Assisi Parish - Kwangulelo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Ambrose Kibuka Parish - Sinon',
    'St. Ambrose Kibuka Parish - Sinon',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Immaculate Heart of Mary Parish - Unga Ltd',
    'Immaculate Heart of Mary Parish - Unga Ltd',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. James the Apostle Parish - Moshono',
    'St. James the Apostle Parish - Moshono',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Jude Thaddeus Parish - Muriet',
    'St. Jude Thaddeus Parish - Muriet',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Jude Thaddeus Parish - Ilboru',
    'St. Jude Thaddeus Parish - Ilboru',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Josephine Bakhita Parish - Korona',
    'St. Josephine Bakhita Parish - Korona',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'East Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Spirit Parish - Ngarenaro',
    'Holy Spirit Parish - Ngarenaro',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'West Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Epiphany Parish - Burka',
    'Epiphany Parish - Burka',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'West Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Monica Parish - Sakina',
    'St. Monica Parish - Sakina',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'West Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Sacred Heart of Jesus Parish - Sombetini',
    'Sacred Heart of Jesus Parish - Sombetini',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'West Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Vincent Pallotti Parish - Esso',
    'St. Vincent Pallotti Parish - Esso',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'West Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Joseph the Worker Parish - Olasiti',
    'St. Joseph the Worker Parish - Olasiti',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'West Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Trinity Parish - Kwambrombo',
    'Holy Trinity Parish - Kwambrombo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'West Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Cross Parish - Kisongo',
    'Holy Cross Parish - Kisongo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'West Arusha Municipality'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Blessed Mother of God Parish - Monduli Mjini',
    'Blessed Mother of God Parish - Monduli Mjini',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Monduli'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Jude Thaddeus Parish - Mto wa Mbu',
    'St. Jude Thaddeus Parish - Mto wa Mbu',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Monduli'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Francis of Assisi Parish - Monduli Juu',
    'St. Francis of Assisi Parish - Monduli Juu',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Monduli'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Moita Bwawani Parish',
    'Moita Bwawani Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Monduli'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Charles Lwanga Martyr Parish - Usa River',
    'St. Charles Lwanga Martyr Parish - Usa River',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kikatiti Parish',
    'Kikatiti Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Stephen Proto Martyr Parish - Maji ya Chai',
    'St. Stephen Proto Martyr Parish - Maji ya Chai',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Noe Mawaggali Parish - Polising’isi',
    'St. Noe Mawaggali Parish - Polising’isi',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Joseph the Husband of Mary Parish - Patandi',
    'St. Joseph the Husband of Mary Parish - Patandi',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Christ the King Parish - Chekereni',
    'Christ the King Parish - Chekereni',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Francis de Sales Parish - Ngurdoto',
    'St. Francis de Sales Parish - Ngurdoto',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mirerani Parish',
    'Mirerani Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mbuguni Parish',
    'Mbuguni Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Joseph the Worker Parish - Nambala',
    'St. Joseph the Worker Parish - Nambala',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Thomas the Apostle Parish - Manyire',
    'St. Thomas the Apostle Parish - Manyire',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Nyumba ya Mungu Parish',
    'Nyumba ya Mungu Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Arumeru'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Christ the Good Shepherd Parish - Loliondo',
    'Christ the Good Shepherd Parish - Loliondo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Ngorongoro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Augustine Parish - Digodigo',
    'St. Augustine Parish - Digodigo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Ngorongoro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Endulen Parish',
    'Endulen Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Ngorongoro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Paul the Apostle Parish - Ngorongoro',
    'St. Paul the Apostle Parish - Ngorongoro',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Ngorongoro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mary Mother of God Parish - Nainokanoka',
    'Mary Mother of God Parish - Nainokanoka',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Ngorongoro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Malambo Parish',
    'Malambo Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Ngorongoro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Christ the Good Shepherd Parish - Emboreet',
    'Christ the Good Shepherd Parish - Emboreet',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Simanjiro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Augustine Parish - Orkesumet',
    'St. Augustine Parish - Orkesumet',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Simanjiro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Joseph Parish - Landanai',
    'St. Joseph Parish - Landanai',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Simanjiro'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kijungu Parish',
    'Kijungu Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Kiteto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Sunya Parish',
    'Sunya Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Kiteto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Blessed Mary of the Assumption Parish - Kibaya',
    'Blessed Mary of the Assumption Parish - Kibaya',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Kiteto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Matui Parish',
    'Matui Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Kiteto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Mathias Apostle Parish - Ngaramtoni',
    'St. Mathias Apostle Parish - Ngaramtoni',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Longido'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Christ the Good Shepherd Parish - Namanga',
    'Christ the Good Shepherd Parish - Namanga',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Longido'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Francis Xavery Parish - Olosipa',
    'St. Francis Xavery Parish - Olosipa',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Longido'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Enduimet Parish',
    'Enduimet Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Longido'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kamwanga Parish',
    'Kamwanga Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Longido'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Lawrence Parish - Longido',
    'St. Lawrence Parish - Longido',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Longido'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Engikaret Parish',
    'Engikaret Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Archdiocese of Arusha'
  AND de.name = 'Longido'
ON CONFLICT (deanery_id, name) DO NOTHING;

-- Diocese of Kahama
INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Charles Lwanga Parish',
    'St. Charles Lwanga Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Kahama Town'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Stephen the Martyr Parish - Nyasubi',
    'St. Stephen the Martyr Parish - Nyasubi',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Kahama Town'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mary Mother of Good Counsel Parish - Mbulu',
    'Mary Mother of Good Counsel Parish - Mbulu',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Kahama Town'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Family Parish - Kagongwa',
    'Holy Family Parish - Kagongwa',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Kahama Town'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Francis De Sales Parish - Isaka',
    'St. Francis De Sales Parish - Isaka',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Kahama Town'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Spirit Parish - Majengo',
    'Holy Spirit Parish - Majengo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Kahama Town'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Sts. Simon and Jude Thaddeus Parish - Busoka',
    'Sts. Simon and Jude Thaddeus Parish - Busoka',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Kahama Town'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Sts. Cosmas and Damian Parish - Mhungula',
    'Sts. Cosmas and Damian Parish - Mhungula',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Kahama Town'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Michael the Archangel Parish - Ngaya',
    'St. Michael the Archangel Parish - Ngaya',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ngaya'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Matthew the Evangelist Parish - Ilogi',
    'St. Matthew the Evangelist Parish - Ilogi',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ngaya'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Theresa of the Child Jesus - Segese',
    'St. Theresa of the Child Jesus - Segese',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ngaya'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mary Mother of Perpetual Help Parish - Ushirombo',
    'Mary Mother of Perpetual Help Parish - Ushirombo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ushirombo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mystery of the Cross Parish - Maganzo',
    'Mystery of the Cross Parish - Maganzo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ushirombo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Eucharist Parish - Kabuhima',
    'Holy Eucharist Parish - Kabuhima',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ushirombo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'The Sacred Heart of Jesus Parish - Kaniha',
    'The Sacred Heart of Jesus Parish - Kaniha',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ushirombo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Trinity Parish - Lulembela',
    'Holy Trinity Parish - Lulembela',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ushirombo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Pope John Paul II Parish - Namonge',
    'St. Pope John Paul II Parish - Namonge',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Ushirombo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Mark the Evangelist Parish - Iboja',
    'St. Mark the Evangelist Parish - Iboja',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Iboja'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mary Mother of Lourdes Parish - Ushetu',
    'Mary Mother of Lourdes Parish - Ushetu',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Iboja'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Divine Mercy Parish - Bulungwa',
    'Divine Mercy Parish - Bulungwa',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Iboja'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. John the Apostle Parish - Ifunde',
    'St. John the Apostle Parish - Ifunde',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Iboja'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Mother Theresa of Calcutta - Chona',
    'St. Mother Theresa of Calcutta - Chona',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Iboja'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Sts. Peter and Paul the Apostles Parish - Nyamilangano',
    'Sts. Peter and Paul the Apostles Parish - Nyamilangano',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Iboja'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Joseph the Worker Parish - Masumbwe',
    'St. Joseph the Worker Parish - Masumbwe',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Masumbwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Name of Jesus Parish - Bukombe',
    'Holy Name of Jesus Parish - Bukombe',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Masumbwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mary Queen of the Most Holy Rosary - Itimbya',
    'Mary Queen of the Most Holy Rosary - Itimbya',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Masumbwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Maximilian Kolbe Parish - Iponya',
    'St. Maximilian Kolbe Parish - Iponya',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Kahama'
  AND de.name = 'Masumbwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

-- Diocese of Sumbawanga
INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'The Cathedral Parish',
    'The Cathedral Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Central'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Spirit Parish',
    'Holy Spirit Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Central'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Holy Family Parish',
    'Holy Family Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Central'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Christ the King Parish',
    'Christ the King Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Central'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Izimba Parish',
    'Izimba Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Central'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Ipito Parish',
    'Ipito Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Central'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Francis of Assisi Parish',
    'St. Francis of Assisi Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Central'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Tunduma Parish',
    'Tunduma Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Southern'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mwazye Parish',
    'Mwazye Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Southern'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mpui Parish',
    'Mpui Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Southern'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Laela Parish',
    'Laela Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Southern'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kaengesa Parish',
    'Kaengesa Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Southern'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Chala Parish',
    'Chala Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Nkansi'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kirando Parish',
    'Kirando Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Nkansi'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kate Parish',
    'Kate Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Nkansi'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kala Parish',
    'Kala Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Nkansi'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Namanyere Parish',
    'Namanyere Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Nkansi'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Matai Parish',
    'Matai Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Kalambo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kasanga Parish',
    'Kasanga Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Kalambo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Ulumi Parish',
    'Ulumi Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Kalambo'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Sopa Parish',
    'Sopa Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Sumbawanga'
  AND de.name = 'Kalambo'
ON CONFLICT (deanery_id, name) DO NOTHING;

-- Diocese of Tanga
INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Anthony’s Cathedral, Chumbageni',
    'St. Anthony’s Cathedral, Chumbageni',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Theresa - Barabara ya 20',
    'St. Theresa - Barabara ya 20',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Mathias Mulumba - Sahare',
    'St. Mathias Mulumba - Sahare',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Donge Parish',
    'Donge Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Joseph’s Mukasa - Amboni',
    'St. Joseph’s Mukasa - Amboni',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Pangani Parish',
    'Pangani Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Muheza Parish',
    'Muheza Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mtindiro Parish',
    'Mtindiro Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mlingano Parish',
    'Mlingano Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Amani Parish',
    'Amani Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'St. Peter’s Saruji',
    'St. Peter’s Saruji',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Maramba Parish',
    'Maramba Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Misozwe Parish',
    'Misozwe Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Tanga'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kilole Parish',
    'Kilole Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Korogwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Hale Parish',
    'Hale Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Korogwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Potwe Parish',
    'Potwe Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Korogwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kwalukonge Parish',
    'Kwalukonge Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Korogwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Magoma Parish',
    'Magoma Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Korogwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mazinde Ngua Parish',
    'Mazinde Ngua Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Korogwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mombo Parish',
    'Mombo Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Korogwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Manundu Parish',
    'Manundu Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Korogwe'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Handeni Parish',
    'Handeni Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Handeni'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kwediboma Parish',
    'Kwediboma Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Handeni'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Kabuku Parish',
    'Kabuku Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Handeni'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mkalamo Parish',
    'Mkalamo Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Handeni'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Lushoto Parish',
    'Lushoto Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Malindi Parish',
    'Malindi Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Mkuzi Parish',
    'Mkuzi Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Soni Parish',
    'Soni Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Tekwa Parish',
    'Tekwa Parish',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Parokia ya Sakhrani',
    'Parokia ya Sakhrani',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Parokia ya Mabughai',
    'Parokia ya Mabughai',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Parokia ya Rangwi',
    'Parokia ya Rangwi',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Parokia ya Kongoi',
    'Parokia ya Kongoi',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Parokia ya Gare',
    'Parokia ya Gare',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Parokia ya Kwai',
    'Parokia ya Kwai',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

INSERT INTO members_parish
    (id, deanery_id, name, description, is_active, created_at, updated_at)
SELECT
    gen_random_uuid(),
    de.id,
    'Parokia ya Kifungilo',
    'Parokia ya Kifungilo',
    TRUE,
    NOW(),
    NOW()
FROM members_deanery de
JOIN members_diocese d ON d.id = de.diocese_id
WHERE d.name = 'Diocese of Tanga'
  AND de.name = 'Lushoto'
ON CONFLICT (deanery_id, name) DO NOTHING;

-- ============================================================
-- ZONES
-- Create 40 zones for every parish
-- ============================================================

INSERT INTO members_zone
(
    id,
    parish_id,
    name,
    description,
    is_active,
    created_at,
    updated_at
)
SELECT
    gen_random_uuid(),
    p.id,
    'Zone ' || z.zone_number,
    'Zone ' || z.zone_number || ' of ' || p.name,
    TRUE,
    NOW(),
    NOW()
FROM members_parish p
CROSS JOIN generate_series(1, 40) AS z(zone_number)
ON CONFLICT (parish_id, name) DO NOTHING;


-- ============================================================
-- SMALL CHRISTIAN COMMUNITIES
-- Create 40 SCCs for every zone
-- ============================================================

INSERT INTO members_smallchristiancommunity
(
    id,
    zone_id,
    name,
    description,
    is_active,
    created_at,
    updated_at
)
SELECT
    gen_random_uuid(),
    z.id,
    'Small Christian Community ' || scc_number,
    'Small Christian Community ' || scc_number || ' of ' || z.name,
    TRUE,
    NOW(),
    NOW()
FROM members_zone z
CROSS JOIN generate_series(1, 40) AS scc_number
ON CONFLICT (zone_id, name) DO NOTHING;

-- ============================================================
-- CHURCH ASSOCIATIONS / VYAMA VYA KITUME
-- ============================================================

INSERT INTO members_churchassociation
(
    id,
    name,
    description,
    is_active,
    created_at,
    updated_at
)
VALUES
(
    gen_random_uuid(),
    'UWAKA',
    'Umoja wa Wanawake wa Kanisa.',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    'WAWAKA',
    'Women association within the Catholic Church.',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    'TCMS',
    'Tanzania Catholic Men association.',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    'UKWAKATA',
    'Umoja wa vijana wa Kanisa Katoliki.',
    TRUE,
    NOW(),
    NOW()
)
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- LEADERSHIP POSITIONS / WADHIFA
-- ============================================================

INSERT INTO members_leadershipposition
(
    id,
    name,
    description,
    is_active,
    created_at,
    updated_at
)
VALUES
(
    gen_random_uuid(),
    'Shemasi',
    'Deacon serving in the Catholic Church.',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    'Padri',
    'Priest serving the Catholic Church community.',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    'Katekista',
    'Catechist responsible for supporting catechesis and Christian formation.',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    'Mzee wa Jumuiya',
    'Leader responsible for supporting and coordinating the Small Christian Community.',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    'Mzee wa Kanisa',
    'Leader responsible for supporting and coordinating the Holy Masses and Parish.',
    TRUE,
    NOW(),
    NOW()
),
(
    gen_random_uuid(),
    'Mwenyekiti wa Chama cha Kitume',
    'Chairperson of a Catholic Church association.',
    TRUE,
    NOW(),
    NOW()
)
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- FINAL CCMIMS ORGANIZATION DATA VERIFICATION
-- ============================================================

SELECT 'Dioceses' AS entity, COUNT(*) AS total
FROM members_diocese

UNION ALL

SELECT 'Deaneries', COUNT(*)
FROM members_deanery

UNION ALL

SELECT 'Parishes', COUNT(*)
FROM members_parish

UNION ALL

SELECT 'Zones', COUNT(*)
FROM members_zone

UNION ALL

SELECT 'Small Christian Communities', COUNT(*)
FROM members_smallchristiancommunity

UNION ALL

SELECT 'Church Associations', COUNT(*)
FROM members_churchassociation

UNION ALL

SELECT 'Leadership Positions', COUNT(*)
FROM members_leadershipposition

UNION ALL

SELECT 'Families', COUNT(*)
FROM members_family

ORDER BY entity;