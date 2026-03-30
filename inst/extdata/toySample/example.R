library(traitR)

#Run these lines only for setup
setup = TRUE

if (setup){
  createDatabase()

  addDataset("traitRExample/Rawdata_updated_2.csv","csv","Example data","Species_Scientific")

  addTree("traitRExample/phylogenetic_tree.tre","newick")
}

speciesExample <- speciesInTrees("traitRExample/phylogenetic_tree.tre")
speciesExampleString <- paste(speciesExample,collapse=",")
traitsExample <- traitsInDatasets("Example data")
traitsExampleString <- paste(traitsExample, collapse = ",")

results <- traitSearch(speciesExampleString,traitsExampleString,"Example data")
