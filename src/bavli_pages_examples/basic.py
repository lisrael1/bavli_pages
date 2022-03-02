import bavli_pages as bp

b = bp.bavli_pages_as_nested_data()
b = b['ברכות'].chapters[2].start.page_hebrew_string
print(b)
b = bp.bavli_pages_as_df()
print(b)
