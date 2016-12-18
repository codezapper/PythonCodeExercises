from django.db import models
from django.template import loader
from .models import Song


'''It is possible (and documented) to use a response like:
HttpResponse(open('test.file')) but Django emits bytes using iter(),
and calling next() to get more bytes. The problem is that the
default behaviour is to check for newlines in the input file.
This does not work well for binary files (there is no real concept
of "line"), so I want an iterator that reads chunks of data
of a specified size.'''


class StreamWrapper():

    def __init__(self, input_file, buffer_size=1024**2):
        self.file_handle = open(input_file, 'rb')
        self.buffer_size = buffer_size

    def next(self):
        stream_data = self.file_handle.read(self.buffer_size)
        if stream_data:
            return stream_data
        else:
            raise StopIteration

    def __iter__(self):
        return self
