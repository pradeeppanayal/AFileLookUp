from math import fabs
from typing import List
from datetime import datetime

import logging
from datetime import datetime
from CommonDAO import CommonDAO
from FileLabelMapperDAO import FileLabelMapperDAO
from LabelDAO import LabelDOA

from beans import FileInfo

class FileInfoDOA(CommonDAO): 
    def __init__(self,dbname:str = 'fileinfo.db') -> None:   
        super().__init__(dbname) 
        self.labelDAO = LabelDOA(dbname)
        self.fileLabelMapperDAO = FileLabelMapperDAO(dbname);
        self.checkSchema()

    def checkSchema(self):
        self._executeUpdate('''
            CREATE TABLE IF NOT EXISTS FileInfo (
                ID INTEGER PRIMARY KEY NOT NULL,
                IMAGE_FILE VARCHAR(50) NOT NULL,
                VECTOR_FILE VARCHAR(50) NOT NULL,
                CATEGORY VARCHAR(50) NOT NULL,
                CREATED_ON INTEGER NOT NULL
            );
        ''')

    def getFilesByLabel(self, label:str):
        vals = self._executeFetchAll(f'''SELECT DISTINCT FileInfo.ID,FIleInfo.CATEGORY,  FileInfo.IMAGE_FILE, FileInfo.VECTOR_FILE, CREATED_ON 
                                        from FIleInfo, Labels, FileLabelMapper where FileLabelMapper.FILE_ID= FileInfo.ID
                                        and FileLabelMapper.LABEL_ID = Labels.ID
                                        and Labels.LABEL LIKE '%{label}%' ''') 
        logging.info(f"Fetched {len(vals)} entries for label {label}")
        result = []
        for item in vals:
            result.append(self._getAsFileInfo(item))
        return result;

    def getNextFileId(self) -> int:
        return self._executeSingle('select IFNULL(MAX(ID),0)+1 from FileInfo')

    def _createNew(self, info:FileInfo):
        info.id = self.getNextFileId();
        info.createdOn = (datetime.utcnow()- datetime(1970,1,1)).total_seconds()
        logging.info(f'Creating file info {info}');
        count = 0
        try:
            count = self._executeUpdate(f'''INSERT INTO FileInfo(ID,CATEGORY,IMAGE_FILE,VECTOR_FILE,CREATED_ON) 
            VALUES({info.id},'{info.category}','{info.imageFile}','{info.vectorFile}',{info.createdOn});''');
        except Exception as e:
            logging.error(e)
        return count

    def _update(self, info:FileInfo):
        raise Exception('this operation not supported')

    def saveFileInfo(self, info:FileInfo):
        count = 0
        if(info.id == 0):
            count = self._createNew(info)
        else:
            count = self._update(info)
        if count == 0:
            return 0    
        label = self.labelDAO.getLabelByName(info.category)
        if(not label):
            return 0;
        self.fileLabelMapperDAO.mapLabel(info.id, label.id)
        return count
        
    def _getAsFileInfo(self, item):
        info = FileInfo(item[1], item[2], item[3])
        info.id = item[0]
        info.createdOn = item[4]
        return info
        
    def getById(self, fileid:int) -> FileInfo:
        vals = self._executeFetchAll(f'''SELECT FileInfo.ID,FIleInfo.CATEGORY,  FileInfo.IMAGE_FILE, FileInfo.VECTOR_FILE, CREATED_ON 
                                        from FIleInfo where FileInfo.ID={fileid} ''')
        logging.info(f"Fetched {len(vals)} entries for id {fileid}")
        result = []
        for item in vals:
            result.append(self._getAsFileInfo(item))
            break
        if(len(result) == 0):
            return None;
        return  result[0]
        

    def getRecent(self, limit:int = 50):
        vals = self._executeFetchAll(f'''SELECT  FileInfo.ID,FIleInfo.CATEGORY,  FileInfo.IMAGE_FILE, FileInfo.VECTOR_FILE,CREATED_ON 
                                    from FIleInfo ORDER BY CREATED_ON DESC LIMIT {limit} ''') 
        result = []
        for item in vals:
            result.append(self._getAsFileInfo(item))
        return result;

    def clearAll(self):
        self._executeUpdate('DELETE FROM FIleInfo')
        self._executeUpdate('DELETE FROM Labels')
        self._executeUpdate('DELETE FROM FileLabelMapper') 
