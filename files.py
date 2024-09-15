import os
import shutil

sdPaths = ["/mnt/mmc/Roms", "/mnt/sdcard/Roms"]

def copy_file(source_path, destination_path):
    """
    Copies a file from the source path to the destination path.

    Parameters:
    source_path (str): Full path of the source file.
    destination_path (str): Full path of the destination file.

    Returns:
    str: Success or error message.
    """
    try:
        # Check if the source file exists
        if not os.path.exists(source_path):
            return f"Error: The file {source_path} does not exist."
        
        # Create the destination directory if it does not exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Copy the file
        shutil.copy2(source_path, destination_path)
        return f"File successfully copied from {source_path} to {destination_path}."
    
    except Exception as e:
        return f"Error copying the file: {e}"

def list_filenames(path):
    """
    Lists all files in the directory.

    Parameters:
    path (str): Directory path.

    Returns:
    list: List of filenames in the directory or an error message.
    """
    try:
        # List all files in the directory
        filenames = [f for f in os.listdir(path) if not os.path.isdir(os.path.join(path, f))]
        return filenames
    except FileNotFoundError:
        print(f"Path {path} does not exist.")
        return [f"Path {path} does not exist."]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [f"An error occurred: {e}"]

def list_directories(path):
    """
    Lists all directories in the directory.

    Parameters:
    path (str): Directory path.

    Returns:
    list: List of directories in the directory or an error message.
    """
    try:
        # List all directories in the directory
        directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return directories
    except FileNotFoundError:
        print(f"Path {path} does not exist.")
        return [f"Path {path} does not exist."]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [f"An error occurred: {e}"]

def get_consoles(sdcard=0):
    """
    Gets the list of console directories.

    Parameters:
    sdcard (int): SD card index.

    Returns:
    list: List of console directories.
    """
    return list_directories(sdPaths[sdcard])

def get_roms(console, sdcard=0):
    """
    Gets the list of ROM files for a given console.

    Parameters:
    console (str): Console directory name.
    sdcard (int): SD card index.

    Returns:
    list: List of ROM files for the console.
    """
    return list_filenames(os.path.join(sdPaths[sdcard], console))

def get_rom_imgs(console, sdcard=0):
    """>
    Gets the list of image files for a given console.

    Parameters:
    console (str): Console directory name.
    sdcard (int): SD card index.

    Returns:
    list: List of image files for the console.
    """
    return list_filenames(os.path.join(sdPaths[sdcard], console, 'Imgs'))

def filter_empty_directories(directories,sdcard=0):
    non_empty_dirs = []
    for directory in directories:
        full_path = os.path.join(sdPaths[sdcard], directory)
        if list_filenames(full_path):
            non_empty_dirs.append(directory)
    return non_empty_dirs