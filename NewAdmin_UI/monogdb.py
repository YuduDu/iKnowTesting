from pymongo import MongoClient

class mongodb:
    def __init__(self):
        try:
            self.client = MongoClient('localhost',27017)
            self.db = self.client.iknowTest
        except:
            print "Failed to connect MonogDB."

    def get_collection(self,collection_name):
        return self.db[collection_name]