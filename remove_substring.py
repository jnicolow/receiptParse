import os

def remove_substring(directory, substring):
    # Get the list of files in the directory
    files = os.listdir(directory)

    # Iterate through each file in the directory
    for filename in files:
        # Construct the full path of the file
        filepath = os.path.join(directory, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(filepath):
            # Remove the specified substring from the filename
            new_filename = filename.replace(substring, '')

            # Construct the new full path with the modified filename
            new_filepath = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(filepath, new_filepath)

            print(f'Renamed: {filename} -> {new_filename}')

# Example usage:
directory_path = 'data/receipts/json/prompt2'
substring_to_remove = '_prompttemplate2'

remove_substring(directory_path, substring_to_remove)

