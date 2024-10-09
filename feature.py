import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Assuming features_df is your final dataframe with features
# Drop any rows with missing values if needed
features_df.dropna(inplace=True)

# Encode categorical variables (e.g., customer location, service type, maid location)
le_location = LabelEncoder()
features_df['customer_location'] = le_location.fit_transform(features_df['customer_location'])
features_df['maid_location'] = le_location.transform(features_df['maid_location'])

le_service = LabelEncoder()
features_df['service_type'] = le_service.fit_transform(features_df['service_type'])
features_df['preferred_services'] = le_service.transform(features_df['preferred_services'])

# Optionally, you could encode working days, timeslots, etc.

# Define your features and target variable
X = features_df.drop(['maid_id'], axis=1)  # Drop maid_id since we're predicting which maid to recommend
y = features_df['maid_id']  # Target variable is the maid ID

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
