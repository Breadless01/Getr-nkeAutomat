from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["Vending"]

db.createCollection("Drinks", validator={
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["key", "name", "price_cents"],
            "additionalProperties": "false",
            "properties": {
                "_id": { "bsonType": "objectId" },
                "key": { "bsonType": "string", "minLength": 1, "description": "business key, unique" },
                "name": { "bsonType": "string", "minLength": 1 },
                "price_cents": { "bsonType": "int", "minimum": 0, "description": ">= 0" }
            }
        }
    },
    "validationLevel": "strict",
    "validationAction": "error"
})

# db.drinks.createIndex({ key: 1 }, { unique: true, name: "ux_key" });
# db.drinks.createIndex({ name: 1 }, { name: "ix_name" });