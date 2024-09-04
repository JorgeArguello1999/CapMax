from modules import google_vision as gv
import os 

# rename all files 
dir_path = '../uploads/'
files = os.listdir(dir_path)

def rename_files():
    counter = 0
    for file in files:
        # Get the file extension
        file_ext = os.path.splitext(file)[1]

        # Create the new file name
        new_file_name = f'test_{counter}{file_ext}'

        # Rename the file
        os.rename(os.path.join(dir_path, file), os.path.join(dir_path, new_file_name))

        # Increment the counter
        counter += 1
    
def create_test_files():
    for file in files:
        content = gv.text_detect(f'uploads/{file}')
        with open(f'test/{file}.txt', "w") as doc:
            doc.write(content)

if __name__ == "__main__":
    create_test_files()