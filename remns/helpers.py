from json.encoder import JSONEncoder
jse = JSONEncoder()

def encode(model_collection):
    return jse.encode([model.api_representation() for model in model_collection])
