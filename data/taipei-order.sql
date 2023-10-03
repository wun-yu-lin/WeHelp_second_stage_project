
-- -----------------------------------------------------
-- Table `taipei_travel`.`booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `taipei_travel`.`booking` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `date` VARCHAR(100) NOT NULL,
  `time` VARCHAR(100) NOT NULL,
  `price` INT NOT NULL,
  `booking_status` INT NOT NULL DEFAULT 1,
  `user_id` BIGINT NOT NULL,
  `attraction_id` INT NOT NULL,
  `order_id` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`, `user_id`, `attraction_id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_booking_attraction1_idx` (`attraction_id` ASC) VISIBLE,
  INDEX `fk_booking_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_booking_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `taipei_travel`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_booking_attraction1`
    FOREIGN KEY (`attraction_id`)
    REFERENCES `taipei_travel`.`attraction` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `taipei_travel`.`order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `taipei_travel`.`order` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_price` DECIMAL(12,4) NOT NULL,
  `prime` VARCHAR(100) NOT NULL,
  `order_time` DATETIME NOT NULL DEFAULT current_timestamp,
  `status` INT NOT NULL DEFAULT 1,
  `number` VARCHAR(100) NULL,
  `contact_name` VARCHAR(255) NOT NULL,
  `contact_email` VARCHAR(255) NOT NULL,
  `contact_phone` VARCHAR(20) NOT NULL,
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `prime_UNIQUE` (`prime` ASC) VISIBLE,
  INDEX `number_idx` (`number` ASC) VISIBLE)
ENGINE = InnoDB;

