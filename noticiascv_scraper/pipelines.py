from supabase import create_client, Client
from dotenv import dotenv_values

config = dotenv_values("../.env")


class SaveArticlesToSupabasePipeline:

    def __init__(self):
        self.url: str = config.get("SUPABASE_URL")
        self.key: str = config.get("SUPABASE_SECRET_KEY")
        self.supabase: Client = create_client(self.url, self.key)

    def process_item(self, item, spider):
        self.supabase.table('articles').insert({
            'source':  item['source'],
            'title': item['title'],
            'author':  item['author'],
            'date_pub':  item['date_pub'],
            'link':  item['link'],
            'topic':  item['topic'],
            'content':  item['text_html']
        }).execute()
        return item
