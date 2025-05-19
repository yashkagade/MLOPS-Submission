import pandas as pd

class ChunkIterator:
    def __init__(self, file_path, chunk_size=100):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_iterator = pd.read_csv(self.file_path, chunksize=self.chunk_size)
    
    def get_chunk(self):
        """Return the next chunk of data."""
        try:
            return next(self.chunk_iterator)
        except StopIteration:
            return None  # No more chunks
    
    def calculate_chunk_statistics(self, chunk):
        """Calculate and return basic statistics for the given chunk."""
        # Basic statistics for the chunk
        stats = {
            "mean_income": chunk['Annual Income (k$)'].mean(),
            "mean_spending_score": chunk['Spending Score (1-100)'].mean(),
            "count": chunk.shape[0],
            "min_age": chunk['Age'].min(),
            "max_age": chunk['Age'].max()
        }
        return stats

    def process_chunks(self):
        """Process the dataset in chunks and calculate statistics."""
        all_stats = []
        
        while True:
            chunk = self.get_chunk()
            if chunk is None:
                break  # No more data
            
            stats = self.calculate_chunk_statistics(chunk)
            all_stats.append(stats)
        
        return all_stats

# ✅ Use the class with the full path to the dataset
file_path = r"C:\Users\User\OneDrive\Desktop\MlOps Assignments\python\assign_4\Mall_Customers.csv"  # Update with your actual file path

# Create an instance of the ChunkIterator with your file path and a desired chunk size
chunk_iterator = ChunkIterator(file_path, chunk_size=100)

# Process the chunks and get statistics
all_chunk_stats = chunk_iterator.process_chunks()

# Print statistics for each chunk
for i, stats in enumerate(all_chunk_stats):
    print(f"Chunk {i+1} statistics: {stats}")
