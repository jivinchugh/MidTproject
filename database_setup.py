import pymongo

def connect_to_database():
    try:
        """Connect to MongoDB database."""
        client = pymongo.MongoClient("mongodb+srv://jchugh:pass123@cluster0.zlyazvx.mongodb.net/sample_airbnb?retryWrites=true&w=majority")
        db = client["user_health"]
        collection = db["users"]
        return collection
    except Exception as e:
        print("Error connecting to database")

def add_user_to_database(collection, user_data):
    """Insert or update user data in the MongoDB collection."""
    # Check if the user already exists in the database
    existing_user = collection.find_one({"username": user_data["username"]})

    if existing_user:
        # Update existing user data
        collection.update_one({"_id": existing_user["_id"]}, {"$set": user_data})
        print("User information updated in the database.")
    else:
        # Insert new user data
        collection.insert_one(user_data)
        print("User added to the database.")

def delete_user_from_database(collection, username):
    #to delete user (after finding the matching username)
    user_deleted = collection.delete_one({"username": username})

    if user_deleted.deleted_count == 0:
        #not found
        print(f"User {username} not found.")
        return False

    collection.delete_many({"user_username": username})
    print(f"User {username} deleted.")
    return True

def search_user_from_database(collection, finditem):
    username = f".*{finditem}.*"
    result = collection.find({"username": {"$regex": username, "$options": "i"}})
    return list(result)