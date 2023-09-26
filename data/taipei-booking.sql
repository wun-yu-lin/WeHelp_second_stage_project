

-- -----------------------------------------------------
-- Table `taipei_travel`.`booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `taipei_travel`.`booking` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `date` VARCHAR(100) NOT NULL,
  `time` VARCHAR(100) NOT NULL,
  `price` INT NOT NULL,
  `booking_status` INT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `attraction_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`, `attraction_id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_booking_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_booking_attraction1_idx` (`attraction_id` ASC) VISIBLE,
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

