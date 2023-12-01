import pymongo

URI = "mongodb+srv://cs130:7SBYtWrVqif1EzoR@cluster0.miyegq5.mongodb.net/?retryWrites=true&w=majority"


def get_mongo_db():
    client = pymongo.MongoClient(URI)
    db = client["ByteSize-Insights"]

    try:
        yield db
    finally:
        client.close()
