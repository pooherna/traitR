from pathlib import Path
import shutil

def folderSetup():
    
    home = Path.home()
    traitRPath = home/"traitR"
    
    if traitRPath.exists():
        
        print(f"traitR already exists")
    else:
        print(f"{traitRPath} needs to be created")
        traitRPath.mkdir(parents=True, exist_ok=True)
        
        dbPath = traitRPath/"db"
        outPath = traitRPath/"out"
        tempPath = traitRPath/"temp"
        
        dbPath.mkdir(parents=True, exist_ok=True)
        outPath.mkdir(parents=True, exist_ok=True)
        tempPath.mkdir(parents=True, exist_ok=True)
        print(f"traitR data files can be found in '{traitRPath}'")
        
def reset():
    home = Path.home()
    traitRPath = home/"traitR"
    
    try:
        shutil.rmtree(traitRPath)
    except FileNotFoundError:
        print(f"Directory {traitRPath} does not exist")
        
    folderSetup()
#reset()