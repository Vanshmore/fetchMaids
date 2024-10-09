import pymongo
from bson.objectid import ObjectId
from datetime import datetime

# MongoDB connection string
mongo_uri = "mongodb+srv://morevansh2003:maideasy@cluster0.da2a1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(mongo_uri)

# Access the 'test' database
db = client['test']

# Fetch customer details
def get_customer_details(customer_id):
    customer = db.customers.find_one({"_id": ObjectId(customer_id)})
    if not customer:
        raise Exception(f"Customer with ID {customer_id} not found.")
    return {
        "location": customer['area'],  # Fetch the customer's location
    }

# Fetch job details (handles different job types: One day, Range)
def get_job_details(customer_id, service_id):
    job = db.jobs.find_one({"customerId": ObjectId(customer_id), "serviceId": ObjectId(service_id)})
    if not job:
        raise Exception(f"Job with customer ID {customer_id} and service ID {service_id} not found.")
    
    # Handling different service types (One day or Range)
    job_details = {
        "preferred_time": job['time'],  # Fetch preferred time
        "service_type": job['serviceType'],  # Fetch service type ('One day', 'Range', etc.)
    }
    
    if job['serviceType'] == 'One day':
        job_details['date'] = job.get('date')
    elif job['serviceType'] == 'Range':
        job_details['dates'] = job.get('dates')
    
    return job_details

# Fetch maid details
def get_maid_details():
    maids = db.maids.find({})
    maid_list = []
    for maid in maids:
        # print(maid)  # Print maid document to debug
        maid_list.append({
            "id": maid['_id'],
            "location": maid.get('preferredLocations', []),  # Use .get() to avoid KeyError
            "rating": maid.get('rating', 0),  # Provide a default value for rating
            "time_slots": maid.get('timeSlots', []),  # Use .get() for timeSlots
            "working_days": maid.get('workingDays', [])  # Use .get() for workingDays
        })
    return maid_list


# Check if the customer's time falls within the maid's available time slots
def is_time_in_slot(customer_time, maid_time_slots):
    customer_time_24hr = datetime.strptime(customer_time, '%I:%M %p').strftime('%H:%M')
    for time_slot in maid_time_slots:
        start_time, end_time = time_slot.split('-')
        if start_time <= customer_time_24hr < end_time:
            return True
    return False

# Filter maids based on location and availability
def match_maids(customer_id, service_id):
    customer = get_customer_details(customer_id)
    job = get_job_details(customer_id, service_id)
    matched_maids = []
    
    # Fetch all maids
    maids = get_maid_details()
    
    for maid in maids:
        # Step 1: Location Matching
        if customer['location'] in maid['location']:
            # Step 2: Availability Matching (time and service type)
            if job['service_type'] == 'One day':
                # Match time for 'One day' service
                if is_time_in_slot(job['preferred_time'], maid['time_slots']):
                    matched_maids.append({
                        "maid_id": maid['id'],
                        "rating": maid['rating']
                    })
            elif job['service_type'] == 'Range':
                # Match time and dates for 'Range' service
                if (is_time_in_slot(job['preferred_time'], maid['time_slots']) and
                    set(job['dates'].values()).intersection(maid['working_days'])):
                    matched_maids.append({
                        "maid_id": maid['id'],
                        "rating": maid['rating']
                    })
    
    # Sort by rating
    matched_maids = sorted(matched_maids, key=lambda x: x['rating'], reverse=True)
    
    return matched_maids

# Test matching function
customer_id = ObjectId("6706830cebf7d489468bdff4")
service_id = ObjectId("6702a4befcbaf5bfc9bbab95")
best_maids = match_maids(customer_id, service_id)
print(best_maids)
