import requests as rq
from sys import stdout
from pathlib import Path
import re
import os

class Downloader:
    """
    class do manage downloading url links
    """
    def __init__(self, *args, session=None): # creates a session
        self.cwd = Path.cwd()
        self.src_path = Path(__file__)
        if not session:
            self.session = rq.Session()
        else:
            self.session = session
        # super().__init__(*args, **kwargs)

    def _get_bar(self, progress):
        """
        progress must be between 0 and 1\n 
        Returns the bar with current progress as a string
        """
        FULL_BLOCKLENGTH = 32
        fillblock = '█'

        blocks = int(progress / (1/FULL_BLOCKLENGTH))
        bar_start = '\r'+fillblock*blocks
        bar_end = (33 - len(bar_start))*'_'+'|'
        if progress > 1:
            progress = 1
        bar_percent = f' {progress*100:0.2f} % '
        text = bar_start+bar_end+bar_percent
        return text
    
    def _make_name(self, url_path: Path, name_in: str):
        """
        Parses the name and returns a writebale name
        """
        try:
            # clean_name = re.search(r'\w+',name_in).group() # parsing name, only alphanumeric, no whitespace
            name = re.split(r'[.]\w+$',name_in)[0] # name without extension
            clean_name = ' '.join(re.findall(r'\w+',name)) # parsing name, only alphanumeric, no whitespace
                
        except :
            print('illegal name, taking name from url')
            return url_path.name
        try:
            # extension = re.search(r'(?<=[.]\w+$)', name_in).group() # matching only extension after last "."
            extension = name_in.split('.')[-1] # matching only extension after last "."
        except:
            extension = None
        if extension:
            name_path = Path(f'{clean_name}.{extension}') # custom extension specified and not in the name
        else:
            name_path = Path(f'{clean_name}{url_path.suffix}') # extension from url
        return name_path.name


    def download(self, url, d_path=None, name_out=None):
        """
        downloads from url

        `d_path`: default download path is current working directory
        
        `name_out`: default name will be the tail of the url address
                can take in a name with or without extension(takes extension from url)
        """
        url_path = Path(url)
        #download_path = self.cwd / url_path.name if not d_path else Path(d_path)
        if not name_out:
            name_out = url_path.name
        else:
            name_out = self._make_name(url_path, name_out)

        if not d_path:
            # download_path = self.src_path.parent
            download_path = self.cwd
        else:
            download_path = Path(d_path)

        # making file path
        save_file = download_path / name_out 
        # checking if file already is there
        if save_file.exists():
            print('skipping', save_file.name)
            return

        r = self.session.get(url)

        size = float(r.headers['content-length'])
        with open(save_file.absolute(), 'wb') as fd:
            tmp = 0
            print(f'Downloding: {save_file.name}')
            print(f'to {save_file.absolute()}')
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    fd.write(chunk)
                    tmp += 1024
                    bar = self._get_bar(tmp / size)
                    output = f'\r{bar} {tmp/1000000:0.2f} / {size/1000000:0.2f} MB'
                    stdout.write(output)
            print('')
            print('Done')

def input_loop():
    while True:
        inp = input('Download path:\n')
        if _test_write(inp): return inp
        #try:
        #    d_path = Path(inp)
        #except Exception as e:
        #    print('invalid path, try again\n')
        #    continue
        #if d_path.exists(): return d_path

def name_loop():
    while True:
        inp = input('Name:\n')
        return inp

def _test_write(path):
    ''' writes a file to the path and returns True if it succeded '''
    writable = False
    try:
        p = Path(path)
        test_file = p / 'testfile.testfile'
        with open(test_file, 'wb') as f:
                f.write(bytes(0))
        writable = True
    except Exception as e:
        print('write test failed: ',e)
        return
    finally:
        try:
            os.remove(test_file)
        except Exception as e:
            #print('deleting test write failed: ',e) 
            pass
        return writable

if __name__ == "__main__":
    d_path = input_loop() #let user decide where to download
    name = name_loop() # let user decide what name it will have
    d = Downloader()
    #d_path = input('download path:')
    d.download('http://i.4cdn.org/gif/1556302608616.webm',d_path, name)