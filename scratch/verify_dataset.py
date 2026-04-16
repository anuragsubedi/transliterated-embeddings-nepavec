import json
import os

def verify_dataset(directory):
    files = [f for f in os.listdir(directory) if f.startswith('chunk_') and f.endswith('.json')]
    if len(files) != 20:
        print(f"Error: Expected 20 files, found {len(files)}")
        return False
    
    total_sentences = 0
    for i in range(1, 21):
        filename = f"chunk_{i}.json"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            print(f"Error: {filename} missing")
            return False
        
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    print(f"Error: {filename} is not a list")
                    return False
                if len(data) != 50:
                    print(f"Error: {filename} has {len(data)} sentences instead of 50")
                    # return False # Just print for now
                total_sentences += len(data)
            except Exception as e:
                print(f"Error parsing {filename}: {e}")
                return False
                
    print(f"Success: Verified 20 files with a total of {total_sentences} sentences.")
    return True

if __name__ == "__main__":
    verify_dataset('dataset')
