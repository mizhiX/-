import pymongo

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.youyaoqi


def insert_company(company_dict):
    db.company.insert_one(company_dict)
