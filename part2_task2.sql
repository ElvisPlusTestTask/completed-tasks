
-- Удаление некорректных записей
DELETE FROM data
WHERE NOT EXISTS (
    SELECT 1 FROM messages WHERE user = data.user
)
AND NOT (
    SUBSTR(datastr, 1, 4) BETWEEN '0000' AND '9999'
    AND SUBSTR(datastr, 5, 2) BETWEEN '01' AND '12'
    AND SUBSTR(datastr, 7, 2) BETWEEN '01' AND '31'
    AND SUBSTR(datastr, 9, 2) BETWEEN '00' AND '23'
    AND SUBSTR(datastr, 11, 2) BETWEEN '00' AND '59'
    AND SUBSTR(datastr, 13, 2) BETWEEN '00' AND '59'
);

-- Проверяем наличие записей для каждого пользователя
INSERT INTO messages (user, message)
SELECT DISTINCT d.user, 'есть запись'
FROM data d
LEFT JOIN messages m ON d.user = m.user
WHERE m.user IS NULL
AND (SELECT COUNT(DISTINCT SUBSTR(datastr, 1, 8)) FROM data WHERE user = d.user) = 7;
