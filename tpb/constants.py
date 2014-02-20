import sys

if sys.version_info >= (3, 0):
    class_type = type
else:
    from new import classobj
    class_type = classobj


class ConstantType(type):

    """
    Tree representation metaclass for class attributes. Metaclass is extended
    to all child classes too.
    """
    def __new__(cls, clsname, bases, dct):
        """
        Extend metaclass to all class attributes too.
        """
        attrs = {}
        for name, attr in dct.items():
            if isinstance(attr, class_type):
                # substitute attr with a new class with Constants as
                # metaclass making it possible to spread this same method
                # to all child classes
                attr = ConstantType(
                    attr.__name__, attr.__bases__, attr.__dict__)
            attrs[name] = attr
        return super(ConstantType, cls).__new__(cls, clsname, bases, attrs)

    def __repr__(cls):
        """
        Tree representation of class attributes. Child classes are also
        represented.
        """
        # dump current class name
        tree = cls.__name__ + ':\n'
        for name in dir(cls):
            if not name.startswith('_'):
                attr = getattr(cls, name)
                output = repr(attr)
                if not isinstance(attr, ConstantType):
                    output = '{}: {}'.format(name, output)
                # indent all child attrs
                tree += '\n'.join([' ' * 4 + line
                                  for line in output.splitlines()]) + '\n'
        return tree

    def __str__(cls):
        return repr(cls)


Constants = ConstantType('Constants', (object,), {})


class ORDERS(Constants):

    class NAME:
        DES = 1
        ASC = 2

    class UPLOADED:
        DES = 3
        ASC = 4

    class SIZE:
        DES = 5
        ASC = 6

    class SEEDERS:
        DES = 7
        ASC = 8

    class LEECHERS:
        DES = 9
        ASC = 10

    class UPLOADER:
        DES = 11
        ASC = 12

    class TYPE:
        DES = 13
        ASC = 14


class CATEGORIES(Constants):
    ALL = 0

    class AUDIO:
        ALL = 100
        MUSIC = 101
        AUDIO_BOOKS = 102
        SOUND_CLIPS = 103
        FLAC = 104
        OTHER = 199

    class VIDEO:
        ALL = 200
        MOVIES = 201
        MOVIES_DVDR = 202
        MUSIC_VIDEOS = 203
        MOVIE_CLIPS = 204
        TV_SHOWS = 205
        HANDHELD = 206
        HD_MOVIES = 207
        HD_TV_SHOWS = 208
        THREE_DIMENSIONS = 209
        OTHER = 299

    class APPLICATIONS:
        ALL = 300
        WINDOWS = 301
        MAC = 302
        UNIX = 303
        HANDHELD = 304
        IOS = 305
        ANDROID = 306
        OTHER = 399

    class GAMES:
        ALL = 400
        PC = 401
        MAC = 402
        PSX = 403
        XBOX360 = 404
        WII = 405
        HANDHELD = 406
        IOS = 407
        ANDROID = 408
        OTHER = 499

    class PORN:
        ALL = 500
        MOVIES = 501
        MOVIES_DVDR = 502
        PICTURES = 503
        GAMES = 504
        HD_MOVIES = 505
        MOVIE_CLIPS = 506
        OTHER = 599

    class OTHER:
        EBOOKS = 601
        COMICS = 602
        PICTURES = 603
        COVERS = 604
        PHYSIBLES = 605
        OTHER = 699
