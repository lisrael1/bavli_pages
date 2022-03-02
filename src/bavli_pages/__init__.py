from bavli_pages.bavli import Bavli


def bavli_pages_as_nested_data():
    return Bavli().get_pages()


def bavli_pages_as_df():
    return Bavli().get_df()

