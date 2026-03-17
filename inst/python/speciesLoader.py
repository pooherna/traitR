import pandas as pd

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
    
    for element in df.index:
        
        df.at[element,"Synonyms"] = df.at[element,"Protonym"]
        
        if df.at[element,column_category] != species and df.at[element,column_category] != subspecies:
            df = df.drop(element)
            #print(f"Dropping {element}")
    
    #df.to_excel("species_subspeciesOnly.xlsx", index=False)
    df.to_csv("data/species_subspeciesOnly.csv", index=False)
    
#def main():
    
    #filename = input("Enter filename of species dataset: ")
    
    #column_name = input("Enter the header name of the column containing the species name: ")
    
    #column_category = input("Enter the header name of the column containing the category, if no column exist enter NONE: ")
    
    #loadSpecies(filename,column_name,column_category)

#loadSpecies("AviList-v2025-11Jun-extended.xlsx","Scientific_name","Taxon_rank")    
#main()