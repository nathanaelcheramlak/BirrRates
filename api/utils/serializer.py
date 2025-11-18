from bson import ObjectId

def serialize_doc(doc):
    return {
        "id": str(doc["_id"]),
        **{k: v for k, v in doc.items() if k != "_id"}
    }
