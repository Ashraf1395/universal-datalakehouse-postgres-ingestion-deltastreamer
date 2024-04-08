from faker import Faker
import pandas as pd
import random

fake = Faker()

# Generate fake data for customers
def generate_customer_data(num_customers):
    customers = []
    for _ in range(num_customers):
        customer = {
            'Customer ID': fake.uuid4(),
            'Customer Name': fake.name(),
            'Customer Address': fake.street_address(),
            'Customer City': fake.city(),
            'Customer State': fake.state(),
            'Customer Zip Code': fake.zipcode(),
            'Customer Contact Number': fake.phone_number(),
            'Customer Email': fake.email()
        }
        customers.append(customer)
    return customers

# Generate fake data for orders
def generate_order_data(num_orders, customers):
    orders = []
    for _ in range(num_orders):
        customer = random.choice(customers)
        order = {
            'Order ID': fake.uuid4(),
            'Customer ID': customer['Customer ID'],
            'Order Date': fake.date_time_between(start_date='-30d', end_date='now'),
            'Delivery Date': fake.date_time_between(start_date='now', end_date='+30d'),
            'Order Status': random.choice(['Pending', 'In Progress', 'Completed']),
            'Order Address': customer['Customer Address'],
            'Order City': customer['Customer City'],
            'Order State': customer['Customer State'],
            'Order Zip Code': customer['Customer Zip Code'],
            'Item Description': fake.word(),
            'Item Quantity': random.randint(1, 10),
            'Item Weight': random.uniform(0.1, 10.0)
        }
        orders.append(order)
    return orders

# Generate fake data for drivers
def generate_driver_data(num_drivers):
    drivers = []
    for _ in range(num_drivers):
        driver = {
            'Driver ID': fake.uuid4(),
            'Driver Name': fake.name(),
            'Driver Contact Number': fake.phone_number(),
            'Driver License Number': fake.random_number(digits=10),
            'Vehicle ID': fake.random_number(digits=6),
            'Vehicle Type': random.choice(['Car', 'Truck', 'Van']),
            'Vehicle Registration Number': fake.random_number(digits=8),
            'Driver Status': random.choice(['Available', 'Busy', 'Offline']),
            'Current Location Latitude': fake.latitude(),
            'Current Location Longitude': fake.longitude()
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
            'Assignment ID': fake.uuid4(),
            'Order ID': order['Order ID'],
            'Driver ID': driver['Driver ID'],
            'Assigned Date': fake.date_time_between(start_date='-1d', end_date='now'),
            'Assigned Status': random.choice(['Pending', 'In Progress', 'Completed']),
            'Assigned Address': order['Order Address'],
            'Assigned City': order['Order City'],
            'Assigned State': order['Order State'],
            'Assigned Zip Code': order['Order Zip Code']
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
    host="localhost",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Function to create table in PostgreSQL and import data
def import_csv_to_postgres(csv_file, table_name):
    # Load CSV data into pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Create table in PostgreSQL
    create_table_query = sql.SQL('''
        CREATE TABLE IF NOT EXISTS {} (
            {}
        )
    ''').format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(sql.Identifier(column) + sql.SQL(' VARCHAR') for column in df.columns)
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
