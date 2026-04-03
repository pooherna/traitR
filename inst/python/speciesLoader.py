import os 
import pandas as pd
from pathlib import Path

home = Path.home()
traitRPath = home/"traitR"

from pathlib import Path

def createDatabase(taxa: str, custom_file: str = "", species_name_col: str = "Scientific_name") -> bool:
    """
    Creates 'species_masterlist.csv' file in the database.
    
    Args:
        taxa: species to load in the database; one of 'Aves', 'Mammalia', 'Custom'...
        custom_file: path to the custom csv file to be used as masterlist; specify only when taxa='Custom'
        species_name_col: custom species_name column in the custom csv file; specify only when taxa='Custom'
    
    Returns:
        True if new 'species_masterlist.csv' file was created; False otherwise, i.e., file exists.    
    """
    extdata_path = os.path.join(Path(__file__).resolve().parent.parent, "extdata")
    SUPPORTED_TAXA = {
        "Aves": os.path.join(extdata_path, "AviList-v2025-11Jun-extended.xlsx"),
        "Custom": None
    }

    # Checkpoint 1: taxa argument validity
    if taxa not in SUPPORTED_TAXA:
        raise ValueError(f"Unsupported taxa: {taxa}")

    if taxa == 'Custom':
        # Checkpoint 2: custom_file argument validity
        if not custom_file:
            raise ValueError(f"Missing custom_file parameter")

        # Checkpoint 3: custom_file file existence 
        if not Path(custom_file).is_file():
            raise FileNotFoundError(f"The specified custom_file was not found: {custom_file}")

    # Set masterlist file
    if taxa == 'Custom':
        masterlist_file = custom_file
    else:
        masterlist_file = SUPPORTED_TAXA[taxa]

    # Checkpoint 4: masterlist_file file type
    _, ext = os.path.splitext(masterlist_file)
    if ext not in [".csv", ".xlsx"]:
        raise ValueError(f"File format not supported (.csv, .xlsx only): {masterlist_file}")

    # Checkpoint 5: db/species_masterlist.csv file existence
    current_dir = os.getcwd()
    db_path = os.path.join(current_dir, "db")
    species_masterlist_file = os.path.join(db_path, "species_masterlist.csv")
    if Path(species_masterlist_file).is_file():
        print("Database has already been set-up. No operations performed.")
        return False
    
    else:
        # Read the custom file
        if ext == ".csv":
            df = pd.read_csv(masterlist_file)
        elif ext == ".xlsx":
            df = pd.read_excel(masterlist_file)

        # Checkpoint 6: check species_column_name existence in df.columns
        if taxa == 'Custom':
            if species_name_col not in df.columns:
                raise ValueError(f"Specified species_name_col not in dataframe: {species_name_col}")
        
            if species_name_col != "Scientific_name":
                df = df.rename(columns={species_name_col: "Scientific_name"})
        
        # NOTE: The extdata files can already be pre-formatted so that
        # using them only involves copying the files into the current 
        # working directory. This will result in the removal of the 
        # formatting code below.

        # Fill null with empty string 
        df = df.fillna("")
        
        # Format Scientific_name
        df['Scientific_name'] = df['Scientific_name'].apply(lambda name: name.replace("_", " "))

        # Add columns: Synonyms, Dataset, Tree
        df['Synonyms'] = None
        df['Dataset'] = None
        df['Tree'] = None
        
        # Save 'species_masterlist.csv'
        df.to_csv(os.path.join(db_path, "species_masterlist.csv"), index=False)
        return True


