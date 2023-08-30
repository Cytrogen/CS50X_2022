-- Keep a log of any SQL queries you execute as you solve the mystery.

-- All you know is that the theft took place on July 28, 2021 and that it took place on Humphrey Street.

-- The THIEF is:
-- The city the thief ESCAPED TO:
-- The ACCOMPLICE is:


-- Log start:

-- First, look up crime scene report descriptions on 7.28 2021
SELECT description FROM crime_scene_reports
WHERE year = 2021
    AND month = 7
    AND day = 28;
-- There is one description mentions CS50 Duck

-- Check this description's id
SELECT id FROM crime_scene_reports
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND description LIKE "%CS50%";
-- Theft took place at 10:15AM at the Humphrey Street bakery
-- Three witnesses were interviewed at the time

-- Check interview
SELECT transcript FROM interviews
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND transcript LIKE "%bakery%";

-- Within 10 minutes the theft got into a car in the bakery parking lot and drive away
SELECT license_plate FROM bakery_security_logs
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute >= 15
    AND minute <= 25
    AND activity = 'exit';

-- Theft was using ATM on Leggett Street withdrawing money
SELECT account_number, amount FROM atm_transactions
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND atm_location LIKE 'Leggett Street'
    AND transaction_type = 'withdraw';

-- Theft was calling the accomplice for less than a minute
SELECT caller, receiver FROM phone_calls
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60;

-- Accomplice was purchasing flight ticket (earliest flight) out of Fifty Ville (tomorrow)
SELECT id FROM airports
WHERE city LIKE 'Fiftyville';
-- origin airports id = 8

-- Find the possible flights
SELECT id, destination_airport_id FROM flights
WHERE year = 2021
    AND month = 7
    AND day = 29
    AND origin_airport_id = 8
ORDER BY hour, minute
LIMIT 1;
-- id: 36
-- destination airport id: 4

-- Check where the theft escaped to
SELECT city FROM airports
WHERE id = 4;
-- The theft escaped to New York City

-- Check who the theft is
-- people has phone number, passport number, and license plate to determine who he or she is
-- Check passport number first
SELECT people.name FROM people
INNER JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id = 36;
-- Passengers on flight 36
-- +--------+
-- | Doris  |
-- | Sofia  |
-- | Bruce  |
-- | Edward |
-- | Kelsey |
-- | Taylor |
-- | Kenny  |
-- | Luca   |
-- +--------+

-- Check the suspects' license plate
SELECT people.name FROM people
INNER JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE bakery_security_logs.year = 2021
    AND bakery_security_logs.month = 7
    AND bakery_security_logs.day = 28
    AND bakery_security_logs.hour = 10
    AND bakery_security_logs.minute >= 15
    AND bakery_security_logs.minute <= 25
    AND bakery_security_logs.activity = 'exit'
    AND people.name IN ('Doris', 'Sofia', 'Bruce', 'Edward', 'Kelsey', 'Taylor', 'Kenny', 'Luca');
-- +--------+
-- | Bruce  |
-- | Luca   |
-- | Sofia  |
-- | Kelsey |
-- +--------+

-- Check the suspects' account number
SELECT bank_accounts.account_number, people.name FROM bank_accounts
INNER JOIN people ON people.id = bank_accounts.person_id
WHERE people.name IN ('Bruce', 'Luca', 'Sofia', 'Kelsey');
-- +----------------+-------+
-- | 49610011       | Bruce |
-- | 28500762       | Luca  |
-- +----------------+-------+

-- Check who the theft is
SELECT people.name, people.phone_number FROM people
INNER JOIN bank_accounts ON bank_accounts.person_id = people.id
INNER JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
INNER JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE bank_accounts.account_number IN ('49610011', '28500762')
    AND atm_transactions.atm_location LIKE 'Leggett Street'
    AND atm_transactions.transaction_type = 'withdraw'
    AND atm_transactions.year = 2021
    AND atm_transactions.month = 7
    AND atm_transactions.day = 28
    AND phone_calls.year = 2021
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60;
-- +-------+----------------+
-- | Bruce | (367) 555-5533 |
-- +-------+----------------+
-- The theft is Bruce

-- Check who the accomplice is
SELECT people.name FROM people
INNER JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE phone_calls.caller = '(367) 555-5533'
    AND phone_calls.year = 2021
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60;
-- +-------+
-- | Robin |
-- +-------+
-- The accomplice is Robin