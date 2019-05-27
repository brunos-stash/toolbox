import unittest
import Downloader
from pathlib import Path

class TestDownloader(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('setUpClass')

    def setUp(self):
        self.d = Downloader.Downloader()
        self.url = Path('https://images.pexels.com/photos/459793/pexels-photo-459793.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')

    def test_make_name(self):
        self.assertEqual(self.d._make_name(self.url, None),'pexels-photo-459793.jpeg')
        self.assertEqual(self.d._make_name(self.url,''),'pexels-photo-459793.jpeg')
        self.assertEqual(self.d._make_name(self.url,'?'),'pexels-photo-459793.jpeg')
        self.assertEqual(self.d._make_name(self.url,'?..?..?'),'pexels-photo-459793.jpeg')
        self.assertEqual(self.d._make_name(self.url,'?..?..?**\\//- -'),'pexels-photo-459793.jpeg')
        self.assertEqual(self.d._make_name(self.url,'___'),'___.jpeg')
        self.assertEqual(self.d._make_name(self.url,'_3_'),'_3_.jpeg')
        self.assertEqual(self.d._make_name(self.url,'_3.png_'),'_3.png_')
        self.assertEqual(self.d._make_name(self.url,'_3.png*'),'_3.png')
        self.assertEqual(self.d._make_name(self.url,'ok'),'ok.jpeg')
        self.assertEqual(self.d._make_name(self.url,'ok.jpeg'),'ok.jpeg')
        self.assertEqual(self.d._make_name(self.url,'ok.png'),'ok.png')
        self.assertEqual(self.d._make_name(self.url,'ok.png.jpeg'),'ok.png.jpeg')
        self.assertEqual(self.d._make_name(self.url,123),'123.jpeg')
        self.assertEqual(self.d._make_name(self.url,123.44),'123.44')
        self.assertEqual(self.d._make_name(self.url,'123'),'123.jpeg')
        self.assertEqual(self.d._make_name(self.url,'123.jpeg'),'123.jpeg')
        self.assertEqual(self.d._make_name(self.url,'123.png'),'123.png')

        
if __name__ == '__main__':
    unittest.main()