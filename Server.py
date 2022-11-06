import json 
from flask import Flask
from flask import send_from_directory
from flask import request
import logging
from FileManager import FileLookUpManager
from beans import FileInfo

logging.basicConfig(filename='Server.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level= logging.DEBUG) 


app = Flask(__name__)
ROOT_DIR = "repo";
manager = FileLookUpManager()


@app.route('/web/<path:filename>')
def send_report(filename):
    return send_from_directory('web', filename+".htm")

@app.route('/web/asset/<path:ftype>/<path:filename>')
def getAssets(ftype,filename):
    return send_from_directory(f'assets/{ftype}', filename)

@app.route('/api/<path:category>/<path:filename>')
def getFile(category,filename):
    return send_from_directory(f'{ROOT_DIR}/{category}', filename)

@app.route('/api/<path:category>/<path:filename>/openinapp')
def openinapp(category,filename):
    return manager.openInApp(f'{ROOT_DIR}/{category}/{filename}')

@app.route('/api/recent', methods=['GET'])
def getRecent():
   try:
      return prepareResponse(True, manager.getRecent()), 200
   except Exception as ex:
      logging.error(ex)
      return prepareResponse(False,f'Something went wrong. Cause : {ex}'),500
      
@app.route('/api/search', methods=['POST'])
def checkFile():
   try:
      data = request.json
      if(not data):
         return "No payload", 400
      if(not data['searchKeyWord']):
         return "No search keyword", 400
      return prepareResponse(True, manager.performSearch(data['searchKeyWord'])), 200
   except Exception as ex:
      logging.error(ex)
      return prepareResponse(False,f'Something went wrong. Cause : {ex}'),500

@app.route('/api/fileinfo', methods=['POST'])
def addInfo():
   try:
      data = request.json
      if(not data):
         return "No payload", 400
      if(not data['category'] or not data['imageFile'] or not data['vectorFile'] ):
         return "All the fields are required Sample ie category,imageFile,vectorFile ", 400
      info = FileInfo(data['category'],data['imageFile'],data['vectorFile'])
      return prepareResponse(manager.save(info),"Added"), 200
   except Exception as ex:
      logging.error(ex)
      return prepareResponse(False,f'Something went wrong. Cause : {ex}'),500

@app.route('/api/fileinfo/<path:fileid>', methods=['GET'])
def getFileInfoById(fileid):
   try:
      loadLabel = True
      return prepareResponse(True, manager.getById(fileid,loadLabel));
   except Exception as ex:
      logging.error(ex)
      return prepareResponse(False,f'Something went wrong. Cause : {ex}'),500

@app.route('/api/fileinfo/<path:fileId>/labels/<path:labelid>', methods=['DELETE'])
def deleteLabel(fileId,labelid):
   try:    
         return prepareResponse(manager.unlinkLabel(fileId, labelid),"Deleted")  
   except Exception as ex:
      logging.error(ex)
      return prepareResponse(False,f'Something went wrong. Cause : {ex}'),500
@app.route('/api/fileinfo/<path:fileId>/labels', methods=['POST'])
def mapLabel(fileId):
   try:    
         data=  request.json
         assert data and data['label'], "Required label"
         return prepareResponse(manager.linkLabel(fileId, data['label']),"Added")  
   except Exception as ex:
      logging.error(ex)
      return prepareResponse(False,f'Something went wrong. Cause : {ex}'),500

def prepareResponse(success:bool, data:any)-> map:
   resp = {'data':data, 'status':'success'}
   if not success:
      resp['status'] = 'error'
   return resp

if __name__ == '__main__': 
   #manager = FileLookUpManager()
   #print(manager)
   app.run()