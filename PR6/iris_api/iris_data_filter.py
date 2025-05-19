import pandas as pd

class IrisDataFilter:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self.df.columns = [col.strip() for col in self.df.columns]

        # Clean species column for consistent matching
        self.df['Species_clean'] = (
            self.df['Species']
            .str.strip()
            .str.lower()
            .str.replace('-', '', regex=False)
            .str.replace(' ', '', regex=False)
        )

    def filter_by_species(self, species: str):
        if species.lower() == 'all':
            return self.df

        # Allow short names for species
        species_lookup = {
            'setosa': 'iris-setosa',
            'versicolor': 'iris-versicolor',
            'virginica': 'iris-virginica'
        }

        species = species.strip().lower().replace('-', '').replace(' ', '')
        full_species = species_lookup.get(species, species)

        # Normalize the species name for consistent matching
        normalized_species = full_species.replace('-', '').replace(' ', '').lower()

        return self.df[self.df['Species_clean'] == normalized_species]
