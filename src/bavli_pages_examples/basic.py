import bavli_pages as bp

bp._get_bavli_obj().generate_chapter_view()
bp._get_bavli_obj().all_pages_in_each_chapter()

masechtot_dict = bp.bavli_pages_as_nested_data()
hebrew_page = masechtot_dict['ברכות'].chapters[2].start.page_hebrew_string
print('מסכת ברכות פרק שלישי מתחיל בדף')
print(hebrew_page)

bavli_masechtot_with_chapters = bp.bavli_pages_per_chapter()
print('רשימה של כל הפרקים בשס עם דף התחלה וסוף')
print(bavli_masechtot_with_chapters)

all_bavli_pages = bp.bavli_per_page()
print(all_bavli_pages.iloc[10])
print('דף יב בכל המסכתות. רשימה של 4 המסכתות האחרונות')
print(all_bavli_pages.query("pages=='יב'").tail(4).T)
