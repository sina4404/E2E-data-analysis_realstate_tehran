import pickle

# Load the saved model
with open('trained_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Function to take input and predict price
def predict_price():
    # Take input from the user
    area_sqm = float(input("Enter area in square meters: "))
    building_age = int(input("Enter building age: "))
    num_rooms = int(input("Enter number of rooms: "))
    has_elevator = int(input("Does it have an elevator? (1 for Yes, 0 for No): "))
    has_parking = int(input("Does it have parking? (1 for Yes, 0 for No): "))
    has_storage = int(input("Does it have storage? (1 for Yes, 0 for No): "))
    district_encoded = int(input("Enter district (encoded value): "))
    floor_number = int(input("Enter floor number: "))

    # Create a list of the input values
    input_data = [[area_sqm, building_age, num_rooms, has_elevator, has_parking, has_storage, district_encoded, floor_number]]

    # Predict the price
    predicted_price = model.predict(input_data)

    # Print the predicted price
    print(f"Predicted Price (in Toman): {predicted_price[0]:.2f}")

# Run the prediction function
predict_price()