from flask import Flask, request, jsonify,render_template
from flask_restful import Api, Resource
import psycopg2

app = Flask(__name__)
api = Api(app)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="metastore",
    user="hive",
    password="hive",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Define routes for frontend pages
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/customers')
# def customers():
#     return render_template('customers.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/drivers')
def drivers():
    return render_template('drivers.html')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')



# Define a Resource for handling CRUD operations on the customers table
class CustomersResource(Resource):
    def get(self):
        # Retrieve all customers from the database
        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()
        print(customers)
        return jsonify(customers)

    def post(self):
        # Create a new customer
        data = request.json
        query = "INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            data['customer_id'], data['customer_name'], data['customer_address'],
            data['customer_city'], data['customer_state'], data['customer_zip_code'],
            data['customer_contact_number'], data['customer_email']
        )
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Customer created successfully"}), 201

# Define a Resource for handling CRUD operations on the orders table
class OrdersResource(Resource):
    def get(self):
        # Retrieve all orders from the database
        cur.execute("SELECT * FROM orders")
        orders = cur.fetchall()
        return jsonify(orders)

    def post(self):
        # Create a new order
        data = request.json
        query = "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            data['order_id'], data['customer_id'], data['order_date'], data['delivery_date'],
            data['order_status'], data['order_address'], data['order_city'], data['order_state'],
            data['order_zip_code'], data['item_description'], data['item_quantity'], data['item_weight']
        )
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Order created successfully"}), 201

# Define a Resource for handling CRUD operations on the drivers table
class DriversResource(Resource):
    def get(self):
        # Retrieve all drivers from the database
        cur.execute("SELECT * FROM drivers")
        drivers = cur.fetchall()
        return jsonify(drivers)

    def post(self):
        # Create a new driver
        data = request.json
        query = "INSERT INTO drivers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            data['driver_id'], data['driver_name'], data['driver_contact_number'],
            data['driver_license_number'], data['vehicle_id'], data['vehicle_type'],
            data['vehicle_registration_number'], data['driver_status'], data['current_location_latitude'],
            data['current_location_longitude']
        )
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Driver created successfully"}), 201

# Define a Resource for handling CRUD operations on the assignments table
class AssignmentsResource(Resource):
    def get(self):
        # Retrieve all assignments from the database
        cur.execute("SELECT * FROM assignments")
        assignments = cur.fetchall()
        return jsonify(assignments)

    def post(self):
        # Create a new assignment
        data = request.json
        query = "INSERT INTO assignments VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            data['assignment_id'], data['order_id'], data['driver_id'], data['assigned_date'],
            data['assigned_status'], data['assigned_address'], data['assigned_city'],
            data['assigned_state'], data['assigned_zip_code']
        )
        cur.execute(query, values)
        conn.commit()
        return jsonify({"message": "Assignment created successfully"}), 201

# Define routes
api.add_resource(CustomersResource, '/customers')
api.add_resource(OrdersResource, '/app/orders')
api.add_resource(DriversResource, '/app/drivers')
api.add_resource(AssignmentsResource, '/app/assignments')

if __name__ == '__main__':
    app.run(debug=True)
