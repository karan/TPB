from collections import OrderedDict

from purl import URL as PURL


def URL(base, path, segments=None, defaults=None):
    url_class = type(Segments.__name__, Segments.__bases__, 
                     dict(Segments.__dict__))
    segments = [] if segments is None else segments
    defaults = [] if defaults is None else defaults
    for segment in segments:
        setattr(url_class, segment, url_class._segment(segment))
    return url_class(base, path, segments, defaults)


class Segments(object):
    def __init__(self, base, path, segments, defaults):
        self.base = PURL(base, path=path)
        self.segments = OrderedDict(zip(segments, defaults))

    def build(self):
        segments = self.base.path_segments() + tuple(self.segments.values())
        url = self.base.path_segments(segments)
        return url

    def __str__(self):
        return self.build().as_string()

    def _get_segment(self, segment):
        return self.segments[segment]

    def _set_segment(self, segment, value):
        self.segments[segment] = value

    @classmethod
    def _segment(cls, segment):
        return property(
                fget=lambda x: cls._get_segment(x, segment),
                fset=lambda x, v: cls._set_segment(x, segment, v),
                )
