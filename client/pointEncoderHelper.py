import json

class PointEncoderHelper(json.JSONEncoder): 
    def default(self, obj): 
        return [obj.x, obj.y]