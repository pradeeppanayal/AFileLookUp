from CommonDAO import CommonDAO
import logging

from beans import Label

class LabelDOA(CommonDAO): 
    def __init__(self,dbname:str = 'fileinfo.db') -> None:   
        super().__init__(dbname) 
        self.checkSchema()

    def checkSchema(self):        
        self._executeUpdate('''
            CREATE TABLE IF NOT EXISTS Labels (
                ID INTEGER NOT NULL,
                LABEL VARCHAR(50) NOT NULL
            )
        ''')   

    def updateLabel(self, fileid:int, label:str, newLabel:str):
        item = self.getById(fileid)
        if not item:
            raise 'Item not found'
        if label == item.category:
            raise 'Cannot update default label'
        tcount = self._executeUpdate(f'UPDATE Labels SET LABEL="{newLabel}" WHERE FILE_ID={fileid} and LABEL ="{label}"')
        logging.info(f'Created label : {label} for file id {fileid}')
        return tcount

    def getLabelByName(self, labelName:str, createIfNotExist:bool = True) -> Label:
        items = self._executeFetchAll(f'SELECT ID, LABEL FROM Labels where LABEL="{labelName}"');
        if(items and len(items)>0):
            item = Label(items[0][1]);
            item.id = items[0][0];
            return item
        if not createIfNotExist:
            return None
        id= self.getNextLabelId()
        logging.info(f'creating label with name :{labelName} and id {id}')
        self._executeUpdate(f'INSERT INTO Labels(ID, LABEL) VALUES({id},"{labelName}")')
        return self.getLabelByName(labelName, False)


    def getNextLabelId(self) -> int:
        return self._executeSingle('select IFNULL(MAX(ID),0)+1 from Labels')
    
    def fetchLabelsByFileId(self, fileId:int) -> list[str]:
        vals = self._executeFetchAll(f'''SELECT Labels.ID, Labels.LABEL
                                        from  Labels,FileLabelMapper where FileLabelMapper.LABEL_ID= Labels.ID
                                        and FileLabelMapper.FILE_ID= {fileId}''')        
        logging.info(f"Fetched {len(vals)} labels for file {fileId}")
        result = []
        for item in vals:
            label = Label(item[1])
            label.id = item[0];
            result.append(label) 
        return result

    def getById(self, labelId:int) -> Label: 
        items = self._executeFetchAll(f'SELECT ID, LABEL FROM Labels where ID="{labelId}"');
        if not items:
            return None
        item = Label(items[0][1])
        item.id = items[0][0]
        return item

    def deleteLabel(self, labelId:int):
        item = self.getById(labelId)
        if not item:
            raise 'Item not found'
        if item.text.upper() == item.category.strip().upper():
            raise 'Cannot delete default label'

        tcount = self._executeUpdate(f'DELETE FROM Labels where ID={labelId}')
        logging.info(f'Deleted label {item.text}')
        return tcount