# import pymongo
# import pandas as pd
# from bson.objectid import ObjectId
# from geopy.distance import geodesic
# from datetime import datetime
# # MongoDB connection string
mongo_uri = "mongodb+srv://morevansh2003:maideasy@cluster0.da2a1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(mongo_uri)

# Access the 'test' database
db = client['test']


# import pymongo
# import pandas as pd
# from bson.objectid import ObjectId

# # MongoDB connection
# mongo_uri = "your_mongo_connection_string"
# client = pymongo.MongoClient(mongo_uri)
# db = client['test']

# # Fetch customer details based on customerId
# def get_customer_data(customer_id):
#     customer = db.customers.find_one({"_id": ObjectId(customer_id)}, {"_id": 1, "area": 1})
#     return customer

# # Fetch maid details based on serviceId
# def get_maid_data(service_id):
#     maids = list(db.maids.find({"_id": ObjectId(service_id)}, {"_id": 1, "preferredLocations": 1, "rating": 1, "timeSlots": 1}))
#     return maids

# # Fetch job details based on customerId and serviceId
# def get_job_data(customer_id, service_id):
#     job = db.jobs.find_one({"customerId": ObjectId(customer_id), "serviceId": ObjectId(service_id)}, 
#                            {"customerId": 1, "serviceId": 1, "time": 1, "dates": 1})
#     return job

# # Main function to fetch the details based on customerId and serviceId
# def fetch_details(customer_id, service_id):
#     customer = get_customer_data(customer_id)
#     maids = get_maid_data(service_id)
#     job = get_job_data(customer_id, service_id)
    
#     # Create DataFrames from fetched data
#     customer_df = pd.DataFrame([customer]) if customer else pd.DataFrame()
#     maids_df = pd.DataFrame(maids) if maids else pd.DataFrame()
#     job_df = pd.DataFrame([job]) if job else pd.DataFrame()

# #     # Display the DataFrames
# #     print("Customer Details DataFrame:\n", customer_df)
# #     print("Maid Details DataFrame:\n", maids_df)
# #     print("Job Details DataFrame:\n", job_df)
#     return customer_df, maids_df, job_df

# # Test with customerId and serviceId
# customer_id = ObjectId("67053e4634f5869c42331090")
# service_id = ObjectId("6702a4befcbaf5bfc9bbab94")
# fetch_details(customer_id, service_id)



# # Helper function to check if time slots match
# def is_time_in_slot(customer_time, maid_time_slots):
#     customer_time_24hr = datetime.strptime(customer_time, '%I:%M %p').strftime('%H:%M')
#     for time_slot in maid_time_slots:
#         start_time, end_time = time_slot.split('-')
#         if start_time <= customer_time_24hr < end_time:
#             return 1  # Match
#     return 0  # No match

# # Feature: Location Match (1 if match, else 0)
# job_df['location_match'] = job_df.apply(lambda x: 
#     1 if customer_df[customer_df['_id'] == x['customerId']]['area'].values[0] in 
#          maid_df[maid_df['_id'] == x['serviceId']]['preferredLocations'].values[0]
#     else 0, axis=1)

# # Feature: Time Match (1 if match, else 0)
# job_df['time_match'] = job_df.apply(lambda x: 
#     is_time_in_slot(x['time'], maid_df[maid_df['_id'] == x['serviceId']]['timeSlots'].values[0]), axis=1)

# # Feature: Rating
# job_df['maid_rating'] = job_df.apply(lambda x: 
#     maid_df[maid_df['_id'] == x['serviceId']]['rating'].values[0], axis=1)

# # Create the final dataset for training
# final_df = job_df[['location_match', 'time_match', 'maid_rating']]
# final_df['match'] = 1  # You can replace this with actual match/no-match labels

# # Display the final DataFrame
# print(final_df.head())

