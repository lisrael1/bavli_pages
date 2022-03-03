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
    def __init__(self, chapter_number, start, end):
        self.chapter_number = chapter_number
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
        self.name = masechet_name
        self.chapters = list()


class Bavli:
    def __init__(self):
        update_tables_by_all_pages = False
        if update_tables_by_all_pages:
            self.generate_chapter_view()
        self.df = pd.read_excel(os.path.dirname(os.path.abspath(__file__)) + '/chapter_view.xlsx')
        self.bavli = dict()
        self.build_nested_data()
        if update_tables_by_all_pages:
            self.all_pages_in_each_chapter()
        self.all_chapters = pd.read_excel(os.path.dirname(os.path.abspath(__file__)) + '/pages_view.xlsx')

    def build_nested_data(self):
        for masechet in self.df.masechet.unique():
            self.bavli[masechet] = Masechet(masechet)
            for chapter in self.df.query('masechet==@masechet').chapter.sort_values().unique():
                chapter_df = self.df.query('masechet==@masechet and chapter==@chapter').set_index('chapter_side').page
                if chapter_df.shape[0] != 2:
                    print(f'error, need start and end page at masechet {masechet} chapter {chapter}')
                    print(chapter_df)
                chapter_obj = Chapter(chapter_number=chapter, start=chapter_df.start, end=chapter_df.end)
                self.bavli[masechet].chapters.append(chapter_obj)

    @staticmethod
    def generate_chapter_view():
        df = pd.read_excel(os.path.dirname(os.path.abspath(__file__)) + '/all_pages.xlsx')
        df = df.melt(id_vars='masechet', var_name='chapter', value_name='page')
        df[['chapter_side', 'chapter']] = df.chapter.str.split('_', expand=True)
        df = df.query('~page.isna()').copy()
        df.chapter = df.chapter.astype(int)
        df['page_number'] = df.page.str[:-1].apply(gematriapy.to_number).values
        df['page_first_side'] = df.page.str[-1].apply(lambda s: True if s == '.' else False).values

        df.to_excel(os.path.dirname(os.path.abspath(__file__))+'/chapter_view.xlsx')

    def all_pages_in_each_chapter(self):
        all_chapters = []
        for masechet_name, masechet in self.bavli.items():
            for chapter in self.bavli[masechet_name].chapters:
                tmp = dict(masechet=masechet_name,
                           chapter=chapter.chapter_number,
                           pages=self.bavli[masechet_name].chapters[chapter.chapter_number-1].list_of_all_pages)
                all_chapters.append(tmp)
        all_chapters = pd.DataFrame(all_chapters).explode('pages')
        all_chapters.to_excel(os.path.dirname(os.path.abspath(__file__))+'/pages_view.xlsx')

    def get_pages(self):
        return self.bavli

    def get_df(self):
        return self.df

    def get_pages_at_chapters(self):
        return self.all_chapters
