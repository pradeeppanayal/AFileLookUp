import logging
import os
from typing import List 

from FileInfoDAO import FileInfoDOA
from FileLabelMapperDAO import FileLabelMapperDAO
from LabelDAO import LabelDOA
from beans import FileInfo, Label

class FileLookUpManager(object):
    def __init__(self,dbname:str = 'fileinfo.db') -> None:
        self.fileInfoDAO = FileInfoDOA(dbname) 
        self.labelDAO = LabelDOA(dbname); 
        self.fileLabelMapperDAO = FileLabelMapperDAO(dbname)

    def performSearch(self, searchKeyWord:str) -> List[map]:
        items =  self.fileInfoDAO.getFilesByLabel(searchKeyWord);
        if not items:
            return []
        return [self._tomap(x) for x in items]

    def save(self,info:FileInfo) -> bool:
        return self.fileInfoDAO.saveFileInfo(info) >0

    def getRecent(self):
        return  [self._tomap(x) for x in self.fileInfoDAO.getRecent()];

    def getById(self,fileId: int, loadLabel:bool) -> map:
        info =  self.fileInfoDAO.getById(fileId)
        if not info:
            return None
            
        if( not loadLabel):
            return info;
        info.labels = self.labelDAO.fetchLabelsByFileId(info.id)
        return self._tomap(info)

    def _tomap(self,info: FileInfo):
        return {
            'category':info.category,
            'imageFile': info.imageFile,
            'vectorFile': info.vectorFile,
            'createdOn':info.createdOn,
            'id': info.id,
            'labels': self._toLabelMap(info.labels)
        }

    def _toLabelMap(self, labels:list[Label])-> list:
        return [{'id': x.id,'text':x.text} for x in labels];

    def linkLabel(self, fileId: int, labelName:str) ->bool:
        label = self.labelDAO.getLabelByName(labelName);
        fileinfo = self.getById(fileId, True)
        if not label or not fileinfo:
            raise 'Not found'
        # do not map if its already mapped
        for item in fileinfo['labels']:
            if item['id'] == label.id:
                logging.info(f"{fileinfo['category']}- {labelName} mapping exist.  skipping..")
                return True

        return self.fileLabelMapperDAO.mapLabel(fileId, label.id) >0
        
    def unlinkLabel(self, fileId: int, labelId:int) ->bool: 
        return self.fileLabelMapperDAO.unMapLabel(fileId, labelId) >0

    def openInApp(Self, path):
        os.startfile(os.path.abspath(path), 'open')
        return "Started"
    def resetDB(self):
        self.fileInfoDAO.clearAll();
        
