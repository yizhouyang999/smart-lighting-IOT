p = 0
# __set__ function
def __set__(value:float) -> None:
    global p
    p = value
    
def get_proximity() -> float:	
    return p