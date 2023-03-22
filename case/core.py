
from elasticsearch import Elasticsearch
import cv2
import face_recognition 

def add_embedding(es,img_encode,name,id):
    data ={
            "face_name":name,
            "face_encoding":img_encode.tolist(),
        }

    es.index(index="faces",doc_type="_doc",id=id,document=data)
    print("Emedding Added Succcessfully!!")
    
def createIndex(es):
    mapping = {
    "mappings": {
        "properties": {
            "title_vector":{
                "type": "dense_vector",
                "dims": 128
            },
            "title_name": {"type": "keyword"}
            }
        }
    }
    es.indices.create(index="face_recognition", body=mapping)

def search_person_embedding(es,img_encode):
    query = {

        "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                # "source": "cosineSimilarity(params.queryVector,'face_encoding') + 1.0",
                "source": "1 / (1 + l2norm(params.queryVector, 'face_encoding'))",

                "params": {
                    "queryVector": img_encode.tolist()
                }
            }
        }
    }

    res = es.search(index="faces", query=query)
    # print(res)
    for hit in res['hits']['hits']: 
                    #double score=float(hit['_score']) 
                    if (float(hit['_score']) > 0.64): 
                        print("==> This face  match with ", hit['_source']['face_name'], ",the score is" ,hit['_score'],hit['_id']) 
                        return hit['_id']
                    elif (float(hit['_score']) > 0.61):
                        print("==> This Could be  ", hit['_source']['face_name'], ",the score is" ,hit['_score'],hit['_id']) 
                        return hit['_id']
                    else: 
                        print("==> Unknown face")

def create_connection():
    hosts = ["localhost"]
    port = 9200
    auth = ("name","<password>")
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    return es


if __name__ == "__main__":   

    es = create_connection()
    img = cv2.imread('Thor.jpeg') # Array of image 
    rgb_image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # Color conversion BGR to RGB 
    img_encode = face_recognition.face_encodings(rgb_image)[0] # encode image 
    search_person_embedding(es=es,img_encode=img_encode)
    # add_embedding(es,img_encode,"Thor ",3)

