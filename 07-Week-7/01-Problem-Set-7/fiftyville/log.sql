-- Keep a log of any SQL queries you execute as you solve the mystery.

-- The theft took place on July 28, 2023
-- It took place on Humphrey Street

-- Question to answer:
-- Who the thief is
-- What city the thief escaped to
-- Who the thief’s accomplice is who helped them escape

-- Find crime scene description from reports
SELECT description FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28 AND street = "Humphrey Street";

-- Analysis of the crime scene description:
-- Theft of the CS50 duck took place at 10:15am
-- At the Humphrey Street BAKERY
-- Interviews with THREE witnesses who were present at the time
-- Each of their interview transcripts mentions the bakery

-- Find interview transcripts in which the bakery is mentioned
SELECT transcript FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

-- Key information from the interview transcripts:
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away
-- ATM on Leggett Street, the thief there withdrawing some money
-- Phone call for less than a minute
-- I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow (July 29, 2023)
-- The thief then asked the person on the other end of the phone to purchase the flight ticket

-- The theft took place on July 28, 2023 at 10:15am
-- Look for cars that left the parking lot sometime within ten minutes of the theft (10:25am) from bakery security logs

-- THIS PEOPLE WERE IN THE BAKERY
-- Find information about AMT on Leggett Street, transaction_type = withdraw
SELECT DISTINCT p.name AS "Thief's name", call_receiver.name AS "Call receiver", a.city AS "Departure", ad.city AS "Destination" FROM atm_transactions AS atm_tr
JOIN bank_accounts AS b_acc ON atm_tr.account_number = b_acc.account_number -- All bank accounts of wanted ATM transactions
JOIN people AS p ON b_acc.person_id = p.id -- All people to whom belong the bank acoounts
JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate -- All cars that were in the bakery parking lot
JOIN phone_calls AS pc ON p.phone_number = pc.caller -- Phone calls for less than a minute
JOIN people AS call_receiver ON pc.receiver = call_receiver.phone_number
JOIN passengers AS ps ON p.passport_number = ps.passport_number -- Find passinger with this passport number
JOIN flights AS f ON ps.flight_id = f.id -- Flight out of Fiftyville tomorrow (July 29, 2023)
JOIN airports AS a ON f.origin_airport_id = a.id -- From Fiftyville Airport
JOIN airports AS ad ON f.destination_airport_id = ad.id -- Desctination Airport
WHERE atm_tr.year = 2023 AND atm_tr.month = 7 AND atm_tr.day = 28 AND atm_tr.atm_location = "Leggett Street" AND transaction_type = "withdraw" AND bsl.hour = 10 AND (bsl.minute BETWEEN (15) AND (25)) AND pc.duration < 60 AND f.day = 29 AND a.city = "Fiftyville"
ORDER BY f.hour ASC
LIMIT 1

-- Littering took place at 16:36
-- No known witnesses
