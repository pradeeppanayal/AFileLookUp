import logging
from CommonDAO import CommonDAO


class FileLabelMapperDAO(CommonDAO):
    def __init__(self, dbname: str) -> None:
        super().__init__(dbname)        
        self.checkSchema()
    
    def checkSchema(self):        
        self._executeUpdate('''
            CREATE TABLE IF NOT EXISTS FileLabelMapper (
                FILE_ID INTEGER NOT NULL,
                LABEL_ID INTEGER NOT NULL
            )
        ''')
    
    def mapLabel(self, fileid:int, labelId:int):
        tcount = self._executeUpdate(f'INSERT INTO FileLabelMapper(FILE_ID, LABEL_ID) VALUES({fileid},{labelId})') 
        return tcount
        
    def unMapLabel(self, fileid:int, labelId:int):
        tcount = self._executeUpdate(f'DELETE FROM FileLabelMapper where FILE_ID = {fileid} and LABEL_ID = {labelId}') 
        return tcount