-- Business question: how many days elapse between approval and the first purchase?
-- If a customer doesn’t make a purchase within the first 14 days, will they become active later on?

SELECT
    CASE
        WHEN days_since_approval <= 7 THEN '0-7 дней'
        WHEN days_since_approval <= 14 THEN '8-14 дней'
        WHEN days_since_approval <= 30 THEN '15-30 дней'
        ELSE '30+ дней'
    END AS period,
    COUNT(*) AS clients,
    SUM(CASE WHEN activation_status = 'yes' THEN 1 ELSE 0 END) AS activated,
    ROUND(100.0 * SUM(CASE WHEN activation_status = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS activation_rate_pct
FROM clients
GROUP BY period
ORDER BY period;