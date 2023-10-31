-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema thinkerIn$thinker
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `thinkerIn$thinker` DEFAULT CHARACTER SET utf8 ;
USE `thinkerIn$thinker` ;

-- -----------------------------------------------------
-- Table `thinkerIn$thinker`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`user` (
  `iduser`  INT NOT  NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `phone` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(256) NULL DEFAULT NULL,
  `code` VARCHAR(256) NULL DEFAULT NULL,
  `auth` VARCHAR(45) NULL DEFAULT 0,
  `create_at` TIMESTAMP NULL DEFAULT current_timestamp,
  PRIMARY KEY (`iduser`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `thinkerIn$thinker`.`quiz`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`quiz` (
  `num` VARCHAR(5) NOT NULL,
  `question` VARCHAR(300) NULL,
  `q_text` VARCHAR(2000) NULL,
  `c1` VARCHAR(100) NULL,
  `c2` VARCHAR(100) NULL,
  `c3` VARCHAR(100) NULL,
  `c4` VARCHAR(100) NULL,
  `c5` VARCHAR(100) NULL,
  `answer` VARCHAR(100) NULL,
  `score` VARCHAR(3) NULL,
  `cat` VARCHAR(45) NULL,
  PRIMARY KEY (`num`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thinkerIn$thinker`.`info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`info` (
  `user_iduser` INT NOT NULL,
  `sex` VARCHAR(45) NULL,
  `age` VARCHAR(45) NULL,
  `edu` VARCHAR(45) NULL,
  `location` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_iduser`),
  INDEX `fk_survey_user_idx` (`user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_survey_user`
    FOREIGN KEY (`user_iduser`)
    REFERENCES `thinkerIn$thinker`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thinkerIn$thinker`.`result`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`result` (
  `user_iduser` INT NOT NULL,
  `q1` VARCHAR(3) NOT NULL,
  `q2` VARCHAR(3) NOT NULL,
  `q3` VARCHAR(3) NOT NULL,
  `q4` VARCHAR(3) NOT NULL,
  `q5` VARCHAR(3) NOT NULL,
  `q6` VARCHAR(3) NOT NULL,
  `q7` VARCHAR(3) NOT NULL,
  `q8` VARCHAR(3) NOT NULL,
  `q9` VARCHAR(3) NOT NULL,
  `q10` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`user_iduser`),
  INDEX `fk_result_user1_idx` (`user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_result_user10`
    FOREIGN KEY (`user_iduser`)
    REFERENCES `thinkerIn$thinker`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thinkerIn$thinker`.`book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`book` (
  `bookid` INT NOT NULL,
  `title` VARCHAR(45) NULL,
  `author` VARCHAR(45) NULL,
  `publish` VARCHAR(45) NULL,
  `year` VARCHAR(45) NULL,
  `category` VARCHAR(45) NULL,
  PRIMARY KEY (`bookid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thinkerIn$thinker`.`recg_book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`recg_book` (
  `book_bookid` INT NOT NULL,
  `user_iduser` INT NOT NULL,
  PRIMARY KEY (`book_bookid`, `user_iduser`),
  INDEX `fk_recg_book_user1_idx` (`user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_recg_book_book1`
    FOREIGN KEY (`book_bookid`)
    REFERENCES `thinkerIn$thinker`.`book` (`bookid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_recg_book_user1`
    FOREIGN KEY (`user_iduser`)
    REFERENCES `thinkerIn$thinker`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



-- -- -----------------------------------------------------
-- -- Table `thinkerIn$thinker`.`noti`
-- -- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`noti` (
-- )
-- ENGINE = InnoDB;


-- -- -----------------------------------------------------
-- -- Table `thinkerIn$thinker`.`event`
-- -- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`event` (
-- )
-- ENGINE = InnoDB;


-- -- -----------------------------------------------------
-- -- Table `thinkerIn$thinker`.`qna`
-- -- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS `thinkerIn$thinker`.`qna` (
-- )
-- ENGINE = InnoDB;




