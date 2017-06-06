class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "flaskuser",
            "passwd": "flaskpassword",
            "db": "P1_Database"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getDataFromDatabase(self, tablename):
        #krijg alle data uit een tabel
        sqlQuery = "SELECT * FROM " + tablename
        
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataFromDatabaseWithCondition(self, tablename, columnname, voorwaarde):
        # krijg enkel de data waarvan de voorwaarde werd voldaan

        sqlQuery = "SELECT * FROM " + tablename + " WHERE " + columnname + " = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=voorwaarde)
        
        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setDataToDatabase(self, tablename, *values):
        # creëer een nieuwe rij,
        # let op! alle waarden die meegegeven worden moeten in dezelfde volgorde staan als de kolommen
        # ook moeten er evenveel waarden als kolommen meegegeven worden!

        # voorbeeld voeg gebruiker toe: setDataToDatabase("Gebruiker", "0", "voornaam", "naam", "voornaam.naam@iets.be", "wachtwoord", "geleende boeken")
        # merk op dat de tweede paramater en dus de eerste value genegeerd wordt bij een auto-increment

        sqlQuery = "INSERT INTO " + tablename + " () VALUES ({param1})"

        #lege lijst aanmaken
        newValuesList = []
        # elke value dat werd meegegeven moet omringd worden door single quotes
        for value in values:
            newValue = "\'" + value + "\'"
            newValuesList.append(newValue)

        # moet aan sql worden meegegeven als een string en niet als een list
        newValuesString = str(newValuesList).strip('[]')

        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=newValuesString)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def updateDataWithCondition(self, tablename, columnname, updatevalue, conditioncolumn, conditionvalue):
        # tablename = naam van tabel waar er iets moet veranderd worden
        # columname = naam van kolom waar er iets moet veranderd worden
        # updatevalue = nieuwe waarde die de oude moet vervangen
        # conditioncolumn = kolomnaam waar een voorwaarde aan verbonden is
        # conditionvalue = waarde van het veld in die kolom
        # voorbeeld naam aanpassen van gebruiker met ID=1: updateDataWithCondition("Gebruiker", "Naam", "Test", "GebruikerID", "1")
        sqlQuery = "UPDATE " + tablename + " SET " + columnname + " = \"" + updatevalue + "\" WHERE " + conditioncolumn + " = \"" + conditionvalue + "\""

        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()