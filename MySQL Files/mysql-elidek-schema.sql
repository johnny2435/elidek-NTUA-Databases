SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS elidek;
CREATE SCHEMA elidek;
USE elidek;

CREATE TABLE project (
	project_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
    funding_amount INT UNSIGNED NOT NULL 
    CHECK (funding_amount >= 100000 AND funding_amount <= 1000000),
    start_date DATE DEFAULT NULL,
    end_date DATE DEFAULT NULL 
    CHECK (end_date is NULL OR (DATEDIFF(end_date, start_date) >= 365 AND DATEDIFF(end_date, start_date) <= 1460)),
    executive_id INT UNSIGNED NOT NULL,
    programme_id INT UNSIGNED NOT NULL,
    supervisor_researcher_id INT UNSIGNED NOT NULL,
    organisation_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (project_id),
    CONSTRAINT fk_executive_id FOREIGN KEY (executive_id) REFERENCES executive (executive_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_programme_id FOREIGN KEY (programme_id) REFERENCES programme (programme_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_supervisor_researcher_id FOREIGN KEY (supervisor_researcher_id) REFERENCES researcher (researcher_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_organisation_id FOREIGN KEY (organisation_id) REFERENCES organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

ALTER TABLE project
ADD duration INT AS (DATEDIFF(end_date, start_date));

CREATE INDEX idx_date on project (start_date);
CREATE INDEX idx_duration on project (duration);

CREATE TABLE researcher (
	researcher_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(45) NOT NULL,
	last_name VARCHAR(45) NOT NULL,
    birth_date DATE NOT NULL,
    sex ENUM('FEMALE', 'MALE'),
    employee_organisation_id INT UNSIGNED NOT NULL,
    employee_date DATE NOT NULL, ###########################################
    PRIMARY KEY (researcher_id),
    CONSTRAINT fk_employee_organisation_id FOREIGN KEY (employee_organisation_id) REFERENCES organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

#ALTER TABLE researcher
#ADD age INT AS (DATEDIFF('2022-06-15', birth_date));

CREATE INDEX idx_birth_date on researcher (birth_date);

CREATE TABLE executive (
	executive_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(90) NOT NULL,
    PRIMARY KEY (executive_id)
);

CREATE INDEX idx_executive on executive (full_name);

CREATE TABLE works_on (
	project_id INT UNSIGNED NOT NULL,
    researcher_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (project_id, researcher_id),
    CONSTRAINT fk_works_on_project_id FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_works_on_researcher_id FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE evaluates (
	project_id INT UNSIGNED NOT NULL,
    researcher_id INT UNSIGNED NOT NULL,
    grade INT UNSIGNED NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (project_id, researcher_id),
    CONSTRAINT fk_evaluates_project_id FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_evaluates_researcher_id FOREIGN KEY (researcher_id) REFERENCES researcher (researcher_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE programme (
	programme_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(90) NOT NULL,
    department VARCHAR(255) NOT NULL,
    PRIMARY KEY (programme_id)
);

CREATE TABLE science_field (
	science_field_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (science_field_id)
);

CREATE TABLE project_science_field (
	project_id INT UNSIGNED NOT NULL,
    science_field_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (project_id, science_field_id),
    ###################################################
    CONSTRAINT fk_project_science_field_project_id FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_project_science_field_science_field_id FOREIGN KEY (science_field_id) REFERENCES science_field (science_field_id) ON DELETE RESTRICT ON UPDATE CASCADE
);



CREATE TABLE organisation (
	organisation_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    abbreviation VARCHAR(45) NOT NULL,
    postal_address VARCHAR(10) NOT NULL,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(90) NOT NULL,
    PRIMARY KEY (organisation_id)
);

CREATE TABLE company (
	organisation_id INT UNSIGNED NOT NULL,
    own_budget INT UNSIGNED NOT NULL,
    PRIMARY KEY (organisation_id),
    CONSTRAINT fk_company_organisation_id FOREIGN KEY (organisation_id) REFERENCES organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE university (
	organisation_id INT UNSIGNED NOT NULL,
    ministry_budget INT UNSIGNED NOT NULL,
    PRIMARY KEY (organisation_id),
    CONSTRAINT fk_university_organisation_id FOREIGN KEY (organisation_id) REFERENCES organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE research_centre (
	organisation_id INT UNSIGNED NOT NULL,
    ministry_budget INT UNSIGNED NOT NULL, ######################################
	private_budget INT UNSIGNED NOT NULL, ######################################
    PRIMARY KEY (organisation_id),
    CONSTRAINT fk_research_centre_organisation_id FOREIGN KEY (organisation_id) REFERENCES organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE deliverable (
	deliverable_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
	date DATE NOT NULL,
    project_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (deliverable_id),
    CONSTRAINT fk_deliverable_project_id FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE phone_number (
	organisation_id INT UNSIGNED NOT NULL,
    number VARCHAR(20) NOT NULL,
    PRIMARY KEY (organisation_id, number),
    CONSTRAINT fk_phone_number_organisation_id FOREIGN KEY (organisation_id) REFERENCES organisation (organisation_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE VIEW project_researcher_view AS
SELECT p.title, r.first_name, r.last_name 
FROM project p join works_on w on p.project_id = w.project_id 
join researcher r on r.researcher_id = w.researcher_id;

CREATE VIEW org_university_view AS
SELECT o.name 
FROM organisation o join university u on u.organisation_id = o.organisation_id;