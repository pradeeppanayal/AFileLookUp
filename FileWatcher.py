import json
import os
import shutil
import zipfile
import time
from urllib import request, parse
import logging
import logging

logging.basicConfig(filename='Watcher.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level= logging.DEBUG) 

DOWNLOAD_DIR ="C:\\Users\\Pradeep\\Downloads"
REPO_DIR = os.path.abspath("repo")
ZIP_DIR = os.path.abspath("zip")

INTERVAL = 5
api_url = 'http://localhost:8080/api/fileinfo'

skippedFiles = []
def _checkForZipFile():

   for filename in os.listdir(DOWNLOAD_DIR):
      if filename in skippedFiles:
         continue
      #print(f"processing filename {filename}")
      f = os.path.join(DOWNLOAD_DIR, filename)
      # checking if it is a file
      if not os.path.isfile(f):
            continue
      if( ".zip" not in filename ):
         continue
      if filename[len(filename)-4:] != ".zip":
         continue
      try:
         filenameWithoutExt = filename[:-4];
         sourceFile = os.path.join(DOWNLOAD_DIR,filename)
         targetDir = os.path.join(REPO_DIR, filenameWithoutExt)
         #os.mkdir(targetDir)

         logging.info(f"Extracting file {filename} to location {targetDir}")
         with zipfile.ZipFile(sourceFile, 'r') as ref:
            ref.extractall(targetDir)
         imagefile, vectorfile = _getFileDetails(targetDir)
         if (not imagefile or not vectorfile):
            logging.error("Could not find the image/vector file(s)")
            skippedFiles.append(filename)
            continue
         data =  {
            'category': filenameWithoutExt,
            'imageFile': imagefile,
            'vectorFile': vectorfile
         }
         jsondataasbytes = json.dumps(data).encode('utf-8')
         req = request.Request(api_url, data = jsondataasbytes ,method='POST')
         req.add_header('Content-Type', 'application/json; charset=utf-8')
         req.add_header('Content-Length', len(jsondataasbytes))
         with request.urlopen(req) as response:
            data = response.read().decode("utf-8")
            logging.info(f'Registerd file  with {data}')
         logging.info(f"Archiving file {filename} to location {ZIP_DIR}")
         shutil.move(sourceFile, os.path.join(ZIP_DIR,filename))
      except Exception as ex:
         skippedFiles.append(filename)
         logging.error(f"Could not process the file {filename} cause {ex}")

def _getFileDetails(path):
   imageFile = None
   vectorFile = None
   for filename in os.listdir(path):
      if not os.path.isfile(os.path.join(path,filename)):
            continue
      extention = filename[len(filename)-4:] 
      if extention == '.eps':
         vectorFile = filename;
      if extention in ['.jpg', 'jpeg', '.png']:
         imageFile = filename
   return imageFile, vectorFile

def main():
   loading = False
   while True:
      try:
         if( not loading):
            loading = True
            _checkForZipFile()
            loading = False
      except Exception as e:
         logging.error(e)
      time.sleep(INTERVAL)

if __name__ == '__main__':
   main()