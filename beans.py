from cProfile import label


class FileInfo(object):
    def __init__(self,category:str,imagefile:str, vectorfile:str) -> None:
        self.imageFile = imagefile;
        self.vectorFile = vectorfile;
        self.category = category;
        self.createdOn = None
        self.id = 0;
        self.labels = []
    def __str__(self) -> str:
        return f'''id:{self.id},Category:{self.category},ImageFile:{self.imageFile},vector:{self.vectorFile}, 
        createdOn:{self.createdOn}, Labels: {self.labels}'''

class Label(object):
    def __init__(self, text:str):
        self.text = text;
        self.id = 0
    def __str__(self) -> str:
        return f'id:{self.id}, label:{self.text}'
