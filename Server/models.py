user_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "phone", "registered_faces"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "phone": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "email" :{
                "bsonType": "string",
                "description": "must be a string"
            },
            "active_profile_id" :{
                "bsonType": "int",
                "description": "must be an integer"
            },
             "registered_faces": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["id", "name", "relation", "embeddings"],
                    "properties": {
                        "id": {
                            "bsonType": "int",
                            "description": "must be an integer and is required"
                        },
                        "name": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "relation": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "embeddings": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "array",
                                "description": "must be an array of embeddings"
                            }
                        }
                    }
                }
            }
        }
    }
}

history_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "history"],
        "properties": {
            "user_id": {
                "bsonType": "objectId",
                "description": "must be an ObjectId and is required"
            },
            "history": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["date", "entries"],
                    "properties": {
                        "date": {
                            "bsonType": "date",
                            "description": "must be a date and is required"
                        },
                        "entries": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "object",
                                "required": ["id","name", "timestamp"],
                                "properties": {
                                     "id": {
                                        "bsonType": "int",
                                        "description": "must be an integer and is required"
                                    },
                                    "name": {
                                        "bsonType": "string",
                                        "description": "must be a string and is required"
                                    },
                                    "timestamp": {
                                        "bsonType": "date",
                                        "description": "must be a date and is required"
                                    },
                                    "image": {
                                        "bsonType": "string",
                                        "description": "must be a string (base64 encoded image) and is required"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

profiles_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "profiles"],
        "properties": {
            "user_id": {
                "bsonType": "objectId",
                "description": "must be an ObjectId and is required"
            },
            "profiles": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["profile_name", "allowed_people"],
                    "properties": {
                        "id": {
                            "bsonType": "int",
                            "description": "must be an integer"
                        },
                        "profile_name": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "allowed_people": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "int",
                                "description": "must be an integer"
                            }
                        }
                    }
                }
            }
        }
    }
}

notifications_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "suspicious_activity", "face_recognition"],
        "properties": {
            "user_id": {
                "bsonType": "objectId",
                "description": "must be an ObjectId and is required"
            },
            "suspicious_activity": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["timestamp", "classification"],
                    "properties": {
                        "timestamp": {
                            "bsonType": "date",
                            "description": "must be a date and is required"
                        },
                        "classification": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        }
                    }
                }
            },
            "face_recognition": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["timestamp", "name"],
                    "properties": {
                        "timestamp": {
                            "bsonType": "date",
                            "description": "must be a date and is required"
                        },
                        "name": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        }
                    }
                }
            }
        }
    }
}
