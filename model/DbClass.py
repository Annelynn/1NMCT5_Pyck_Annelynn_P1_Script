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
        #get all data from table
        sqlQuery = "SELECT * FROM " + tablename

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        return result

    def getDataFromDatabaseWithCondition(self, tablename, columnname, condition):
        # receive data only when condition is fulfilled

        sqlQuery = "SELECT * FROM " + tablename + " WHERE " + columnname + " = '{param1}'"

        # combine query and parameter
        sqlCommand = sqlQuery.format(param1=condition)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        return result

    def setDataToDatabase(self, tablename, *values):
        # create new row
        # attention! all values need to be in the same order as the columns
        # attention2! the number of values should match the number of columns

        #e.g. add user: setDataToDatabase("User", "0", "firstName", "name", "firstName.name@something.com", "password", "borrowedBooks")
        # notice how parameters added to a column with an auto-increment do not get added to the table

        sqlQuery = "INSERT INTO " + tablename + " () VALUES ({param1})"

        #create empty list
        newValuesList = []

        # every value should be surrounded with single quotes
        for value in values:
            newValue = "\'" + value + "\'"
            newValuesList.append(newValue)

        # convert list to string with commas between different values
        newValuesString = str(newValuesList).strip('[]')

        # combine query and parameter
        sqlCommand = sqlQuery.format(param1=newValuesString)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()

    def updateDataWithCondition(self, tablename, columnname, updatevalue, conditioncolumn, conditionvalue):
        # tablename = name of table where something needs to be changed
        # columname = name of column where something needs to be changed
        # updatevalue = new value to replace old one
        # conditioncolumn = columnname where the condition applies
        # conditionvalue = value of condition
        # e.g. edit name of user with ID=1: updateDataWithCondition("User", "Name", "Test", "userID", "1")
        sqlQuery = "UPDATE " + tablename + " SET " + columnname + " = \"" + updatevalue + "\" WHERE " + conditioncolumn + " = \"" + conditionvalue + "\""

        self.__cursor.execute(sqlQuery)
        self.__connection.commit()

    # if cursor would be closed in every function, only one function can be executed on one instance
    def closeCursor(self):
        self.__cursor.close()