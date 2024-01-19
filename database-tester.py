import databaseHadith
from log import LOG


test = databaseHadith.DatabaseHadith(LOG)

conn = test.get_connection()
test.create_database(conn)

getTest = test.get_data(conn, "test_key")
print(getTest)
check_if_exists = test.is_data_exist(conn, "test_key")
print(check_if_exists)

test.insert_data(conn, "test_key", "test_blob")

getTest = test.get_data(conn, "test_key")
print(getTest)
check_if_exists = test.is_data_exist(conn, "test_key")
print(check_if_exists)

deleteResponse = test.delete_data(conn, "test_key")
print("deleteResponse")
print(deleteResponse)

getTest = test.get_data(conn, "test_key")
print(getTest)
check_if_exists = test.is_data_exist(conn, "test_key")
print(check_if_exists)