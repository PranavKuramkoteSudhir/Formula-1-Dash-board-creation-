class F1Schema:
    def __init__(self, mysql_connector):
        command="CREATE SCHEMA IF NOT EXISTS `formula2`;"
        mysql_connector.execute_query(command)

        command="USE `formula2`;"
        mysql_connector.execute_query(command)
        command = "CREATE TABLE `circuits` ( `circuitId` INT NOT NULL, `circuitRef` VARCHAR(255) DEFAULT NULL, `alt` FLOAT DEFAULT NULL, `country` VARCHAR(255) DEFAULT NULL, `location` VARCHAR(255) DEFAULT NULL, `name` VARCHAR(255) DEFAULT NULL, PRIMARY KEY (`circuitId`)) ;"
        mysql_connector.execute_query(command)
        command ="CREATE TABLE `constructors` ( `constructorId` INT NOT NULL, `name` VARCHAR(255) DEFAULT NULL, `constructorRef` VARCHAR(255) DEFAULT NULL, `nationality` VARCHAR(255) DEFAULT NULL, PRIMARY KEY (`constructorId`)) ;"
        mysql_connector.execute_query(command)
        command="CREATE TABLE `drivers` (`driverId` INT NOT NULL, `number` INT DEFAULT NULL, `code` VARCHAR(255) DEFAULT NULL, `dob` DATE DEFAULT NULL, `forename` VARCHAR(255) DEFAULT NULL, `surname` VARCHAR(255) DEFAULT NULL, `nationality` VARCHAR(255) DEFAULT NULL, PRIMARY KEY (`driverId`) ) ;"
        mysql_connector.execute_query(command)
        command="CREATE TABLE `races` (  `raceId` INT NOT NULL,  `time` VARCHAR(255) DEFAULT NULL,  `date` DATE DEFAULT NULL,  `circuitId` INT NOT NULL,  `round` INT DEFAULT NULL,  `year` INT DEFAULT NULL,  PRIMARY KEY (`raceId`),  KEY `circuitId` (`circuitId`),  CONSTRAINT `races_ibfk_1` FOREIGN KEY (`circuitId`) REFERENCES `circuits` (`circuitId`)) ;"
        mysql_connector.execute_query(command)
        command="CREATE TABLE `lap_times` ( `raceId` INT NOT NULL, `driverId` INT NOT NULL, `lap` INT NOT NULL, `position` INT DEFAULT NULL, `time` VARCHAR(255) DEFAULT NULL, PRIMARY KEY (`raceId`, `driverId`, `lap`), KEY `driverId` (`driverId`), CONSTRAINT `lap_times_ibfk_1` FOREIGN KEY (`raceId`) REFERENCES `races` (`raceId`), CONSTRAINT `lap_times_ibfk_2` FOREIGN KEY (`driverId`) REFERENCES `drivers` (`driverId`) ) ;"
        mysql_connector.execute_query(command)
        command="CREATE TABLE `pit_stops` ( `raceId` INT NOT NULL, `driverId` INT NOT NULL, `lap` INT NOT NULL, `time` VARCHAR(255) DEFAULT NULL, `stop` INT DEFAULT NULL, `duration` VARCHAR(20) DEFAULT NULL, `milliseconds` INT DEFAULT NULL, PRIMARY KEY (`raceId`, `driverId`, `lap`), KEY `driverId` (`driverId`), CONSTRAINT `pit_stops_ibfk_1` FOREIGN KEY (`raceId`) REFERENCES `races` (`raceId`), CONSTRAINT `pit_stops_ibfk_2` FOREIGN KEY (`driverId`) REFERENCES `drivers` (`driverId`)) ;"
        mysql_connector.execute_query(command)
        command="CREATE TABLE `qualifying` (  `raceId` INT NOT NULL,  `driverId` INT NOT NULL,  `q3` VARCHAR(255) DEFAULT NULL,  `position` INT DEFAULT NULL,  `qualifyId` INT NOT NULL,  PRIMARY KEY (`raceId`, `driverId`),  KEY `driverId` (`driverId`),  CONSTRAINT `qualifying_ibfk_1` FOREIGN KEY (`raceId`) REFERENCES `races` (`raceId`),  CONSTRAINT `qualifying_ibfk_2` FOREIGN KEY (`driverId`) REFERENCES `drivers` (`driverId`));"
        mysql_connector.execute_query(command)
        command="CREATE TABLE `results` (  `resultId` INT NOT NULL,  `raceId` INT DEFAULT NULL,  `driverId` INT DEFAULT NULL,  `grid` INT DEFAULT NULL,  `constructorId` INT DEFAULT NULL,  `position` INT DEFAULT NULL,  `fastestLapSpeed` VARCHAR(255) DEFAULT NULL,  `fastestLapTime` VARCHAR(255) DEFAULT NULL,  `points` FLOAT DEFAULT NULL,  `laps` INT DEFAULT NULL,  PRIMARY KEY (`resultId`),  KEY `raceId` (`raceId`),  KEY `driverId` (`driverId`),  KEY `constructorId` (`constructorId`),  CONSTRAINT `results_ibfk_1` FOREIGN KEY (`raceId`) REFERENCES `races` (`raceId`),  CONSTRAINT `results_ibfk_2` FOREIGN KEY (`driverId`) REFERENCES `drivers` (`driverId`),  CONSTRAINT `results_ibfk_3` FOREIGN KEY (`constructorId`) REFERENCES `constructors` (`constructorId`)) ;"
        mysql_connector.execute_query(command)