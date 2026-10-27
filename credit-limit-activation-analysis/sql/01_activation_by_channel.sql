-- Business question: Which distribution channel yields the highest rate of credit limit activations?
-- Hypothesis: Customers who interact via a branch (office) rarely activate their credit limit,
-- Because they do not receive reminders.

SELECT
    channel,
    COUNT(*) AS total_clients,
    SUM(CASE WHEN activation_status = 'yes' THEN 1 ELSE 0 END) AS activated,
    ROUND(100.0 * SUM(CASE WHEN activation_status = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS activation_rate_pct
FROM clients
GROUP BY channel
ORDER BY activation_rate_pct ASC;