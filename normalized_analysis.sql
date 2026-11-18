-- Q1 — Top legal areas
SELECT a.area_name, COUNT(*) AS documents
        FROM legal_areas a
        JOIN document_areas da ON a.area_id = da.area_id
        GROUP BY a.area_id, a.area_name
        ORDER BY documents DESC
        LIMIT 10;

-- Q2 — Legal areas by decade
SELECT d.decade, a.area_name,
               COUNT(*) AS documents
        FROM legal_documents d
        JOIN document_areas da ON d.law_id = da.law_id
        JOIN legal_areas a ON da.area_id = a.area_id
        WHERE d.decade >= 1990
        GROUP BY d.decade, a.area_id, a.area_name
        ORDER BY d.decade DESC, documents DESC
        LIMIT 15;

-- Q3 — Areas with at least 100 documents
SELECT a.area_name, COUNT(*) AS documents
        FROM legal_areas a
        JOIN document_areas da ON a.area_id = da.area_id
        GROUP BY a.area_id, a.area_name
        HAVING COUNT(*) >= 100
        ORDER BY documents DESC
        LIMIT 10;

-- Q4 — Multi-area documents
SELECT COUNT(*) AS multi_area_documents
        FROM (
            SELECT law_id
            FROM document_areas
            GROUP BY law_id
            HAVING COUNT(DISTINCT area_id) > 1
        );

-- Q5 — Ranked legal areas by decade
WITH area_counts AS (
            SELECT d.decade, a.area_name,
                   COUNT(*) AS documents
            FROM legal_documents d
            JOIN document_areas da
                 ON d.law_id = da.law_id
            JOIN legal_areas a
                 ON da.area_id = a.area_id
            WHERE d.decade >= 1990
            GROUP BY d.decade, a.area_id, a.area_name
        ),
        ranked AS (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY decade
                       ORDER BY documents DESC, area_name
                   ) AS rank_in_decade
            FROM area_counts
        )
        SELECT *
        FROM ranked
        WHERE rank_in_decade <= 3
        ORDER BY decade, rank_in_decade;

-- Q6 — Unresolved categories by decade
SELECT d.decade,
               COUNT(*) AS total_documents,
               COUNT(u.law_id) AS unresolved,
               ROUND(
                   100.0 * COUNT(u.law_id) /
                   NULLIF(COUNT(*), 0), 2
               ) AS unresolved_percent
        FROM legal_documents d
        LEFT JOIN unresolved_area_strings u
             ON d.law_id = u.law_id
        WHERE d.decade >= 1990
        GROUP BY d.decade
        ORDER BY d.decade;

-- Q7 — Category diversity by decade
SELECT d.decade,
               COUNT(DISTINCT da.area_id)
                   AS distinct_areas,
               COUNT(DISTINCT d.law_id)
                   AS classified_documents
        FROM legal_documents d
        JOIN document_areas da
             ON d.law_id = da.law_id
        WHERE d.decade >= 1990
        GROUP BY d.decade
        ORDER BY d.decade;

-- Q8 — Top years for legal area links
WITH yearly_counts AS (
            SELECT d.year,
                   COUNT(*) AS area_links
            FROM legal_documents d
            JOIN document_areas da
                 ON d.law_id = da.law_id
            WHERE d.year IS NOT NULL
            GROUP BY d.year
        )
        SELECT year, area_links
        FROM yearly_counts
        ORDER BY area_links DESC
        LIMIT 10;