import os

# Function to concatenate HTML files in a directory
def concatenate_html_files(directory):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter HTML files
    html_files = [file for file in files if file.endswith('.html')]
    
    # Concatenate HTML contents with separator '::'
    concatenated_content = ''
    for html_file in html_files:
        file_path = os.path.join(directory, html_file)
        with open(file_path, 'r') as file:
            html_content = file.read()
            concatenated_content += html_content + '::'
    
    # Remove the last separator '::'
    concatenated_content = concatenated_content[:-2]
    
    return concatenated_content

# Provide the directory containing HTML files
directory = '.'  # Change this to your desired directory

# Concatenate HTML files in the directory
result = concatenate_html_files(directory)

# Print or do whatever you want with the concatenated result
print(result)
