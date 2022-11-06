import json
import os
import shutil
import zipfile
import time
from urllib import request, parse
import logging

logging.basicConfig(filename='Watcher.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level= logging.DEBUG) 

DOWNLOAD_DIR ="C:\\Users\\prade\\Downloads"
REPO_DIR = os.path.abspath("repo")
ZIP_DIR = os.path.abspath("zip")

INTERVAL = 5
api_url = 'http://localhost:8080/api/fileinfo'

ignoreList = []
def _checkForZipFile():

   for filename in os.listdir(DOWNLOAD_DIR):
      #print(f"processing filename {filename}")
      f = os.path.join(DOWNLOAD_DIR, filename)
      # checking if it is a file
      if not os.path.isfile(f):
            continue
      if( ".zip" not in filename ):
         continue
      if filename[len(filename)-4:] != ".zip":
         continue
      if filename in ignoreList:
         continue
      try:
         filenameWithoutExt = filename[:-4];
         sourceFile = os.path.join(DOWNLOAD_DIR,filename)
         targetDir = os.path.join(REPO_DIR, filenameWithoutExt)
         #os.mkdir(targetDir)

         logging.info(f"Extracting file {filename} to location {targetDir}")
         with zipfile.ZipFile(sourceFile, 'r') as ref:
            ref.extractall(targetDir)
         imagefiles, vectorfiles = _getFileDetails(targetDir)
         if (not imagefiles or not vectorfiles or len(imagefiles) == 0 or len(vectorfiles) == 0 ):
            logging.error("Could not find any image/vector file(s)")
            continue
         logging.info(f"Identified images: {len(imagefiles)} and vector files {len(vectorfiles)}")
         for i in range(min(len(vectorfiles),len(imagefiles))):
            imagefile = imagefiles[i]
            vectorfile = vectorfiles[i]

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
               resp = response.read().decode("utf-8")
               logging.info(f'Registerd file  with request {data} and response {resp}')
         logging.info(f"Archiving file {filename} to location {ZIP_DIR}")
         shutil.move(sourceFile, os.path.join(ZIP_DIR,filename))
      except Exception as ex:
         ignoreList.append(filename)
         logging.error(f"Could not process the file {filename} cause {ex}")

def _getFileDetails(path):
   imageFiles = []
   vectorFiles = []
   for filename in os.listdir(path):
      if not os.path.isfile(os.path.join(path,filename)):
            continue
      extention = filename[len(filename)-4:] 
      if extention == '.eps':
         vectorFiles.append(filename);
      if extention in ['.jpg', 'jpeg', '.png']:
         imageFiles.append(filename)
   return imageFiles, vectorFiles

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