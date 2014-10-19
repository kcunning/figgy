# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 5:01 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.

from django.test import TestCase
from lxml import etree
from storage.models import Book, Alias
import storage.tools


class TestTools(TestCase):
    def setUp(self):
        pass

    def test_storage_tools_process_book_element_db(self):
        '''process_book_element should put the book in the database.'''

        xml_str = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        xml = etree.fromstring(xml_str)
        storage.tools.process_book_element(xml)

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get(pk='12345')

        self.assertEqual(book.title, 'A title')
        self.assertEqual(book.aliases.count(), 2)
        self.assertEqual(Alias.objects.get(scheme='ISBN-10').value, '0158757819')
        self.assertEqual(Alias.objects.get(scheme='ISBN-13').value, '0000000000123')

    def test_unique_alias_on_new_book(self):
        book1 = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        book2 = '''
        <book id="123450">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000009999"/>
            </aliases>
        </book>
        '''

        xml1 = etree.fromstring(book1)
        xml2 = etree.fromstring(book2)
        storage.tools.process_book_element(xml1)
        storage.tools.process_book_element(xml2)

        book1 = Book.objects.get(id="12345")
        book2 = Book.objects.filter(id="123450")

        self.assertEqual(len(book2), 0)
        self.assertEqual(book1.title, "A title")

    def test_update_alias_on_old_book(self):
        book1 = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        book2 = '''
        <book id="12345">
            <title>A title corrected</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        xml1 = etree.fromstring(book1)
        xml2 = etree.fromstring(book2)
        storage.tools.process_book_element(xml1)
        storage.tools.process_book_element(xml2)

        book = Book.objects.get(id="12345")

        self.assertEqual(book.title, "A title corrected")
        self.assertEqual(len(book.aliases.all()), 2)