if __name__ == '__main__': 
    # status = createDatabase(taxa="Mammalia") # => Unsupported taxa
    # status = createDatabase(taxa="Custom") # => Missing custom_file parameter
    # status = createDatabase(taxa="Custom", custom_file="blink.csv") # => The specified custom_file was not found
    # status = createDatabase(
    #     taxa="Custom", 
    #     custom_file="/Users/jimuelcelestejr/Downloads/1-s2.0-S2772442524000224-main.pdf" # random file
    # ) # => File format not supported
    # status = createDatabase(taxa="Aves") # => Database has already been set-up. No operations performed.
    # status = createDatabase(
    #     taxa="Custom", 
    #     custom_file="/Users/jimuelcelestejr/Documents/codebook/traitR/inst/extdata/mdd.csv",
    #     species_name_col="Name"
    # ) # => Specified species_name_col not in dataframe
    status = createDatabase(taxa="Aves") # => Successful; predefined dataset
    # status = createDatabase(
    #     taxa="Custom", 
    #     custom_file="/Users/jimuelcelestejr/Documents/codebook/traitR/inst/extdata/mdd.csv",
    #     species_name_col="sciName"
    # ) # => Successful; custom dataset

    # print(status)


def loadSpecies(filename,column_name,column_category):

    species = "species"
    subspecies = "subspecies"
    
    df = pd.read_excel(filename,header=0)
    
    #print(f"Data example: {df.at[1,"Taxon_rank"]}")
    
    #(f"Finding data for Struthio molybdophanes: {df[df["Scientific_name"] == "Struthio molybdophanes"]}")
    
    df.insert(len(df.columns),"Synonyms",[""] * len(df.index))
    
    #Check if species list has a dataset column, if not create it
    if "Dataset" not in df.columns:
        df.insert(len(df.columns),"Dataset",[""] * len(df.index))    
        
    #Check if species list has a tree column, if not create it
    if "Tree" not in df.columns:
        df.insert(len(df.columns),"Tree",[""] * len(df.index))        
    
    total = 0
    
    for element in df.index:
        
        total = element
        df.at[element,"Synonyms"] = df.at[element,"Protonym"]
        
        if df.at[element,column_category] != species and df.at[element,column_category] != subspecies:
            df = df.drop(element)
            #print(f"Dropping {element}")
    
    #df.to_excel("species_subspeciesOnly.xlsx", index=False)
    
    #dfMammals = pd.read_csv("mdd.csv", header=0, encoding='latin1') 
    dfMammals = pd.read_csv("Species_Scientific.csv", header=0, encoding='latin1') 
    
    #mammalSpeciesName = dfMammals['sciName'].tolist()
    mammalSpeciesName = dfMammals['Species_Scientific'].tolist()
    mammalSpeciesName = [species.replace("_", " ") for species in mammalSpeciesName]
    
    total = total + 1
    
    for species in mammalSpeciesName:
        #speciesOfInterestName = leaf.name.replace("_"," ")
        total = total + 1
        
        originalName = species
        
        #latestSequence = latestSequence + 1
        speciesRow = [None for i in range(len(df.columns))]
        #speciesRow[0] = latestSequence
        speciesRow[0] = total
        speciesRow[5] = species
            
        #speciesToAdd.append(speciesRow)
        df = pd.concat([df,pd.DataFrame([speciesRow], columns=["Sequence","Taxon_rank","Order","Family","Family_English_name","Scientific_name","Authority","Bibliographic_details","English_name_AviList","English_name_Clements_v2024","English_name_BirdLife_v9","Proposal_number","Decision_summary","Range","Extinct_or_possibly_extinct","IUCN_Red_List_Category","BirdLife_DataZone_URL","Species_code_Cornell_Lab","Birds_of_the_World_URL","AvibaseID","Gender_of_genus","Type_species_of_genus","Type_locality","Title_of_original_description","Original_description_URL","Protonym","Synonyms","Dataset","Tree"])], ignore_index=True)
    
    df.to_csv(traitRPath/"db"/"species_subspeciesOnly.csv", index=False)
    
#def main():
    
    #filename = input("Enter filename of species dataset: ")
    
    #column_name = input("Enter the header name of the column containing the species name: ")
    
    #column_category = input("Enter the header name of the column containing the category, if no column exist enter NONE: ")
    
    #loadSpecies(filename,column_name,column_category)

#loadSpecies("AviList-v2025-11Jun-extended.xlsx","Scientific_name","Taxon_rank")    
#main()