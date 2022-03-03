from bavli_pages.bavli import Bavli


def bavli_pages_as_nested_data():
    return Bavli().get_pages()


def bavli_pages_per_chapter():
    return Bavli().get_df()

def bavli_per_page():
    return Bavli().get_pages_at_chapters()

