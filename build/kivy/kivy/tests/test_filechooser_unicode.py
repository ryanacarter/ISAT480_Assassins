# -*- coding: utf-8 -*-
# XXX: please be careful to only save this file with an utf-8 editor
import unittest
import logging


class FileChooserUnicodeTestCase(unittest.TestCase):

    def setUp(self):
        import os
        from os.path import join
        from zipfile import ZipFile
        basepath = os.path.dirname(__file__) + u''
        basepathu = join(basepath, u'filechooser_files')
        self.basepathu = basepathu
        basepathb = bytes(basepathu)
        self.basepathb = basepathb

        # this will test creating unicode and bytes filesnames
        ufiles = [u'कीवीtestu',
                  u'कीवीtestu' + unichr(0xFFFF),
                  u'कीवीtestu' + unichr(0xFFFF - 1),
                  u'कीवीtestu' + unichr(0xFF)]
        # don't use non-ascii directly because that will test source file
        # text conversion, not path issues :)
        bfiles = [b'\xc3\xa0\xc2\xa4\xe2\x80\xa2\xc3\xa0\xc2\xa5\xe2\x82\xac\
        \xc3\xa0\xc2\xa4\xc2\xb5\xc3\xa0\xc2\xa5\xe2\x82\xactestb',
        b'oor\xff\xff\xff\xff\xee\xfe\xef\x81\x8D\x99testb']
        self.ufiles = [join(basepathu, f) for f in ufiles]
        self.bfiles = [join(basepathb, f) for f in bfiles]
        if not os.path.isdir(basepathu):
            os.mkdir(basepathu)
        for f in self.ufiles:
            open(f, 'wb').close()
        for f in self.bfiles:
            open(f, 'wb').close()

        # existing files
        existfiles = [u'à¤•à¥€à¤µà¥€test', u'à¤•à¥€à¤’µà¥€test',
                      u'Ã Â¤â€¢Ã Â¥â‚¬Ã Â¤ÂµÃ Â¥â‚¬test', u'testl\ufffe',
                      u'testl\uffff']
        self.exitsfiles = [join(basepathu, f) for f in existfiles]
        with ZipFile(join(basepath, u'unicode_files.zip'), 'r') as myzip:
            myzip.extractall(path=basepathu)
        for f in self.exitsfiles:
            open(f, 'rb').close()

    def test_filechooserlistview_unicode(self):
        from kivy.uix.filechooser import FileChooserListView
        from kivy.clock import Clock
        from os.path import join

        wid = FileChooserListView(path=self.basepathu)
        for i in range(1):
            Clock.tick()
        files = [join(self.basepathu, f) for f in wid.files]
        for f in self.ufiles:
            self.assertIn(f, files)
        # we cannot test the bfiles because we'd have to know the system
        # unicode encoding to be able to compare to returned unicode
        for f in self.exitsfiles:
            self.assertIn(f, files)
        wid = FileChooserListView(path=self.basepathb)
        Clock.tick()
        files = [join(self.basepathb, f) for f in wid.files]
        for f in self.bfiles:
            self.assertIn(f, files)

    def tearDown(self):
        import shutil
        try:
            shutil.rmtree(self.basepathu, ignore_errors=True)
        except:
            pass

