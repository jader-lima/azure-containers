CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY,
    department TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id INT PRIMARY KEY,
    jobs TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hired_employees (
    id INT PRIMARY KEY,
    name TEXT,
    datetime TEXT,
    department_id INT,
    job_id INT
);

ALTER TABLE hired_employees
ADD CONSTRAINT fk_department_id
FOREIGN KEY (department_id) REFERENCES departments(id);

ALTER TABLE hired_employees
ADD CONSTRAINT fk_jobs_id
FOREIGN KEY (job_id) REFERENCES jobs(id);