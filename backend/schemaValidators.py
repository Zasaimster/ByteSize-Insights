userValidator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email", "password"],
        "properties": {
            "name": {
                "bsonType": "string"
            },
            "email": {
                "bsonType": "string"
            },
            "password": {
                "bsonType": "string"
            },
            "repositories": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                }
            }
        }
    }
}

repositoryValidator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["url", "name", "description"],
        "properties": {
            "url": {
                "bsonType": "string"
            },
            "name": {
                "bsonType": "string"
            },
            "description": {
                "bsonType": "string"
            }
        }
    }
}

pullRequestValidator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["number", "name", "description", "author", "date"],
        "properties": {
            "number": {
                "bsonType": "int"
            },
            "name": {
                "bsonType": "string"
            },
            "description": {
                "bsonType": "string"
            },
            "author": {
                "bsonType": "string",
            },
            "date": {
                "bsonType": "date"
            },
            "reviewers": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                }
            },
            "labels": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                }
            }
        }
    }
}