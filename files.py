import os
import shutil

sdPaths = ["/mnt/mmc/Roms","/mnt/sdcard/Roms"]

def copy_file(source_path, destination_path):
    """
    Copia un archivo desde una ruta origen a una ruta destino.
    
    Parameters:
    source_path (str): Ruta completa del archivo de origen.
    destination_path (str): Ruta completa del archivo de destino.

    Returns:
    str: Mensaje de éxito o error.
    """
    try:
        # Verificar si el archivo de origen existe
        if not os.path.exists(source_path):
            return f"Error: El archivo {source_path} no existe."
        
        # Crear directorio de destino si no existe
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Copiar archivo
        shutil.copy2(source_path, destination_path)
        return f"Archivo copiado exitosamente de {source_path} a {destination_path}."
    
    except Exception as e:
        return f"Error al copiar el archivo: {e}"

def list_filenames(path):
    try:
        # List all files in the directory
        filenames = [f for f in os.listdir(path)]
        return filenames
    except FileNotFoundError:
        print(f"Path {rom_path} does not exist.")
        return [f"Path {rom_path} does not exist."]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [f"An error occurred: {e}"]
    
def get_consoles(sdcard=0):
    return list_filenames(sdPaths[sdcard])

def get_roms(console,sdcard=0):
    return list_filenames(os.join(
        sdPaths[sdcard],
        console
    ))

def get_rom_imgs(console,sdcard=0):
    return list_filenames(os.join(
        sdPaths[sdcard],
        console,
        'Imgs'
    ))
