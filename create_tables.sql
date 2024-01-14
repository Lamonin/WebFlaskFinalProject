CREATE TABLE IF NOT EXISTS brand (
    brand_id INTEGER PRIMARY KEY,
    brand_name TEXT
);

CREATE TABLE IF NOT EXISTS model (
    model_id INTEGER PRIMARY KEY,
    brand_id INTEGER,
    model_name TEXT,
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
);

CREATE TABLE IF NOT EXISTS color (
    color_id INTEGER PRIMARY KEY,
    color_name TEXT
);

CREATE TABLE IF NOT EXISTS defect (
    defect_id INTEGER PRIMARY KEY,
    defect_name TEXT,
    cost INTEGER
);

CREATE TABLE IF NOT EXISTS car_defect (
    car_defect_id INTEGER PRIMARY KEY,
    car_id INTEGER,
    defect_id INTEGER,
    FOREIGN KEY (car_id) REFERENCES car(car_id),
    FOREIGN KEY (defect_id) REFERENCES defect(defect_id)
);

CREATE TABLE IF NOT EXISTS car (
    car_id INTEGER PRIMARY KEY,
    model_id INTEGER,
    color_id INTEGER,
    year_of_manufacture INTEGER,
    license_plate TEXT,
    FOREIGN KEY (model_id) REFERENCES MODEL(model_id),
    FOREIGN KEY (color_id) REFERENCES color(color_id)
);

CREATE TABLE IF NOT EXISTS client (
    client_id INTEGER PRIMARY KEY,
    full_name TEXT,
    phone_number TEXT,
    driver_license_number TEXT,
    driver_experience INTEGER
);

CREATE TABLE IF NOT EXISTS rental_contract (
    rental_contract_id INTEGER PRIMARY KEY,
    car_id INTEGER,
    client_id INTEGER,
    rental_start_date DATE,
    rental_end_date DATE,
    total_cost INTEGER,
    fine_amount INTEGER,
    FOREIGN KEY (client_id) REFERENCES client(client_id),
    FOREIGN KEY (car_id) REFERENCES car(car_id)
);
