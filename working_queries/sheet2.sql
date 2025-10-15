-- Cohort Six Year Graduation Rate

SELECT
    CASE 
        WHEN c.term LIKE '%08' THEN 'Fall ' || SUBSTR(c.term + 600, 3, 2)
        WHEN c.term LIKE '%01' THEN 'Spring ' || SUBSTR(c.term + 600, 3, 2)
        WHEN c.term LIKE '%05' THEN 'Summer ' || SUBSTR(c.term + 600, 3, 2)
        ELSE c.term
    END AS "Graduation Term",
    ROUND(SUM(CASE WHEN c.grad_term IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS "Graduation Rate"
FROM edwprd.sdmcohortfr_us c
WHERE c.ft_pt_ind = 'FT' 
AND c.term = '201808'
GROUP BY c.term;
