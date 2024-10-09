
# def services_match(customer_service, maid_services):
#          return customer_service in maid_services

# # Create an empty list to store the results
# data = []

# for _, customer in customers_df.iterrows():
#     for _, maid in maids_df.iterrows():
#         # Check if location matches
#         if customer['area'] == maid['location']:
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

# # Optional: Add additional features, like time overlaps, distance, etc.
# # For example, you can calculate the distance between customer and maid location (if you have coordinates)

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