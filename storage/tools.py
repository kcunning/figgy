# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 4:58 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.
import logging

from django.db import IntegrityError

from storage.models import Book

def process_book_element(book_element):
    """
    Process a book element into the database.

    :param book: book element
    :returns:
    """

    book, created = Book.objects.get_or_create(pk=book_element.get('id'))
    book.title = book_element.findtext('title')
    book.description = book_element.findtext('description')

    for alias in book_element.xpath('aliases/alias'):
        scheme = alias.get('scheme')
        value = alias.get('value')
        try:
            book.aliases.get_or_create(scheme=scheme, value=value)
        except IntegrityError as e:
            print 'ERROR: Cannot use value {val} for book "{book}". Unique constraint.'.format(
                val=value, book=book.title)
            print 'Book not imported.'
            # Do not save this book that comes from a file with bad data
            if created:
                book.delete()
            return # Do not save!

    book.save()