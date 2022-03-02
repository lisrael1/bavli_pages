import os

import pandas as pd
import gematriapy


class Page:
    def __init__(self, page_hebrew_string):
        self.page_hebrew_string = page_hebrew_string
        self.page_number = self.cast_hebrew_page_to_number(self.page_hebrew_string[:-1])
        self.first_page_side = True if '.' in self.page_hebrew_string else False

    @staticmethod
    def cast_hebrew_page_to_number(page_hebrew_letter):
        return gematriapy.to_number(page_hebrew_letter)


class Chapter:
    def __init__(self, start, end):
        self.start = Page(start)
        self.end = Page(end)
        self.list_of_all_pages = self.get_list_of_all_pages()

    def get_list_of_all_pages(self):
        start_number = self.start.page_number
        end_number = self.end.page_number
        list_of_all_pages = [gematriapy.to_hebrew(n) for n in range(start_number, end_number + 1)]
        return list_of_all_pages


class Masechet:
    def __init__(self, masechet_name: str):
        self.name=masechet_name
        self.chapters=list()


class Bavli:
    def __init__(self):
        self.df = self.get_df()
        self.bavli = dict()
        self.build_nested_data()

    def build_nested_data(self):
        for masechet in self.df.masechet.unique():
            self.bavli[masechet] = Masechet(masechet)
            for chapter in self.df.query('masechet==@masechet').chapter.sort_values().unique():
                chapter_df = self.df.query('masechet==@masechet and chapter==@chapter').set_index('chapter_side').page
                if chapter_df.shape[0] != 2:
                    print(f'error, need start and end page at masechet {masechet} chapter {chapter}')
                    print(chapter_df)
                chapter_obj = Chapter(start=chapter_df.start, end=chapter_df.end)
                self.bavli[masechet].chapters.append(chapter_obj)

    @staticmethod
    def get_df():
        df = pd.read_excel(os.path.dirname(os.path.abspath(__file__)) + '/all_pages.xlsx')
        df = df.melt(id_vars='masechet', var_name='chapter', value_name='page')
        df[['chapter_side', 'chapter']] = df.chapter.str.split('_', expand=True)
        df = df.query('~page.isna()')
        df.chapter = df.chapter.astype(int)
        df['page_number'] = df.page.str[:-1].apply(gematriapy.to_number)
        df['page_first_side'] = df.page.str[-1].apply(lambda s: True if s == '.' else False)

        # df.to_excel(os.path.dirname(os.path.abspath(__file__))+'/del.xlsx')

        return df

    def get_pages(self):
        return self.bavli

    def get_df(self):
        return self.df
