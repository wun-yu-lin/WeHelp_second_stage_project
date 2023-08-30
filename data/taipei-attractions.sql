-- MySQL Script generated by MySQL Workbench
-- Thu Aug 31 01:29:14 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema taipei_travel
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema taipei_travel
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `taipei_travel` DEFAULT CHARACTER SET utf8 ;
USE `taipei_travel` ;

-- -----------------------------------------------------
-- Table `taipei_travel`.`mrt`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `taipei_travel`.`mrt` (
  `mrt_id` INT NOT NULL AUTO_INCREMENT,
  `mrt` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`mrt_id`),
  UNIQUE INDEX `mrt_id_UNIQUE` (`mrt_id` ASC) VISIBLE,
  UNIQUE INDEX `mrt_UNIQUE` (`mrt` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `taipei_travel`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `taipei_travel`.`category` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(255) NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `taipei_travel`.`attraction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `taipei_travel`.`attraction` (
  `attraction_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `transport` VARCHAR(255) NOT NULL,
  `mrt_id` INT NOT NULL,
  `lat` DOUBLE NOT NULL,
  `lng` DOUBLE NOT NULL,
  `category_id` INT NOT NULL,
  `description` VARCHAR(1000) NOT NULL,
  PRIMARY KEY (`attraction_id`),
  INDEX `fk_attractions_mrt_idx` (`mrt_id` ASC) VISIBLE,
  INDEX `fk_attractions_category1_idx` (`category_id` ASC) VISIBLE,
  UNIQUE INDEX `attraction_id_UNIQUE` (`attraction_id` ASC) VISIBLE,
  CONSTRAINT `fk_attractions_mrt`
    FOREIGN KEY (`mrt_id`)
    REFERENCES `taipei_travel`.`mrt` (`mrt_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_attractions_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `taipei_travel`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `taipei_travel`.`image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `taipei_travel`.`image` (
  `image_id` INT NOT NULL AUTO_INCREMENT,
  `src` VARCHAR(255) NOT NULL,
  `attraction_id` INT NOT NULL,
  PRIMARY KEY (`image_id`, `attraction_id`),
  UNIQUE INDEX `file_id_UNIQUE` (`image_id` ASC) VISIBLE,
  INDEX `fk_image_attractions1_idx` (`attraction_id` ASC) VISIBLE,
  CONSTRAINT `fk_image_attractions1`
    FOREIGN KEY (`attraction_id`)
    REFERENCES `taipei_travel`.`attraction` (`attraction_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `taipei_travel`.`attraction_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `taipei_travel`.`attraction_info` (
  `attraction_id` INT NOT NULL,
  `attraction_info_id` INT NOT NULL AUTO_INCREMENT,
  `avEnd` VARCHAR(45) NULL,
  `idpt` VARCHAR(45) NULL,
  `POI` VARCHAR(45) NULL,
  `memo_time` VARCHAR(45) NULL,
  `avBegin` VARCHAR(45) NULL,
  `ref_wp` VARCHAR(45) NULL,
  `direction` VARCHAR(255) NULL,
  `rate` INT NULL,
  PRIMARY KEY (`attraction_info_id`),
  CONSTRAINT `fk_attraction_other_info_attractions1`
    FOREIGN KEY (`attraction_id`)
    REFERENCES `taipei_travel`.`attraction` (`attraction_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
