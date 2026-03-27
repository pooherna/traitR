import os 
import pandas as pd

from pathlib import Path
from speciesLoader import createDatabase 

def testDataset() -> object :
	"""
	Returns the first 100 records from the Aves data.

	Returns: 
		Pandas DataFrame object.

	"""

	extdata_path = os.path.join(Path(__file__).resolve().parent.parent, "extdata")
	aves_file = os.path.join(extdata_path, "AviList-v2025-11Jun-extended.xlsx")
	df = pd.read_excel(aves_file)
	df = df.fillna("")
	df['Synonyms'] = None
	df['Dataset'] = None
	df['Tree'] = None
	return df.head(100)


def testDatabase() -> None:
	"""
	Creates a sample database with Aves data.

	Returns:
		None
	"""
	createDatabase(taxa='Aves')


if __name__ == "__main__":
	df = testDataset()
	print(df)

	testDatabase()