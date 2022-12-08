import sqlite3
import uuid


class Executer:

    def __init__(self, file_path):
        self.__conn = sqlite3.connect(file_path)
        self.__cursor = self.__conn.cursor()

    def insert_table(self,
                     table_name: str,
                     *args) -> None:
        execution_string = "CREATE TABLE IF NOT EXISTS " + table_name + "("

        for i in args:
            execution_string += i + ", "

        execution_string = execution_string[:-2] + ");"

        self.__cursor.execute(execution_string.upper())

    def list_tables(self) -> list:
        command = "SELECT name FROM sqlite_master WHERE type='table';"
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def list_category_from_pk(self, pk) -> list:
        command = "SELECT category FROM categories WHERE category_id='{}'".format(pk)
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def list_category_from_name(self, name) -> list:
        command = "SELECT CATEGORY_ID FROM CATEGORIES WHERE CATEGORY='{}'".format(name.upper())
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def list_user_from_id(self, id) -> list:
        command = "SELECT username FROM users WHERE user_id='{}'".format(id)
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def list_location_from_id(self, id) -> list:
        command = "SELECT address,zip_code,state FROM location WHERE location_id='{}'".format(id)
        self.__cursor.execute(command)
        return self.__cursor.fetchall()

    def insert_into(self,
                    table_name: str,
                    values: tuple,
                    columns=None):

        base_string = "INSERT INTO " + table_name

        if columns is not None:
            base_string += str(columns)
            if len(columns) == 1:
                base_string = base_string[:-2] + ")"

        if len(values) == 1:
            base_string += " VALUES" + " " + str(values)
            base_string = base_string[:-2] + ");"
        else:
            base_string += " VALUES" + " " + str(values) + ";"

        self.__cursor.execute(base_string.upper())

    def delete_from_table(self,
                          table_name: str,
                          *args):

        query = "DELETE FROM {}".format(table_name)

        for i in args:
            query += " " + i

        self.__cursor.execute(query.upper())

    def fetch_data(self,
                   table: str,
                   *args,
                   select_col=None,
                   ret_str=False):

        base_str = "SELECT"
        if select_col is None:
            base_str += " *"
        else:
            base_str += " "
            for i in select_col:
                base_str += i + ", "
            base_str = base_str[:-2]

        base_str += " FROM {}".format(table)

        for i in args:
            base_str += " " + i

        self.__cursor.execute(base_str.upper() + ";")

        if ret_str:
            return base_str.upper() + ";"
        else:
            return self.__cursor.fetchall(),

    def make_view(self,
                  view_name: str,
                  table: str,
                  *args,
                  select_col=None):

        create_str = "CREATE VIEW {} AS".format(view_name)

        base_str = self.fetch_data(table,
                                   *args,
                                   select_col=select_col,
                                   ret_str=True)

        full_str = create_str + " " + base_str

        self.__cursor.execute(full_str.upper())

    def close_connection(self):
        self.__conn.close()

    def commit(self):
        self.__conn.commit()


if __name__ == '__main__':
    executer = Executer("shipping_db.sqlite")

    command_list = ["location_id VARCHAR(36) PRIMARY KEY",
                    "address VARCHAR(50) NOT NULL",
                    "zip_code VARCHAR(10) NOT NULL",
                    "country VARCHAR(50) NOT NULL",
                    "state VARCHAR(2)",
                    "date_created default current_timestamp"]

    executer.insert_table("LOCATION", *command_list)

    command_list = ["role_key VARCHAR(30) PRIMARY KEY",
                    "description VARCHAR(50) NOT NULL",
                    "role_name VARCHAR(30) NOT NULL"]

    executer.insert_table("roles", *command_list)

    command_list = ["category_id VARCHAR(36) PRIMARY KEY",
                    "category VARCHAR(50) NOT NULL"]

    executer.insert_table("categories", *command_list)

    command_list = ["product_id VARCHAR(36)",
                    "category_id VARCHAR(36) NOT NULL",
                    "model VARCHAR(50) NOT NULL",
                    "color VARCHAR(50) NOT NULL",
                    "size INTEGER NOT NULL",
                    "release INTEGER NOT NULL",
                    "FOREIGN KEY (category_id) REFERENCES categories(category_id)"]

    executer.insert_table("product", *command_list)

    command_list = ["user_id VARCHAR(36) PRIMARY KEY",
                    "username VARCHAR(50) NOT NULL"]

    executer.insert_table("users", *command_list)

    command_list = ["order_id INTEGER PRIMARY KEY AUTOINCREMENT",
                    "user_id VARCHAR(50) NOT NULL",
                    "location_id VARCHAR(36) NOT NULL",
                    "product_id VARCHAR(36) NOT NULL",
                    "date_created default current_timestamp",
                    "FOREIGN KEY (product_id) REFERENCES product(product_id)",
                    "FOREIGN KEY (location_id) REFERENCES location(location_id)",
                    "FOREIGN KEY (user_id) REFERENCES users(user_id)"]

    executer.insert_table("orders", *command_list)

    print("Created {}, {}, {}, and {} tables".format("LOCATION",
                                                     "ROLES",
                                                     "PRODUCT",
                                                     "ORDERS"))

    # ---------------------------------------------------------------------------------------------

    location_1 = str(uuid.uuid4())
    location_2 = str(uuid.uuid4())
    location_3 = str(uuid.uuid4())

    executer.insert_into("location",
                         (location_1,
                          "1 Apple Park Way",
                          "95014",
                          "United States",
                          "CA"),
                         columns=("location_id",
                                  "address",
                                  "zip_code",
                                  "country",
                                  "state"))

    executer.insert_into("location",
                         (location_2,
                          "3261 Falls Creek Dr",
                          "95135",
                          "United States",
                          "CA"),
                         columns=("location_id",
                                  "address",
                                  "zip_code",
                                  "country",
                                  "state"))

    executer.insert_into("location",
                         (location_3,
                          "1 Washington Sq",
                          "95192",
                          "United States",
                          "CA"),
                         columns=("location_id",
                                  "address",
                                  "zip_code",
                                  "country",
                                  "state"))

    print("Inserted data into the {} table".format("LOCATION"))
