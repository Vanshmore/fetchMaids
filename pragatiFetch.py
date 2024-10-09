import pymongo
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from sklearn.preprocessing import MinMaxScaler
from bson.objectid import ObjectId
from datetime import datetime
import numpy as np

# MongoDB connection string
mongo_uri = "mongodb+srv://morevansh2003:maideasy@cluster0.da2a1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(mongo_uri)

# Access the 'test' database
db = client['test']

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="maid_locator")

# Function to get latitude and longitude from location name
def get_coordinates(location_name):
    location = geolocator.geocode(location_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"Location '{location_name}' could not be geocoded.")

# Fetch customer details
def get_customer_details(customer_id):
    customer = db.customers.find_one({"_id": ObjectId(customer_id)})
    return {
        "location": customer['area'],  # Fetch the customer's location (area)
    }

# Fetch job details (time, service)
def get_job_details(customer_id, service_id):
    job = db.jobs.find_one({"customerId": customer_id, "serviceId": service_id})
    return {
        "preferred_time": job['time'],  # Fetch preferred time
        "dates": job['dates'],  # Fetch date range
    }

# Fetch maid details
def get_maid_details():
    maids = db.maids.find({})
    maid_list = []
    for maid in maids:
        # Use .get() to safely access potential missing keys
        maid_list.append({
            "id": maid['_id'],
            "location": maid.get('preferredLocations', []),  # Provide an empty list if the key is missing
            "rating": maid.get('rating', 0),  # Provide a default rating if the key is missing
            "time_slots": maid.get('timeSlots', []),  # Provide an empty list if the key is missing
            "working_days": maid.get('workingDays', [])  # Provide an empty list if the key is missing
        })
    return maid_list

def is_time_in_slot(customer_time, maid_time_slots):
    # Convert customer time to 24-hour format for comparison
    customer_time_24hr = datetime.strptime(customer_time, '%I:%M %p').strftime('%H:%M')

    matching_slots = []

    for time_slot in maid_time_slots:
        start_time, end_time = time_slot.split('-')  # Split the time range
        if start_time <= customer_time_24hr < end_time:  # Check if customer time falls in the range
            matching_slots.append(time_slot)

    return matching_slots

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
            # Step 2: Availability Matching (day and time)
            matching_time_slots = is_time_in_slot(job['preferred_time'], maid['time_slots'])
            if matching_time_slots:  # Check if there are matching time slots
                matched_maids.append({
                    "maid_id": maid['id'],
                    "rating": maid['rating'],
                    "location": maid['location'],  # Add location for KNN
                    "matching_time_slots": matching_time_slots  # Include matching time slots in the result
                })

    # Sort by rating
    matched_maids = sorted(matched_maids, key=lambda x: x['rating'], reverse=True)
    return matched_maids

# Function to calculate the distance between customer and maid based on their locations
def calculate_distance(customer_location, maid_location):
    return geodesic(customer_location, maid_location).km  # Returns distance in kilometers

# Normalize attributes like rating and time slots for KNN
def normalize_attributes(matched_maids):
    ratings = np.array([float(maid['rating']) for maid in matched_maids]).reshape(-1, 1)
    time_slots = np.array([len(maid['matching_time_slots']) for maid in matched_maids]).reshape(-1, 1)

    # Min-Max scaling to normalize ratings and time slots
    scaler = MinMaxScaler()
    normalized_ratings = scaler.fit_transform(ratings)
    normalized_time_slots = scaler.fit_transform(time_slots)

    for i, maid in enumerate(matched_maids):
        maid['normalized_rating'] = normalized_ratings[i][0]
        maid['normalized_time_slots'] = normalized_time_slots[i][0]

    return matched_maids

# KNN function to suggest the best maids based on distance, rating, and availability
def knn_suggest_best_maids(customer_location_name, matched_maids, k=3):
    # Convert customer location name to coordinates (lat, lon)
    customer_location = get_coordinates(customer_location_name)

    # Normalize maid attributes
    matched_maids = normalize_attributes(matched_maids)

    # Calculate distance between the customer and each maid
    for maid in matched_maids:
        # Convert maid location name to coordinates
        maid_location = get_coordinates(maid['location'])
        maid['distance'] = calculate_distance(customer_location, maid_location)

    # Combine distance, normalized rating, and normalized time slots into a single score
    for maid in matched_maids:
        maid['knn_score'] = maid['normalized_rating'] * 0.5 + maid['normalized_time_slots'] * 0.3 + (1 / (1 + maid['distance'])) * 0.2  # Weighted score

    # Sort maids by their KNN score
    best_maids = sorted(matched_maids, key=lambda x: x['knn_score'], reverse=True)

    # Return top k maids
    return best_maids[:k]

# Test matching function
customer_id = ObjectId("67053e4634f5869c42331090")
service_id = ObjectId("6702a4befcbaf5bfc9bbab93")
best_maids = match_maids(customer_id, service_id)

# Get customer location name
customer_details = get_customer_details(customer_id)
customer_location_name = customer_details['location']

# Get the top 3 maids using KNN
top_maids = knn_suggest_best_maids(customer_location_name, best_maids, k=3)
print(top_maids)  # Maids are sorted by their KNN score
