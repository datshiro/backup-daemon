import os
import zipfile
import time
import settings

class Config(dict):
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj,key)


class BackupApp:
    default_config = dict({
        'SOURCE_PATH':      None,
        'DESTINATION_PATH': None,
        'OUTPUT':           "Backup.zip",
    })

    root_path = os.path.abspath(os.path.dirname(__file__))
    config_class = Config
    
    def __init__(self):
        self.config = self.make_config()
        self.output = self.config['OUTPUT']
            
        if self.config['DESTINATION_PATH'] is None:
            self.config['DESTINATION_PATH'] = self.root_path


    def make_config(self):
        defaults = dict(self.default_config)
        return self.config_class(defaults)


    def zip_dir(self, dir_path, *args, **kwargs):
        list_files = os.scandir(dir_path)
        for file in list_files:
            try:
                self.ZIP_HANDLER.write(os.path.relpath(file.path))
                if file.is_dir():
                    self.zip_dir(dir_path=file.path)
            except PermissionError:
                print("---Permission Denied---: ", file.path)
        list_files.close()


    def backup_dir(self):
        source = self.config['SOURCE_PATH']
        dst = self.config['DESTINATION_PATH']
        if not os.path.exists(source):
            print(source + " is not a directory!")
            return False

        try:
            os.makedirs(dst)
        except FileExistsError:
            if(os.path.isfile(dst)):
                print(dst + " is not a directory!")
                return False
        output_path = os.path.join(dst, self.config['OUTPUT'])
        self.ZIP_HANDLER = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        os.chdir(source)       # This is need for get relative path 
        print("Start Zip ", time.ctime())
        self.zip_dir(dir_path=source)
        print("End Zip ", time.ctime())

    def close(self):
        self.ZIP_HANDLER.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ZIP_HANDLER.close()

# Call os.stat(entry.path) to update os.DirEntry objects

if __name__ == '__main__':
    with BackupApp() as app:
        app.config.from_object(settings)
        app.backup_dir()