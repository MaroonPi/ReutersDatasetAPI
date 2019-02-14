from flask import Flask
from flask import request
import pymongo
from bson.json_util import dumps

#Connecting to database
client = pymongo.MongoClient("mongodb://helloiamuser:whatisthis123@datasetcluster-shard-00-00-e5jwa.gcp.mongodb.net:27017,datasetcluster-shard-00-01-e5jwa.gcp.mongodb.net:27017,datasetcluster-shard-00-02-e5jwa.gcp.mongodb.net:27017/test?ssl=true&replicaSet=DatasetCluster-shard-0&authSource=admin&retryWrites=true")
db = client.Reuters
posts = db.ReutersDataset

#Creating the endpoint
app = Flask(__name__)

@app.route('/api/reuters',methods=['GET'])
def getReutersArticle():
    params = (request.query_string).decode("utf-8")
    returnDict = {}
    #To list all contents
    if(params==""):
        return dumps(posts.find())
    else:
        params = params.split('&')
        #To list content specified by unique identifier
        if(len(params)==1 and params[0].split('=')[0]=='id'):
            return dumps(posts.find_one({'_id':params[0].split('=')[1]}))
        else:
        #To search content specified by attributes
            paramDict = {}
            for i in params:
                paramDict[i.split('=')[0]] = i.split('=')[1]
            return dumps(posts.find(paramDict))

if __name__ == '__main__':
    app.run(debug=True,ssl_context='adhoc')
