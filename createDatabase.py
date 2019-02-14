import os
from bs4 import BeautifulSoup
import pymongo

#Connecting to database
client = pymongo.MongoClient("mongodb://helloiamuser:whatisthis123@datasetcluster-shard-00-00-e5jwa.gcp.mongodb.net:27017,datasetcluster-shard-00-01-e5jwa.gcp.mongodb.net:27017,datasetcluster-shard-00-02-e5jwa.gcp.mongodb.net:27017/test?ssl=true&replicaSet=DatasetCluster-shard-0&authSource=admin&retryWrites=true")
db = client.Reuters
posts = db.ReutersDataset

#Parsing XML File. Converted the SGM file into an XML file for better parsing
f = open("reut2-000.xml","r")
data = f.read()
soup = BeautifulSoup(data,"html.parser")

#Collecting all reuter articles into an array
reuterItems = [a for a in soup.findAll('reuters')]

#Reading each reuter article and posting into database
reuterDict = {}
topics = []
places = []
people = []
orgs = []
exchanges = []
companies = []
for i in range(len(reuterItems)):
    reuterDict["_id"] = i+1
    try:
        reuterDict["date"] = str(reuterItems[i].find('date').get_text())
    except AttributeError:
        reuterDict["date"] = ""
    for d in reuterItems[i].findAll('d'):
        if(d.parent.name=='topics'):
            try:
                topics.append(str(d.get_text()))
            except AttributeError:
                topics.append("")
        elif(d.parent.name=='places'):
            try:
                places.append(str(d.get_text()))
            except AttributeError:
                places.append("")
        elif(d.parent.name=='people'):
            try:
                people.append(str(d.get_text()))
            except AttributeError:
                people.append("")
        elif(d.parent.name=='orgs'):
            try:
                orgs.append(str(d.get_text()))
            except AttributeError:
                orgs.append("")
        elif(d.parent.name=='exchanges'):
            try:
                exchanges.append(str(d.get_text()))
            except AttributeError:
                exchanges.append("")
        elif(d.parent.name=='companies'):
            try:
                companies.append(str(d.get_text()))
            except AttributeError:
                companies.append("")
    reuterDict["topics"] = topics
    reuterDict["places"] = places
    reuterDict["people"] = people
    reuterDict["orgs"] = orgs
    reuterDict["exchanges"] = exchanges
    reuterDict["companies"] = companies
    try:
        reuterDict["title"] = str(reuterItems[i].find('title').get_text())
    except AttributeError:
        reuterDict["title"] = ""
    try:
        reuterDict["dateline"] = str(reuterItems[i].find('dateline').get_text())
    except AttributeError:
        reuterDict["dateline"] = ""
    try:
        reuterDict["body"] = str(reuterItems[i].find('body').get_text())
    except AttributeError:
        reuterDict["body"] = ""
    post_id = posts.insert_one(reuterDict).inserted_id
    topics.clear()
    places.clear()
    people.clear()
    orgs.clear()
    exchanges.clear()
    companies.clear()
    reuterDict.clear()
