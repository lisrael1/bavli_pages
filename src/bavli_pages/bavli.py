import os

import pandas as pd


class Page:
    def __init__(self, page_hebrew_string):
        self.page_hebrew_string = page_hebrew_string
        self.page_number = self.cast_hebrew_page_to_number(self.page_hebrew_string[:-1])
        self.first_page_side = True if '.' in self.page_hebrew_string else False

    @staticmethod
    def cast_hebrew_page_to_number(page_hebrew_letter):
        return -1


class Chapter:
    def __init__(self, start, end):
        self.start = Page(start)
        self.end = Page(end)


class Masechet:
    def __init__(self, masechet_name: str):
        self.name=masechet_name
        self.chapters=list()


class Bavli:
    def __init__(self):
        self.df = pd.read_excel(os.path.dirname(os.path.abspath(__file__))+'/all_pages.xlsx')
        self.df = self.df.melt(id_vars='masechet', var_name='chapter', value_name='page')
        self.df[['chapter_side', 'chapter']]=self.df.chapter.str.split('_', expand=True)
        self.df = self.df.query('~page.isna()')
        self.df.chapter = self.df.chapter.astype(int)

        # df.to_excel(os.path.dirname(os.path.abspath(__file__))+'/del.xlsx')

        self.bavli = dict()
        for masechet in self.df.masechet.unique():
            self.bavli[masechet] = Masechet(masechet)
            for chapter in self.df.query('masechet==@masechet').chapter.sort_values().unique():
                chapter_df = self.df.query('masechet==@masechet and chapter==@chapter').set_index('chapter_side').page
                if chapter_df.shape[0] != 2:
                    print(f'error, need start and end page at masechet {masechet} chapter {chapter}')
                    print(chapter_df)
                chapter_obj = Chapter(start=chapter_df.start, end=chapter_df.end)
                self.bavli[masechet].chapters.append(chapter_obj)

    def get_pages(self):
        return self.bavli

    def get_df(self):
        return self.df