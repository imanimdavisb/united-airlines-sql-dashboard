DROP TABLE IF EXISTS flight_operations;
CREATE TABLE flight_operations (
 flight_id INTEGER PRIMARY KEY,
 flight_date DATE NOT NULL,
 month TEXT NOT NULL,
 airline TEXT NOT NULL,
 origin_airport TEXT NOT NULL,
 destination_airport TEXT NOT NULL,
 scheduled_departure TEXT NOT NULL,
 departure_delay_minutes INTEGER NOT NULL,
 arrival_delay_minutes INTEGER NOT NULL,
 cancelled INTEGER NOT NULL,
 delay_reason TEXT NOT NULL,
 distance_miles INTEGER NOT NULL
);
