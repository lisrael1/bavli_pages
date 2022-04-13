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
        """
            all_pages.xlsx is a given data.
            the function here transform it into masechet and chapter table,
            where each unique masechet chapter has 2 rows here - start and end page
        :return:
        """
        df = pd.read_excel(os.path.dirname(os.path.abspath(__file__)) + '/all_pages.xlsx')
        df = df.melt(id_vars='masechet', var_name='chapter', value_name='page')
        df[['chapter_side', 'chapter']] = df.chapter.str.split('_', expand=True)
        df = df.query('~page.isna()').copy()
        df.chapter = df.chapter.astype(int)
        df['page_number'] = df.page.str[:-1].apply(gematriapy.to_number).astype(int).values
        df['page_first_side'] = df.page.str[-1].apply(lambda s: True if s == '.' else False).values
        df = df.sort_values(['masechet', 'page_number', 'chapter_side'], ascending=[True, True, True])
        if df.groupby(['masechet', 'chapter']).size().value_counts().shape[0] != 1:
            print("error - for each masechet and chapter there should be 2 rows - start and end page, "
                  "and it's not the situation")
            print(df.groupby(['masechet', 'chapter']).size().value_counts())

        df.to_excel(os.path.dirname(os.path.abspath(__file__)) + '/chapter_view.xlsx', index=False)

    def all_pages_in_each_chapter(self):
        all_pages = []
        for masechet_name, masechet in self.bavli.items():
            for chapter in self.bavli[masechet_name].chapters:
                tmp = dict(masechet=masechet_name,
                           chapter=chapter.chapter_number,
                           pages=self.bavli[masechet_name].chapters[chapter.chapter_number - 1].list_of_all_pages)
                all_pages.append(tmp)
        all_pages = pd.DataFrame(all_pages).explode('pages')
        all_pages['page_number'] = all_pages.fillna('ת').pages.apply(gematriapy.to_number)

        # looking for jumps in chapters
        if all_pages.groupby('masechet').chapter.apply(lambda c: not c.is_monotonic).sum() != 0:
            print('error - jumps at the chapters')
            print(all_pages.groupby('masechet').chapter.apply(lambda c: not c.is_monotonic))

        # looking for jumps in pages
        if all_pages.groupby('masechet').page_number.apply(lambda c: not c.is_monotonic).sum() != 0:
            print('error - jumps at the page_number')
            print(all_pages.groupby('masechet').page_number.apply(lambda c: not c.is_monotonic))

        missing_pages = all_pages \
            .drop_duplicates(['masechet', 'page_number']) \
            .query('masechet!="תמיד"') \
            .groupby('masechet') \
            .apply(lambda g: g.page_number.max() != g.shape[0] + 1)
        if missing_pages.sum():
            print('error - max page not as expected')
            print(missing_pages)
        unique_pages = all_pages.groupby('masechet').apply(lambda g: g.page_number.nunique() != g.shape[0])
        if unique_pages.sum():
            print('error - missing page ')
            print(unique_pages)
        raw_pages = all_pages \
            .query('masechet!="תמיד"') \
            .groupby('masechet') \
            .apply(lambda g: all(i == j for i, j in
                                 zip(g.page_number.sort_values().unique().tolist(),
                                     range(2, g.shape[0] + 2))))
        if raw_pages.mean() != 1:
            print('missing pages')
            print(raw_pages)
        all_pages.to_excel(os.path.dirname(os.path.abspath(__file__)) + '/pages_view.xlsx', index=False)

        # old school checking
        all_pages = all_pages.assign(next_page_chapter=all_pages.chapter.shift().fillna(0).astype(int))
        should_be_empty = all_pages \
            .query('chapter != next_page_chapter and chapter-1 != next_page_chapter and chapter != 1')
        if not should_be_empty.empty:
            print('error - there are jumps in chapters at pages_view.xlsx')

    def get_pages(self):
        return self.bavli

    def get_df(self):
        return self.df

    def get_pages_at_chapters(self):
        return self.all_chapters
