from flask import Flask, jsonify, request
from bson.objectid import ObjectId
import pymongo
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection string
mongo_uri = "mongodb+srv://morevansh2003:maideasy@cluster0.da2a1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(mongo_uri)
db = client['test']

# Fetch job details
def get_job_details(job_id):
    job = db.jobs.find_one({"_id": ObjectId(job_id)})
    customer = db.customers.find_one({"_id": ObjectId(job['customerId'])})
    
    return {
        "customer_location": customer['area'],  # Fetch the customer's location (area)
        "preferred_time": job['time'],  # Fetch preferred time
        "dates": job['dates'],  # Fetch date range
        "service_id": job['serviceId'],  # Fetch service ID
    }

# Fetch maid details
def get_maid_details():
    maids = db.maids.find({})
    maid_list = []
    for maid in maids:
        maid_list.append({
            "id": maid['_id'],
            "location": maid.get('preferredLocations', []),
            "rating": maid.get('rating', 0),
            "time_slots": maid.get('timeSlots', []),
            "working_days": maid.get('workingDays', [])
        })
    return maid_list

def is_time_in_slot(customer_time, maid_time_slots):
    customer_time_24hr = datetime.strptime(customer_time, '%I:%M %p').strftime('%H:%M')
    matching_slots = []
    for time_slot in maid_time_slots:
        start_time, end_time = time_slot.split('-')
        if start_time <= customer_time_24hr < end_time:
            matching_slots.append(time_slot)
    return matching_slots

# Filter maids based on location and availability
def match_maids(job_id):
    job = get_job_details(job_id)
    matched_maids = []
    maids = get_maid_details()
    for maid in maids:
        if job['customer_location'] in maid['location']:
            matching_time_slots = is_time_in_slot(job['preferred_time'], maid['time_slots'])
            if matching_time_slots:
                matched_maids.append({
                    "maid_id": maid['id'],
                    "rating": maid['rating'],
                    "location": maid['location'],
                    "matching_time_slots": matching_time_slots
                })
    matched_maids = sorted(matched_maids, key=lambda x: float(x['rating']), reverse=True)
    return matched_maids

# Normalize attributes like rating and time slots for KNN
def normalize_attributes(matched_maids):
    ratings = np.array([float(maid['rating']) for maid in matched_maids]).reshape(-1, 1)
    time_slots = np.array([len(maid['matching_time_slots']) for maid in matched_maids]).reshape(-1, 1)

    scaler = MinMaxScaler()
    normalized_ratings = scaler.fit_transform(ratings)
    normalized_time_slots = scaler.fit_transform(time_slots)

    for i, maid in enumerate(matched_maids):
        maid['normalized_rating'] = normalized_ratings[i][0]
        maid['normalized_time_slots'] = normalized_time_slots[i][0]

    return matched_maids

# KNN function to suggest the best maids
def knn_suggest_best_maids(customer_location_name, matched_maids, k=3):
    print("Customer Area:", customer_location_name)
    matched_maids = normalize_attributes(matched_maids)

    for maid in matched_maids:
        maid['knn_score'] = maid['normalized_rating'] * 0.5 + maid['normalized_time_slots'] * 0.5

    best_maids = sorted(matched_maids, key=lambda x: x['knn_score'], reverse=True)
    return best_maids[:k]

# Define API routes
@app.route('/match_maids/<job_id>', methods=['GET'])
def api_match_maids(job_id):
    try:
        best_maids = match_maids(ObjectId(job_id))
        job_details = get_job_details(ObjectId(job_id))
        customer_location_name = job_details['customer_location']
        top_maids = knn_suggest_best_maids(customer_location_name, best_maids, k=3)

        # Convert ObjectId to string for JSON serialization
        for maid in top_maids:
            maid['maid_id'] = str(maid['maid_id'])

        return jsonify(top_maids)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