# ---------------------------------------------------------------------------------------------
    category_1 = str(uuid.uuid4())
    category_2 = str(uuid.uuid4())
    category_3 = str(uuid.uuid4())

    executer.insert_into("categories",
                         (category_1,
                          "Phone"),
                         columns=None)

    executer.insert_into("categories",
                         (category_2,
                          "Laptop"),
                         columns=None)

    executer.insert_into("categories",
                         (category_3,
                          "Watch"),
                         columns=None)

    print("Inserted data into the {} table".format("Categories"))
    # ----------------------------------------------------------------------------------------------
    product_1 = str(uuid.uuid4())
    product_2 = str(uuid.uuid4())
    product_3 = str(uuid.uuid4())

    executer.insert_into("product",
                         (product_1,
                          category_1,
                          "iPhone 13",
                          "Grey",
                          6,
                          2021),
                         columns=None)

    executer.insert_into("product",
                         (product_2,
                          category_2,
                          "Macbook Pro",
                          "Silver",
                          13,
                          2019),
                         columns=None)

    executer.insert_into("product",
                         (product_3,
                          category_3,
                          "Series 5",
                          "Rose Gold",
                          2,
                          2018),
                         columns=None)

    print("Inserted data into the {} table".format("PRODUCT"))
    # ----------------------------------------------------------------------------------------------

    executer.insert_into("roles",
                         ("Admin", "access to all columns", "admin"),
                         columns=None)

    executer.insert_into("roles",
                         ("Shipper", "access to order and address", "ship"),
                         columns=None)

    executer.insert_into("roles",
                         ("Recipient", "access to order and username", "recipient"),
                         columns=None)

    print("Inserted data into the {} table".format("ROLES"))
    # ----------------------------------------------------------------------------------------------

    user_1 = str(uuid.uuid4())
    user_2 = str(uuid.uuid4())
    user_3 = str(uuid.uuid4())

    executer.insert_into("users",
                         (user_1,
                          "Karan Gandhi"),
                         columns=None)

    executer.insert_into("users",
                         (user_2,
                          "James Yu"),
                         columns=None)

    executer.insert_into("users",
                         (user_3,
                          "Sunny Chen"),
                         columns=None)

    print("Inserted data into the {} table".format("Users"))
    
    # ----------------------------------------------------------------------------------------------

    executer.insert_into("orders",
                         (user_1,
                          location_1,
                          product_1),
                         columns=("user_id",
                                  "location_id",
                                  "product_id"))

    executer.insert_into("orders",
                         (user_2,
                          location_2,
                          product_2),
                         columns=("user_id",
                                  "location_id",
                                  "product_id"))

    executer.insert_into("orders",
                         (user_3,
                          location_3,
                          product_3),
                         columns=("user_id",
                                  "location_id",
                                  "product_id"))

    print("Inserted data into the {} table".format("ORDERS"))
    # --------------------------------------------------------------------------------------------------------
    executer.make_view("Admin_View",
                       "orders",
                       select_col=("order_id",
                                   "user_id",
                                   "location_id",
                                   "product_id",
                                   "date_created"))

    executer.make_view("User_View",
                       "orders",
                       select_col=("user_id",
                                   "product_id",
                                   "date_created"))

    executer.make_view("Shipper_View",
                       "orders",
                       select_col=("location_id",
                                   "product_id",
                                   "date_created"))

    executer.commit()
    executer.close_connection()

    print("Created the {}, {}, and {} views".format("ADMIN",
                                                    "USER",
                                                    "SHIPPER"))

