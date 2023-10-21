from datetime import datetime
from supabase import create_client, Client
from dotenv import dotenv_values
import os

dotenv_path = os.path.abspath('.env')

config = dotenv_values(dotenv_path)


def normalize_date(date_obj):
    if not isinstance(date_obj, datetime):
        return None
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')


def article_exist(link: str) -> bool:
    url: str = config.get("SUPABASE_URL")
    key: str = config.get("SUPABASE_SECRET_KEY")
    supabase: Client = create_client(url, key)

    data, count = supabase.table('articles').select('*').eq('link', link).execute()

    return True if len(data[1]) > 0 else False
