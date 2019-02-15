from flask import Flask
from flask import request
import pymongo
from bson.json_util import dumps

#Connecting to database
client = pymongo.MongoClient("mongodb://helloiamuser:whatisthis123@datasetcluster-shard-00-00-e5jwa.gcp.mongodb.net:27017,datasetcluster-shard-00-01-e5jwa.gcp.mongodb.net:27017,datasetcluster-shard-00-02-e5jwa.gcp.mongodb.net:27017/test?ssl=true&replicaSet=DatasetCluster-shard-0&authSource=admin&retryWrites=true")
db = client.Reuters
posts = db.ReutersDataset

#Creating the endpoints
app = Flask(__name__)

#API endpoint to list all contents
@app.route('/api/reuters/articles',methods=['GET'])
def getAllArticles():
    params = (request.query_string).decode("utf-8")
    if(params==""):
        return dumps(posts.find())
    else:
        return "Error! Please do not enter parameters!",500

#API endpoint to get content by unique identifier
@app.route('/api/reuters/articles/<int:article_id>',methods=['GET'])
def getArticleById(article_id):
    return dumps(posts.find_one({'_id':article_id}))

#API endpoint to get content by any attributes
@app.route('/api/reuters/articles/attributes',methods=['GET'])
def getArticleByAttributes():
    params = (request.query_string).decode("utf-8")
    acceptedParams = ['id','date','topics','places','people','orgs','exchanges','companies','title','dateline','body']
    if(params==""):
        return "Error! Please enter attributes!",500
    else:
        params = params.split('&')
        #If only id is given
        if(len(params)==1 and params[0].split('=')[0]=='id'):
            return dumps(posts.find_one({'_id':int(params[0].split('=')[1])}))
        else:
            paramDict = {}
            flag = False
            for parameter in params:
                if parameter.split('=')[0] not in acceptedParams:
                    flag = True
                    break
                else:
                    if(parameter.split('=')[0]=='id'):
                        paramDict['_id'] = int(parameter.split('=')[1])
                    else:
                        paramDict[parameter.split('=')[0]] = parameter.split('=')[1]
            if(flag):
                return "Error! Please enter valid parameters!",500
            else:
                return dumps(posts.find(paramDict))

if __name__ == '__main__':
    app.run(debug=True,ssl_context='adhoc')
