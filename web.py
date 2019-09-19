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
    
    def _print_progress(self, current_bytes, size):
        bar = self._get_bar(current_bytes / size)
        output = f'\r{bar} {current_bytes/1000000:0.2f} / {size/1000000:0.2f} MB'
        stdout.write(output)
        # stdout.flush()

    def _get_bar(self, progress):
        """
        progress must be between 0 and 1\n 
        Returns the bar with current progress as a string
        """
        FULL_BLOCKLENGTH = 32
        fillblock = '█'

        if progress > 1:
            progress = 1
        blocks = int(progress / (1/FULL_BLOCKLENGTH))
        bar_start = fillblock*blocks
        bar_end = (33 - len(bar_start))*'_'+'|'
        bar_percent = f' {progress*100:0.2f} % '
        text = bar_start+bar_end+bar_percent
        return text
    
    def _make_name(self, url_path: Path, name_in: str):
        """
        Parses the name and returns a writebale name
        """
        # in case its a number and  not None
        if name_in and name_in != type(str):
            name_in = str(name_in)

        try:
            name_in[0] # if its empty it raises exception
            # clean_name = re.search(r'\w+',name_in).group() # parsing name, only alphanumeric, no whitespace
            # name = re.split(r'[.].+$',name_in)[0] # name without extension
            name_parts = name_in.split('.') # name without extension
            if len(name_parts) > 1:
                name_noext = '.'.join(name_parts[:-1]) # joining together without extension
            else:
                name_noext = name_parts[0]
            clean_name = ' '.join(re.findall(r'\w+.+',name_noext)) # parsing name, only alphanumeric, no whitespace
            clean_name[0] # empty testing
        except :
            print('invalid name, taking name from url')
            name = re.split(r'[?]',url_path.name)[0] # if '?' in url, get rid of it
            return name
        try:
            extension = re.search(r'(?<=[.])\w+$', name_in).group() # matching only extension after last "."
            # extension = name.split('.')[-1] # matching only extension after last "."
        except:
            extension = None
        if extension:
            name_path = Path(f'{clean_name}.{extension}') # custom extension specified and not in the name
        else:
            name = re.split(r'[?]',url_path.name)[0] # if '?' in url, get rid of it
            extension = re.search(r'(?<=[.])\w+$', name).group() # matching only extension after last "."
            name_path = Path(f'{clean_name}.{extension}') # extension from url
        return name_path.name


    def download(self, url, d_path=None, name_out=None, printprogess=False):
        """
        downloads from url

        `d_path`: default download path is current working directory
        
        `name_out`: default name will be the tail of the url address
                can take in a name with or without extension(takes extension from url)
        `printprogress`: will print current download progress in terminal
        """
        url_path = Path(url)
        #download_path = self.cwd / url_path.name if not d_path else Path(d_path)
        name_out = self._make_name(url_path, name_out)

        if not d_path:
            # download_path = self.src_path.parent
            download_path = self.cwd
        else:
            download_path = Path(d_path)
        # os.chdir(download_path)
        # making file path
        save_file = download_path / name_out 
        # checking if file already is there
        if save_file.exists():
            print('skipping', save_file.name)
            return

        r = self.session.get(url)
        # size = float(r.headers['content-length'])
        contentlength = r.headers.get('content-length')
        if contentlength is not None:
            size = float(contentlength)
        else:
            size = 1
        with open(save_file, 'wb') as fd:
            tmp = 0
            print(f'Downloding: {save_file.name}')
            print(f'to {save_file.absolute()}')
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    fd.write(chunk)
                    tmp += 1024
                    if printprogess:
                        self._print_progress(tmp, size)
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
    # d_path = input_loop() #let user decide where to download
    d_path = Path('/home/bruno/Desktop')
    name = name_loop() # let user decide what name it will have
    # name = 'Полное собрание сочинений. Братья Карамазовы. Части II-III, Федор Достоевский.djvu'
    d = Downloader()
    test_image_url = 'https://images.pexels.com/photos/459793/pexels-photo-459793.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260' 
    d.download(test_image_url, d_path, name, printprogess=False)