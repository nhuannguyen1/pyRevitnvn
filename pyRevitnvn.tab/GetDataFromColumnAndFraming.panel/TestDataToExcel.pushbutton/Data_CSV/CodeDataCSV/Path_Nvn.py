def resource_path(self):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = self.dir_path + self.FolderName 
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, self.FileName)
    # Extract file name from path, no matter what the os/path format
def ExtractFileNameFromPath (self):
        # get file Name
    FileName = os.path.basename(self.Path)
    return FileName