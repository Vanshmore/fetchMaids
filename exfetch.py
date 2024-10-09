import pymongo
import pandas as pd
from geopy.distance import geodesic
from bson.objectid import ObjectId
# MongoDB connection string
mongo_uri = "mongodb+srv://morevansh2003:maideasy@cluster0.da2a1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(mongo_uri)

# Access the 'test' database
db = client['test']
customer_id = ObjectId("67053e4634f5869c42331090")
# service_id = ObjectId("6702a4befcbaf5bfc9bbab93")
# Fetch the job by customerId and serviceId and print the time
def fetch_job_time(customer_id, service_id):
    job = db.jobs.find_one({"customerId": customer_id, "serviceId": service_id})
    
    if job:
        print(f"Job time: {job.get('time', 'No time available')}")  # Fetch and print 'time'
    else:
        print(f"No job found for Customer ID: {customer_id} and Service ID: {service_id}")

# Test the function
# customer_id = "<customer_id_here>"  # Replace with actual customer ID
# service_id = "<service_id_here>"  # Replace with actual service ID



# fetch_job_time(customer_id, service_id)





# Fetch the customer by customerId and print workingDays
def fetch_working_days(customer_id):
    customer = db.customers.find_one({"_id": customer_id})
    
    if customer:
        print(f"Customer workingDays: {customer.get('workingDays', 'No workingDays available')}")
    else:
        print(f"No customer found for Customer ID: {customer_id}")

fetch_working_days(customer_id)


