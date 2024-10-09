import pymongo
import pandas as pd
from geopy.distance import geodesic
# MongoDB connection string
mongo_uri = "mongodb+srv://morevansh2003:maideasy@cluster0.da2a1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(mongo_uri)

# Access the 'test' database
db = client['test']

# Fetch data from each collection individually
def fetch_customers():
    customers_collection = db['customers']
    customers = list(customers_collection.find())
    return customers

def fetch_maids():
    maids_collection = db['maids']
    maids = list(maids_collection.find())
    return maids

def fetch_jobs():
    jobs_collection = db['jobs']
    jobs = list(jobs_collection.find())
    return jobs

# Test fetching data
customers = fetch_customers()
maids = fetch_maids()
jobs = fetch_jobs()


# Create DataFrames
customers_df = pd.DataFrame(customers)
maids_df = pd.DataFrame(maids)
jobs_df = pd.DataFrame(jobs)
# Print the first row of each collection to check field names
print(customers_df.head())  # Check if 'area', 'service_type', 'preferred_time', etc. exist
print(maids_df.head())      # Check if 'location', 'preferred_services', 'rating', etc. exist
print(jobs_df.head())       # Check the fields in jobs collection


# def services_match(customer_service, maid_services):
#          return customer_service in maid_services

# # Create an empty list to store the results
# data = []

# for _, customer in customers_df.iterrows():
#     for _, maid in maids_df.iterrows():
#         # Check if location matches
#         if customer['location'] == maid['preferredLocations']:
#             # Check if service matches
#             if services_match(customer['service_type'], maid['preferred_services']):
#                 # Create a row with all the required features
#                 data.append({
#                     'customer_id': customer['customer_id'],
#                     'customer_location': customer['location'],
#                     'service_type': customer['service_type'],
#                     'preferred_time': customer['preferred_time'],
#                     'working_days': customer['working_days'],
#                     'maid_id': maid['maid_id'],
#                     'maid_location': maid['location'],
#                     'preferred_services': maid['preferred_services'],
#                     'maid_rating': maid['rating'],
#                     'maid_availability': maid['availability'],
#                 })

# # Convert the result into a DataFrame
# features_df = pd.DataFrame(data)



# # Function to simulate calculating distance (if you had latitude/longitude data)
# def calculate_distance(customer_location, maid_location):
#     # Assuming you have lat/long coordinates for the locations
#     location_coords = {
#         'Pune': (18.5204, 73.8567),
#         'Mumbai': (19.0760, 72.8777)
#     }
#     return geodesic(location_coords[customer_location], location_coords[maid_location]).km

# # Add distance feature (optional, only if you have coordinates)
# features_df['distance'] = features_df.apply(lambda row: calculate_distance(row['customer_location'], row['maid_location']), axis=1)

# # Print the final feature DataFrame
# print(features_df)