from new import classobj


class Constants(type):
    def __repr__(cls):
        tree = cls.__name__ + '\n'
        for name in dir(cls):
            if not name.startswith('_'):
                attr = getattr(cls, name)
                if isinstance(attr, classobj):
                    attr = Constants(attr.__name__, attr.__bases__, attr.__dict__)
                    setattr(cls, name, attr)
                attr = '{}: {}'.format(name, repr(attr))
                tree += '\n'.join([ ' '*4 + line for line in attr.splitlines() ]) + '\n'
        return tree

    def __str__(cls):
        return repr(cls)


class orders:
    __metaclass__ = Constants

    class name:
        asc = 1
        des = 2
    class uploaded:
        asc = 3
        des = 4
    class size:
        asc = 5
        des = 6
    class seeders:
        asc = 7
        des = 8
    class leechers:
        asc = 9
        des = 10
    class uploader:
        asc = 11
        des = 12
    class type:
        asc = 13
        des = 14


class categories:
    __metaclass__ = Constants

    all = 0
    class audio:
        all = 100
        music = 101
        audio_books = 102
        sound_clips = 103
        flac = 104
        other = 199
    class video:
        all = 200
        movies = 201
        movies_dvdr = 202
        music_videos = 203
        movie_clips = 204
        tv_shows = 205
        handheld = 206
        hd_movies = 207
        hd_tv_shows = 208
        three_dimensions = 209
        other = 299
    class applications:
        all = 300
        windows = 301
        mac = 302
        unix = 303
        handheld = 304
        ios = 305
        android = 306
        other = 399
    class games:
        all = 400
        pc = 401
        mac = 402
        psx = 403
        xbox360 = 404
        wii = 405
        handheld = 406
        ios = 407
        android = 408
        other = 499
    class other:
        ebooks = 601
        comics = 602
        pictures = 603
        covers = 604
        physibles = 605
        other = 699
