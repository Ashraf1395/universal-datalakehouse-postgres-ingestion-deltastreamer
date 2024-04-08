from faker import Faker
import pandas as pd
import random

fake = Faker()

# Generate fake data for customers
def generate_customer_data(num_customers):
    customers = []
    for _ in range(num_customers):
        customer = {
            'customer_id': fake.uuid4(),
            'customer_name': fake.name(),
            'customer_address': fake.street_address(),
            'customer_city': fake.city(),
            'customer_state': fake.state(),
            'customer_zip_code': fake.zipcode(),
            'customer_contact_number': fake.phone_number(),
            'customer_email': fake.email()
        }
        customers.append(customer)
    return customers

# Generate fake data for orders
def generate_order_data(num_orders, customers):
    orders = []
    for _ in range(num_orders):
        customer = random.choice(customers)
        order = {
            'order_id': fake.uuid4(),
            'customer_id': customer['customer_id'],
            'order_date': fake.date_time_between(start_date='-30d', end_date='now'),
            'delivery_date': fake.date_time_between(start_date='now', end_date='+30d'),
            'order_status': random.choice(['Pending', 'In Progress', 'Completed']),
            'order_address': customer['customer_address'],
            'order_city': customer['customer_city'],
            'order_state': customer['customer_state'],
            'order_zip_code': customer['customer_zip_code'],
            'item_description': fake.word(),
            'item_quantity': random.randint(1, 10),
            'item_weight': random.uniform(0.1, 10.0)
        }
        orders.append(order)
    return orders

# Generate fake data for drivers
def generate_driver_data(num_drivers):
    drivers = []
    for _ in range(num_drivers):
        driver = {
            'driver_id': fake.uuid4(),
            'driver_name': fake.name(),
            'driver_contact_number': fake.phone_number(),
            'driver_license_number': fake.random_number(digits=10),
            'vehicle_id': fake.random_number(digits=6),
            'vehicle_type': random.choice(['Car', 'Truck', 'Van']),
            'vehicle_registration_number': fake.random_number(digits=8),
            'driver_status': random.choice(['Available', 'Busy', 'Offline']),
            'current_location_latitude': fake.latitude(),
            'current_location_longitude': fake.longitude()
        }
        drivers.append(driver)
    return drivers

# Generate fake data for assignments
def generate_assignment_data(num_assignments, orders, drivers):
    assignments = []
    for _ in range(num_assignments):
        order = random.choice(orders)
        driver = random.choice(drivers)
        assignment = {
            'assignment_id': fake.uuid4(),
            'order_id': order['order_id'],
            'driver_id': driver['driver_id'],
            'assigned_date': fake.date_time_between(start_date='-1d', end_date='now'),
            'assigned_status': random.choice(['Pending', 'In Progress', 'Completed']),
            'assigned_address': order['order_address'],
            'assigned_city': order['order_city'],
            'assigned_state': order['order_state'],
            'assigned_zip_code': order['order_zip_code']
        }
        assignments.append(assignment)
    return assignments

# Generate fake data
num_customers = 10
num_orders = 20
num_drivers = 5
num_assignments = 15

customers = generate_customer_data(num_customers)
orders = generate_order_data(num_orders, customers)
drivers = generate_driver_data(num_drivers)
assignments = generate_assignment_data(num_assignments, orders, drivers)

# Create DataFrames
customers_df = pd.DataFrame(customers)
orders_df = pd.DataFrame(orders)
drivers_df = pd.DataFrame(drivers)
assignments_df = pd.DataFrame(assignments)

# Save DataFrames to CSV files
customers_df.to_csv('data/customers.csv', index=False)
orders_df.to_csv('data/orders.csv', index=False)
drivers_df.to_csv('data/drivers.csv', index=False)
assignments_df.to_csv('data/assignments.csv', index=False)



import psycopg2
from psycopg2 import sql
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="metastore",
    user="hive",
    password="hive",
    host="metastore_db",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Function to create table in PostgreSQL and import data
def import_csv_to_postgres(csv_file, table_name):
    # Load CSV data into pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Drop existing table if it exists
    drop_table_query = sql.SQL('DROP TABLE IF EXISTS {}').format(sql.Identifier(table_name))
    cur.execute(drop_table_query)
    
    # Create table in PostgreSQL
    create_table_query = sql.SQL('''
        CREATE TABLE IF NOT EXISTS {} (
            {}
        )
    ''').format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(sql.Identifier(column.lower()) + sql.SQL(' VARCHAR') for column in df.columns)
    )
    cur.execute(create_table_query)

    # Import data into PostgreSQL
    with open(csv_file, 'r') as f:
        next(f)  # Skip the header
        cur.copy_from(f, table_name, sep=',')
    
    conn.commit()
    print(f"Data imported into PostgreSQL table '{table_name}'.")

# Import data into PostgreSQL tables
import_csv_to_postgres('data/customers.csv', 'customers')
import_csv_to_postgres('data/orders.csv', 'orders')
import_csv_to_postgres('data/drivers.csv', 'drivers')
import_csv_to_postgres('data/assignments.csv', 'assignments')

# Close the cursor and connection
cur.close()
conn.close()
