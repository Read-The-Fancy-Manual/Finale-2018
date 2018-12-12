CREATE DATABASE IF NOT EXISTS ProductionDebugging;

CREATE USER 'pdebugging'@'localhost' IDENTIFIED BY 'yo2yoh4xoomah2xee2Hij6aiSh6oajee4Eecie0thoh3Xeithi';
GRANT ALL PRIVILEGES ON * . * TO 'pdebugging'@'localhost';

USE ProductionDebugging;



CREATE TABLE IF NOT EXISTS ProductionDebugging.tbl_user (
    login VARCHAR(100),
    password VARCHAR(100)
);

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE sp_createUser (
    IN p_login VARCHAR(100),
    IN p_password VARCHAR(100)
)
BEGIN
    IF (select exists (select 1 from tbl_user where login = p_login)) THEN
        select 'Username exists!';
    ELSE
        START TRANSACTION;
        insert into tbl_user
        (
            login,
            password
        )
        values
        (
            p_login,
            p_password
        );
        ROLLBACK;
        select 'User creation has been disabled, changes have been canceled.';
    END IF;
END$$
DELIMITER ;
