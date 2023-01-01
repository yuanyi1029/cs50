-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Identify clues and insight on what happened on July 28 2021 on Humphrey Street. Interviews conducted on 3 witnesses that day
SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Identify testimonies from witnesses (Ruth, Eugene, Raymond) that talked about the bakery
-- Ruth: theif drove away from parking lot, in 10 minutes of the theft
-- Eugene: theif was at the ATM on Leggett Street withdrawing money
-- Raymond: theif talked to accomplice for <1 minute, planned to take earliest flight out of Fiftyville the next day, accomplice will purchase flight ticket
SELECT * FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- Identify Fiftyville airport id (8)
SELECT id FROM airports WHERE city = 'Fiftyville';

-- Identify the earlist flight away from Fiftyville
-- Earlist flight away from Fiftyville: Flight id 38, July 29 2021 8:20 a.m. From airport id 8 to airport id 4
SELECT * FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id LIKE (SELECT id FROM airports WHERE city = 'Fiftyville') ORDER BY hour LIMIT 1;

-- Identify which city the thief went to
-- The thief went to LaGuardia Airport, New York City
SELECT * FROM airports WHERE id = 4;

-- Look through ATM withdrawals ids on July 28 2021 Leggett street
SELECT id FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Identify the poeple who made withdrawals on Leggett street July 28 2021
SELECT name, atm_transactions.amount FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number WHERE atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw';

-- Identify the people on the flight to LaGuardia Airport from fiftyville
SELECT passengers.flight_id, name, passengers.passport_number, passengers.seat FROM people JOIN passengers ON people.passport_number = passengers.passport_number JOIN flights ON passengers.flight_id = flights.id WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.hour = 8 AND flights.minute = 20 ORDER BY passengers.passport_number;

-- Identify the people who left the bakery in 10 minutes
SELECT name, bakery_security_logs.hour, bakery_security_logs.minute FROM people JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate WHERE bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 AND bakery_security_logs.activity = 'exit' AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25 ORDER BY bakery_security_logs.minute;

-- Identify phonecalls under a minute
SELECT name, phone_calls.duration FROM people JOIN phone_calls ON people.phone_number = phone_calls.receiver WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60 ORDER BY phone_calls.duration;


-- Only Bruce appeared in all the suspect lists. the thief is Bruce, Bruce called Robin for about 45 seconds so the accomplice is Robin