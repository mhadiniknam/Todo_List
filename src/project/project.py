class project: 
    def __init__(self, name : str , description) -> str:
        if len(name.strip) > 30 :
            raise ValueError("Project name must be at most 30 word")
        if len(description.strip) > 150 :
            raise ValueError("Project description must be at most 150 word")
        
        self.name = name 
        self.description = description
