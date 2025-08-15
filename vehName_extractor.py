import os
import re
from pathlib import Path

class VehiclesMetaExtractor:
    def __init__(self, base_directories=None):
        # Handle both single directory (string) and multiple directories (list)
        if base_directories is None:
            self.base_directories = ["emergency"]
        elif isinstance(base_directories, str):
            self.base_directories = [base_directories]
        else:
            self.base_directories = base_directories
        self.results = []
    
    def find_vehicles_meta_files(self):
        """Find all vehicles.meta files in all specified directories and their subdirectories"""
        meta_files = []
        
        for base_directory in self.base_directories:
            if not os.path.exists(base_directory):
                print(f"Warning: Directory '{base_directory}' not found! Skipping...")
                continue
            
            print(f"Searching in directory: {base_directory}")
            
            # Walk through all directories and subdirectories
            for root, dirs, files in os.walk(base_directory):
                for file in files:
                    if file.lower() == 'vehicles.meta':
                        file_path = os.path.join(root, file)
                        # Get the folder name (parent directory of the file)
                        folder_name = os.path.basename(root)
                        # Get relative path from the base directory for better identification
                        relative_path = os.path.relpath(file_path, base_directory)
                        meta_files.append({
                            'folder': folder_name,
                            'file_path': file_path,
                            'relative_path': relative_path,
                            'base_directory': base_directory
                        })
        
        return meta_files
    
    def extract_model_names(self, file_path):
        """Extract all modelName values from vehicles.meta files"""
        model_names = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all <modelName> to </modelName> sections 
            modelName_pattern = r'<modelName>(.*?)</modelName>'
            modelName_matches = re.findall(modelName_pattern, content, re.DOTALL)
            
            for match in modelName_matches:
                cleaned_match = match.strip()
                if cleaned_match:
                    model_names.append(cleaned_match)
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        return model_names
    
    def process_all_files(self):
        """Process all vehicles.meta files and extract ID values"""
        meta_files = self.find_vehicles_meta_files()
        
        if not meta_files:
            print("No vehicles.meta files found!")
            return
        
        print(f"Found {len(meta_files)} vehicles.meta files")
        print("Processing files...\n")
        
        for meta_info in meta_files:
            model_names = self.extract_model_names(meta_info['file_path'])
            
            if model_names:
                for model_name in model_names:
                    result = {
                        'folder': meta_info['folder'],
                        'file_path': meta_info['relative_path'],
                        'model_name': model_name,
                        'base_directory': meta_info['base_directory']
                    }
                    self.results.append(result)
                    print(f"Directory: {meta_info['base_directory']} | Folder: {meta_info['folder']} | ID: {model_name}")
            # Removed the else block - no longer prints folders with no ID values found
        
        print(f"\nTotal ID values extracted: {len(self.results)}")
    
    def alphabetical_sort_key(self, text):
        """Generate a key for alphabetical sorting"""
        return text.lower()
    
    def save_to_txt(self, output_file="veh_spawncodes.txt"):
        """Save extracted data to text file"""
        if not self.results:
            print("No data to save!")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("vehicles.meta Model Names Extraction Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Group by folder for cleaner output
            folders = {}
            for result in self.results:
                folder = result['folder']
                if folder not in folders:
                    folders[folder] = []
                folders[folder].append(result['model_name'])
            
            # Write grouped results (only sort IDs within each folder)
            for folder, ids in folders.items():
                sorted_ids = sorted(ids, key=lambda x: x.lower())
                f.write(f"Folder: {folder}\n")
                f.write("-" * 30 + "\n")
                for id_value in sorted_ids:
                    f.write(f"ID: {id_value}\n")
                f.write("\n")
            
            # Write summary
            f.write("=" * 50 + "\n")
            f.write(f"Total folders processed: {len(folders)}\n")
            f.write(f"Total ID values found: {len(self.results)}\n")
        
        print(f"\nResults saved to {output_file}")
    
    def check_for_duplicates(self):
        """Check for duplicate ID values and return duplicate info"""
        id_map = {}
        duplicates = {}
        
        # Build a map of ID values to their locations
        for result in self.results:
            id_value = result['model_name']
            if id_value not in id_map:
                id_map[id_value] = []
            id_map[id_value].append(result)
        
        # Find duplicates
        for id_value, locations in id_map.items():
            if len(locations) > 1:
                duplicates[id_value] = locations
        
        return duplicates
    
    def save_simple_format(self, output_file="veh_spawncodes_simple.txt"):
        """Save in simple format: id_value | folder_name (sorted by ID numerically)"""
        if not self.results:
            print("No data to save!")
            return
        
        # Sort results by ID value numerically
        sorted_results = sorted(self.results, key=lambda x: self.alphabetical_sort_key(x['model_name']))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in sorted_results:
                f.write(f"{result['model_name']}\n")
        
        print(f"Simple format saved to {output_file}")
    
    def save_duplicates_report(self, output_file="duplicateveh_ids.txt"):
        """Save duplicate ID values report (IDs sorted numerically)"""
        duplicates = self.check_for_duplicates()
        
        if not duplicates:
            print("No duplicate ID values found!")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("DUPLICATE ID VALUES REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            # Sort duplicate IDs numerically
            for id_value in sorted(duplicates.keys(), key=self.alphabetical_sort_key):
                locations = duplicates[id_value]
                f.write(f"ID: {id_value} (found {len(locations)} times)\n")
                f.write("-" * 30 + "\n")
                for location in locations:
                    f.write(f"  Folder: {location['folder']}\n")
                    f.write(f"  Path: {location['file_path']}\n")
                f.write("\n")
            
            f.write("=" * 50 + "\n")
            f.write(f"Total duplicate IDs: {len(duplicates)}\n")
            total_duplicates = sum(len(locations) for locations in duplicates.values())
            f.write(f"Total duplicate instances: {total_duplicates}\n")
        
        print(f"Duplicate report saved to {output_file}")
        print(f"Found {len(duplicates)} duplicate IDs with {sum(len(locations) for locations in duplicates.values())} total instances")

def main():
    # Initialize the extractor with multiple directories
    # You can specify multiple directories like this:
    directories_to_search = [
        "[emergency]",
        "[Vehicles]",
    ]
    
    # Or use a single directory:
    # directories_to_search = "[emergency]"
    
    extractor = VehiclesMetaExtractor(directories_to_search)
    
    # Process all vehicle.meta files
    extractor.process_all_files()
    
    # Save results to text files
    extractor.save_to_txt()
    extractor.save_simple_format()
    
    # Check for and save duplicate IDs
    extractor.save_duplicates_report()

if __name__ == "__main__":
    main()
