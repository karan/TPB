from collections import OrderedDict

from purl import URL as PURL


def URL(base, path, segments=None, defaults=None):
    """
    URL segment handler capable of getting and setting segments by name. The
    URL is constructed by joining base, path and segments.

    For each segment a property capable of getting and setting that segment is
    created dynamically.
    """
    # Make a copy of the Segments class
    url_class = type(Segments.__name__, Segments.__bases__,
                     dict(Segments.__dict__))
    segments = [] if segments is None else segments
    defaults = [] if defaults is None else defaults
    # For each segment attach a property capable of getting and setting it
    for segment in segments:
        setattr(url_class, segment, url_class._segment(segment))
    # Instantiate the class with the actual parameters
    return url_class(base, path, segments, defaults)


class Segments(object):

    """
    URL segment handler, not intended for direct use. The URL is constructed by
    joining base, path and segments.
    """

    def __init__(self, base, path, segments, defaults):
        # Preserve the base URL
        self.base = PURL(base, path=path)
        # Map the segments and defaults lists to an ordered dict
        self.segments = OrderedDict(zip(segments, defaults))

    def build(self):
        # Join base segments and segments
        segments = self.base.path_segments() + tuple(self.segments.values())
        # Create a new URL with the segments replaced
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
        """
        Returns a property capable of setting and getting a segment.
        """
        return property(
            fget=lambda x: cls._get_segment(x, segment),
            fset=lambda x, v: cls._set_segment(x, segment, v),
        )
