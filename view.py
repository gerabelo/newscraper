# 5d5ad15a49c88a73c8fe8ca4 5d5ad16849c88a73c8fe8fed

from pymongo import MongoClient
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client['facebook']
posts = db['ACriticaCom']

# negativos = posts.find({'publicacao':{'$regex':'/Lula/'}}).limit(3)
negativos = posts.find({"publicacao": {"$regex": "lula", "$options": "i"}})


# positivos = posts.find({{'score':{'$gt':0}},{'publicacao':{'$regex':/Lula/}}}).limit(3)

print('negativos')
for negativo in negativos:
    print(negativo.get('score'))
    print(negativo.get('_id'))
    soup = BeautifulSoup(negativo.get("publicacao"), 'html.parser')
    post_message = soup.find("div",{"data-testid":"post_message"})
    if post_message:
        paragraphs = post_message.find_all("p")
        if paragraphs:
            for paragraph in paragraphs:
                print(paragraph.get_text())
    
# print('positivos')
# for positivo in positivos:
#     print(positivo.get('score'))
#     soup = BeautifulSoup(positivo.get("publicacao"), 'html.parser')
#     post_message = soup.find("div",{"data-testid":"post_message"})
#     if post_message:
#         paragraphs = post_message.find_all("p")
#         if paragraphs:
#             for paragraph in paragraphs:
#                 print(paragraph.get_text())
    
