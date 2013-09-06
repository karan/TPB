from new import classobj


class Constants(type):
    """
    Tree representation metaclass for class attributes. Metaclass is extended
    to all child classes too.
    """
    def __repr__(cls):
        """
        Tree representation of class attributes. If some attribute is a class,
        this class is also represented in a tree.
        """
        # dump current class name
        tree = cls.__name__ + '\n'

        for name in dir(cls):
            if not name.startswith('_'):
                attr = getattr(cls, name)
                
                # if attr is a class
                if isinstance(attr, classobj):

                    # substitute attr with a new class with Constants as 
                    # metaclass making it possible to spread this same method
                    # to all child classes
                    attr = Constants(attr.__name__, attr.__bases__, attr.__dict__)
                    setattr(cls, name, attr)

                attr = '{}: {}'.format(name, repr(attr))
                # indent all child attrs
                tree += '\n'.join([ ' '*4 + line for line in attr.splitlines() ]) + '\n'
        return tree

    def __str__(cls):
        return repr(cls)


class ORDERS:
    __metaclass__ = Constants

    class NAME:
        ASC = 1
        DES = 2
    class UPLOADED:
        ASC = 3
        DES = 4
    class SIZE:
        ASC = 5
        DES = 6
    class SEEDERS:
        ASC = 7
        DES = 8
    class LEECHERS:
        ASC = 9
        DES = 10
    class UPLOADER:
        ASC = 11
        DES = 12
    class TYPE:
        ASC = 13
        DES = 14


class CATEGORIES:
    __metaclass__ = Constants

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
    class OTHER:
        EBOOKS = 601
        COMICS = 602
        PICTURES = 603
        COVERS = 604
        PHYSIBLES = 605
        OTHER = 699
