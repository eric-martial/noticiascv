from supabase import create_client, Client
from dotenv import dotenv_values
import os

dotenv_path = os.path.abspath('.env')

config = dotenv_values(dotenv_path)


class SaveArticlesToSupabasePipeline:

    def process_item(self, item, spider):
        url: str = config.get("SUPABASE_URL")
        key: str = config.get("SUPABASE_SECRET_KEY")
        supabase: Client = create_client(url, key)

        supabase.table('articles').insert({
            'source':  item['source'],
            'title': item['title'],
            'author':  item['author'],
            'date_pub':  item['date_pub'],
            'link':  item['link'],
            'topic':  item['topic'],
            'content':  item['text_html']
        }).execute()
        
        return item
