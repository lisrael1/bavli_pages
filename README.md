## bavli_pages

### List of pages per Masechet at each chapter at the Jewish Talmud/Gemara/Shas Bavli.

```
usage example:
    b = bp.bavli_pages_as_nested_data()
    b = b['ברכות'].chapters[2].start.page_hebrew_string
    print(b)
        יז:
                    
    b = bp.bavli_per_page()
    print(b.iloc[10])
        masechet    ברכות
        chapter         1
        pages          יב
    print(b.query("pages=='יב'").tail(4).T)
        masechet  תמורה  כריתות  מעילה  נידה
        chapter     1     3     3    1
        pages       יב     ב     יב     יב

    b = bp.bavli_pages_per_chapter()
        
```
