from Bio import Phylo
import pandas as pd
import pytaxon

def addTree(treeFilename, treeFormat = "newick"):
    
    speciesFilename = "data/species_subspeciesOnly.csv"
    #speciesDf = pd.read_excel(speciesFilename,header=0)
    speciesDf = pd.read_csv(speciesFilename,header=0)
    tree = Phylo.read(treeFilename, treeFormat)
    
    #load file with species that need to be verified
    #verificationFile = "newSpecies.xlsx"
    verificationFile = "data/newSpecies.csv"
    #treeDatasetFile = "trees.xlsx"
    treeDatasetFile = "data/trees.csv"
    
    try:
        #speciesToVerifyList = pd.read_excel(verificationFile, header=0)
        speciesToVerifyList = pd.read_csv(verificationFile, header=0)
    
    except FileNotFoundError:
        speciesToVerifyList = None
        
    leafs = tree.get_terminals()
    speciesInTreeList = ""
    
    totalNotFound = 0
    speciesToAdd = []    
    
    nanMatrix = speciesDf.isna()
    leafsInTree = 0
    
    speciesForPytaxon = []
    
    for leaf in leafs:
        speciesOfInterestName = leaf.name.replace("_"," ")
        
        #Get name from Pytaxon ASSUMING 1 SPECIES FOR NOW
        #Create dataframe with species info to create temp file for Pytaxon
        speciesRow = [None for i in range(2)]
        speciesRow[0] = speciesOfInterestName
        speciesRow[1] = speciesOfInterestName
        speciesForPytaxon.append(speciesRow)
    
    #print(f"Number of columns in speciesToAdd {len(speciesToAdd[0])}")
    speciesPytaxonDF = pd.DataFrame(speciesForPytaxon, columns=["species","scientificName"])
        
    speciesPytaxonDF.to_excel("temp/pytaxonTemp.xlsx", index=False)
        
    #Run Pytaxon
    pt = pytaxon.Pytaxon(11)
    pt.read_spreadshet("temp/pytaxonTemp.xlsx")
    pt.read_columns(f"x,x,x,x,x,x,species,scientificName")
    pt.check_species_and_lineage()     
    
    for leaf in leafs:
        speciesOfInterestName = leaf.name.replace("_"," ")
        
        originalName = speciesOfInterestName
        #Obtain new name to use
        ptData = pt._incorrect_data
        numEntries = ptData['Wrong Name'].count(speciesOfInterestName)
        
        if numEntries >= 2 and ('(' not in ptData['Suggested Name'][ptData['Wrong Name'].index(speciesOfInterestName)] and ',' not in ptData['Suggested Name'][ptData['Wrong Name'].index(speciesOfInterestName)]):
            pytaxonName = ptData['Suggested Name'][ptData['Wrong Name'].index(speciesOfInterestName)]
            
            if pytaxonName != '':
                #speciesOfInterestName = ptData['Suggested Name'][ptData['Wrong Name'].index(speciesOfInterestName)]
                speciesOfInterestName = pytaxonName            
        
        leafsInTree = leafsInTree + 1
        
        #Look for the species name in the master list as species or a protonym or a synonym
        rowsWithElementSpecies = speciesDf[speciesDf["Scientific_name"] == speciesOfInterestName]
        rowsWithElementProtonym = speciesDf[speciesDf["Protonym"] == speciesOfInterestName]
        rowsWithElementSynonym = speciesDf[speciesDf["Synonyms"].str.contains(speciesOfInterestName,na=False)]
        
        #Register tree with the species
        if len(rowsWithElementSpecies.index) > 0:
            #Add dataset to species list
            if speciesDf.at[rowsWithElementSpecies.index[0],"Tree"] == "" or nanMatrix.at[rowsWithElementSpecies.index[0],"Tree"]:
                speciesDf = speciesDf.fillna("")
                speciesDf.at[rowsWithElementSpecies.index[0],"Tree"] = treeFilename
            else:
                speciesDf.at[rowsWithElementSpecies.index[0],"Tree"] = f"{speciesDf.at[rowsWithElementSpecies.index[0],"Tree"]},{treeFilename}"
                
            if speciesInTreeList == "":
                speciesInTreeList = speciesOfInterestName
            else:
                speciesInTreeList = f"{speciesInTreeList},{speciesOfInterestName}"
                
            continue
        elif len(rowsWithElementProtonym.index) > 0:
            #Add dataset to species list
            if speciesDf.at[rowsWithElementProtonym.index[0],"Tree"] == "" or nanMatrix.at[rowsWithElementProtonym.index[0],"Tree"]:
                speciesDf = speciesDf.fillna("")
                speciesDf.at[rowsWithElementProtonym.index[0],"Tree"] = treeFilename
            else:
                speciesDf.at[rowsWithElementProtonym.index[0],"Tree"] = f"{speciesDf.at[rowsWithElementProtonym.index[0],"Tree"]},{treeFilename}"
                
            if speciesInTreeList == "":
                speciesInTreeList = speciesDf.at[rowsWithElementProtonym.index[0],"Scientific_name"]
            else:
                speciesInTreeList = f"{speciesInTreeList},{speciesDf.at[rowsWithElementProtonym.index[0],"Scientific_name"]}"
                
            continue
        elif len(rowsWithElementSynonym.index) > 0:
            #Add dataset to species list
            if speciesDf.at[rowsWithElementSynonym.index[0],"Tree"] == "" or nanMatrix.at[rowsWithElementSynonym.index[0],"Tree"]:
                speciesDf = speciesDf.fillna("")
                speciesDf.at[rowsWithElementSynonym.index[0],"Tree"] = treeFilename
            else:
                speciesDf.at[rowsWithElementSynonym.index[0],"Tree"] = f"{speciesDf.at[rowsWithElementSynonym.index[0],"Tree"]},{treeFilename}"
                
            if speciesInTreeList == "":
                speciesInTreeList = speciesDf.at[rowsWithElementSynonym.index[0],"Scientific_name"]
            else:
                speciesInTreeList = f"{speciesInTreeList},{speciesDf.at[rowsWithElementSynonym.index[0],"Scientific_name"]}"
                
            continue
        
        #Species no found so need to add it to verification list
        print(f"{speciesOfInterestName} not found in master list. \n")
        totalNotFound = totalNotFound + 1
        
        #print(f"Number of columns in speciesToAdd {len(speciesToAdd[-1])}")
        if speciesToVerifyList is None:
            #latestSequence = latestSequence + 1
            speciesRow = [None for i in range(len(speciesDf.columns) + 1)]
            #speciesRow[0] = latestSequence
            speciesRow[0] = -1
            speciesRow[5] = speciesOfInterestName
            speciesRow[28] = treeFilename
            speciesRow[29] = originalName
            
            speciesToAdd.append(speciesRow)
        
        else:
            nanMatrixVerifySpecies = speciesToVerifyList.isna()
            rowsVerifySpecies = speciesToVerifyList[speciesToVerifyList["Scientific_name"] == speciesOfInterestName]
            
            if len(rowsVerifySpecies.index) > 0:
                if speciesToVerifyList.at[rowsVerifySpecies.index[0],"Tree"] == '' or nanMatrixVerifySpecies.at[rowsVerifySpecies.index[0],"Tree"]:
                    speciesToVerifyList = speciesToVerifyList.fillna("")
                    speciesToVerifyList.at[rowsVerifySpecies.index[0],"Tree"] = treeFilename
                else:
                    speciesToVerifyList.at[rowsVerifySpecies.index[0],"Tree"] = f"{speciesToVerifyList.at[rowsVerifySpecies.index[0],"Tree"]},{treeFilename}"
                
            else:
                #latestSequence = latestSequence + 1
                speciesRow = [None for i in range(len(speciesDf.columns) + 1)]
                #speciesRow[0] = latestSequence
                speciesRow[0] = -1
                speciesRow[5] = speciesOfInterestName
                speciesRow[28] = treeFilename
                speciesRow[29] = originalName
                
                speciesToAdd.append(speciesRow)
                
    print(f"Total species not found: {totalNotFound}")
    print(f"Total species in tree: {leafsInTree}")
    #Add tree to tree dataset
    treeRow = [treeFilename,"",speciesInTreeList]
    
    try:
        #treesList = pd.read_excel(treeDatasetFile, header=0)
        treesList = pd.read_csv(treeDatasetFile, header=0)
        
        treesList = pd.concat([treesList,pd.DataFrame([treeRow], columns=["treeName","treeLocation","speciesIncluded"])], ignore_index=True)
        
    except FileNotFoundError:
        treesList = pd.DataFrame([treeRow], columns=["treeName","treeLocation","speciesIncluded"])    
        
    #treesList.to_excel(treeDatasetFile, index=False)
    treesList.to_csv(treeDatasetFile, index=False)
    
    frameColumns = speciesDf.columns.tolist()
    frameColumns.append("speciesDatasetName")    
    
    #print(f"Number of columns in speciesToAdd {len(speciesToAdd[-1])}")
    if speciesToVerifyList is not None:
        speciesToVerifyList = pd.concat([speciesToVerifyList, pd.DataFrame(speciesToAdd, columns=speciesToVerifyList.columns)], ignore_index=True)
    
    else:
        speciesToVerifyList = pd.DataFrame(speciesToAdd, columns=frameColumns)
        
    #speciesToVerifyList.to_excel(verificationFile, index=False)
    speciesToVerifyList.to_csv(verificationFile, index=False)
    
    #speciesDf.to_excel(speciesFilename, index=False)
    speciesDf.to_csv(speciesFilename, index=False)
    
#def main():
    #addTree("BBtreeC2022.tre","species_subspeciesOnly.csv")
    #addTree("new_tree.nwk","species_subspeciesOnly.csv")
        
#tree = Phylo.read("BBtreeC2022.tre","newick")
#print(tree)
#terminals = tree.get_terminals()
#print("Rhea_americana" == terminals[1].name)
#test = terminals[1].name
#test = test + "a"
#print(test)
#main()