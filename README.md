## bavli_pages

#### List of pages per Masechet at each chapter at the Jewish Talmud/Gemara/Shas Bavli.

usage example:
```python
    import bavli_pages as bp

    masechtot_dict = bp.bavli_pages_as_nested_data()
    hebrew_page = masechtot_dict['ברכות'].chapters[2].start.page_hebrew_string
    print('מסכת ברכות פרק שלישי מתחיל בדף')
    print(hebrew_page)
    
    
        מסכת ברכות פרק שלישי מתחיל בדף
        יז:         
    
    bavli_masechtot_with_chapters = bp.bavli_pages_per_chapter()
    print('רשימה של כל הפרקים בשס עם דף התחלה וסוף')
    print(bavli_masechtot_with_chapters)
    
```
    
רשימה של כל הפרקים בשס עם דף התחלה וסוף

| masechet   | chapter | page | chapter_side | page_number | page_first_side |
|------------|---------|------|--------------|-------------|------------------|
| בבא בתרא  | 1       | ב.   | start        | 2           | True             |
| בבא בתרא  | 1       | יז.  | end          | 17          | True             |
| בבא בתרא  | 2       | יז.  | start        | 17          | True             |
| בבא בתרא  | 2       | כז:  | end          | 27          | False            |
| בבא בתרא  | 3       | כח.  | start        | 28          | True             |
| ...        | ...     | ...  | ...          | ...         | ...              |
| תענית      | 2       | יח:  | end          | 18          | False            |
| תענית      | 3       | יח:  | start        | 18          | False            |
| תענית      | 3       | כו.  | end          | 26          | True             |
| תענית      | 4       | כו.  | start        | 26          | True             |
| תענית      | 4       | לא:  | end          | 31          | False            |

[626 rows x 6 columns]
```python
        
        
    all_bavli_pages = bp.bavli_per_page()
    print(all_bavli_pages.iloc[10])
    
    
        masechet       בבא בתרא
        chapter               1
        pages                יב
        page_number          12
        Name: 10, dtype: object
        
        
    print('דף יב בכל המסכתות. רשימה של 4 המסכתות האחרונות')
    print(all_bavli_pages.query("pages=='יב'").tail(4).T)

```

דף יב בכל המסכתות. רשימה של 4 המסכתות האחרונות

| masechet    | שבועות | שבת | תמורה | תענית |
|-------------|---------|-----|--------|--------|
| chapter     | 1       | 1   | 1      | 1      |
| pages       | יב      | יב  | יב     | יב     |
| page_number | 12      | 12  | 12     | 12     |
