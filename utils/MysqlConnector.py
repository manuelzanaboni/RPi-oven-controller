import os
import mysql.connector

class MysqlConnector:
    def __init__(self):
        
        self.user = os.environ.get("MYSQL_USER")
        self.password = os.environ.get("MYSQL_PSW")
        self.host = os.environ.get("MYSQL_HOST")
        self.database = os.environ.get("MYSQL_DATABASE")
        
    def create_table(self):
        cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)

        table = (
            "CREATE TABLE IF NOT EXISTS `oven` ("
            "  `id` int NOT NULL AUTO_INCREMENT,"
            "  `oven_temp` float NOT NULL,"
            "  `floor_temp` float NOT NULL,"
            "  `puffer_temp` float NOT NULL,"
            "  `fumes_temp` float NOT NULL,"
            "  `delta_press_oven` float NOT NULL,"
            "  `delta_press_gas` float NOT NULL,"
            "  `set_point` int NOT NULL,"
            "  `burner_status` tinyint(1) NOT NULL,"
            "  `resistance_status` tinyint(1) NOT NULL,"
            "  `wifi_signal` int NOT NULL,"
            "  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB")

        cursor = cnx.cursor()
        cursor.execute(table)
        cnx.commit()
        cursor.close()
        cnx.close()
        
    def insert_data(self, data):        
        cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
        

        insert_string = ("INSERT INTO oven "
                       "(oven_temp, floor_temp, puffer_temp, fumes_temp, delta_press_oven, delta_press_gas, set_point, burner_status, resistance_status, wifi_signal)"
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        cursor = cnx.cursor()
        cursor.execute(insert_string, data)
        print(cursor.lastrowid)
        cnx.commit()
        cursor.close()









