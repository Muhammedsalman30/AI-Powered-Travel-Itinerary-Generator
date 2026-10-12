import database

database.create_table()

print("Database connected successfully!")

print("Available functions:")

print(hasattr(database, "create_table"))
print(hasattr(database, "add_customer"))
print(hasattr(database, "get_customers"))
print(hasattr(database, "search_customer"))
print(hasattr(database, "update_customer"))
print(hasattr(database, "delete_customer"))

print("Database test completed!")