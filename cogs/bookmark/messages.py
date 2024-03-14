from config.messages import GlobalMessages


class BookmarkMess(GlobalMessages):
    bookmark_title = "Bookmark on server `{server}`"
    bookmark_upload_limit = "Zpráva obsahuje přílohu přesahující upload limit, doporučuji si tuto přílohu stáhnout. V připadě smazání původní zprávy nebude příloha dostupná."
    bookmark_created = "Bookmark `{bookmark_name}` created"
