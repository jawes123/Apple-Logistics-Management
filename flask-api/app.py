from flask import Flask, request, jsonify
from flask_cors import CORS
from db import Executer
import uuid
import os

app = Flask(__name__, static_folder='../client-app/build', static_url_path='/')
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/deliver', methods=['POST'])
def insert_order():
    username = request.form["username"]
    product_id = request.form["productName"]
    street_address = request.form["streetAddress"]
    zip_code = request.form["zipCode"]
    country = request.form["country"]
    state = request.form["state"]

    ex = Executer("shipping_db.sqlite")

    location_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    ex.insert_into("location",
                   (location_id,
                    street_address,
                    zip_code,
                    country,
                    state),
                   columns=("location_id",
                            "address",
                            "zip_code",
                            "country",
                            "state"))
    
    ex.insert_into("users",
                    (user_id,
                     username),
                    columns=None)

    try:
        ex.insert_into("orders",
                       (user_id,
                        location_id,
                        product_id),
                       columns=("user_id",
                                "location_id",
                                "product_id")
                       )

        ret_dict = {"status": 200,
                    "success": True,
                    "error": None}

    except:

        ex.delete_from_table("location",
                             "WHERE location_id = {}".format('"' + location_id + '"'))

        ret_dict = {"status": 500,
                    "success": False,
                    "error": "Username in use"}

    ex.commit()
    ex.close_connection()

    return jsonify(ret_dict)


@app.route('/api/logs', methods=['POST'])
def get_view():
    key = request.form["key"]
    ex = Executer("shipping_db.sqlite")

    if key.upper() == "MANAGER":
        data = ex.fetch_data("ADMIN_VIEW")[-1]
        columns = ["id", "username", "location_id", "product_id", "date_created"]
        data_list = []
        for i in data:
            data_list.append({columns[0]: i[0],
                              columns[1]: ex.list_user_from_id(i[1])[0][0],
                              columns[2]: ex.list_location_from_id(i[2])[0][0] + ", " + ex.list_location_from_id(i[2])[0][2] + " " + ex.list_location_from_id(i[2])[0][1],
                              columns[3]: i[3],
                              columns[4]: i[4]})

    elif key.upper() == "RECIPIENT":
        data = ex.fetch_data("User_View")[-1]
        columns = ["username", "product_id", "date_created"]
        data_list = []
        for i in data:
            data_list.append({columns[0]: ex.list_user_from_id(i[0])[0][0],
                              columns[1]: i[1],
                              columns[2]: i[2]})

    elif key.upper() == "SHIPPER":
        data = ex.fetch_data("Shipper_View")[-1]
        columns = ["location_id", "product_id", "date_created"]
        data_list = []
        for i in data:
            data_list.append({columns[0]: ex.list_location_from_id(i[0])[0][0] + ", " + ex.list_location_from_id(i[0])[0][2] + " " + ex.list_location_from_id(i[0])[0][1],
                              columns[1]: i[1],
                              columns[2]: i[2]})

    ex.commit()
    ex.close_connection()
    return jsonify(data_list)


@app.route("/api/inventory/add", methods=["POST"])
def insert_product():
    product_id = str(uuid.uuid4())
    product_category_id = request.form["category_id"] 
    product_model = request.form["model"]
    product_color = request.form["color"]
    product_size = request.form["size"]
    product_release = request.form["release"]

    ex = Executer("shipping_db.sqlite")

    product_category_id = (ex.list_category_from_name(product_category_id))[0]

    ex.insert_into("product",
                   (product_id,
                    product_category_id[0],
                    product_model,
                    product_color,
                    product_size,
                    product_release),
                   columns=None)

    ex.commit()
    ex.close_connection()

    return jsonify({"status": 200,
                    "success": True,
                    "error": None})


@app.route("/api/inventory/products", methods=["GET"])
def get_products():
    ex = Executer("shipping_db.sqlite")

    data = ex.fetch_data("product")
    modify = list(data[0])
    new = []
    for i in modify:
        temp = list(i)
        temp[1] = ex.list_category_from_pk(temp[1])[0]
        new.append(tuple(temp))
    data2 = tuple(new)

    ex.commit()
    ex.close_connection()

    return jsonify(data2)

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
