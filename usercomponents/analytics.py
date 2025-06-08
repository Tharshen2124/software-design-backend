from clients.supabase_client import supabase
from datetime import datetime, timedelta
from collections import OrderedDict
import pytz

def get_all_total_complaints(): 
    response = supabase.table("complaints").select("*", count="exact").execute()
    num = response.count
    return num

def get_status_complaints(status:str):
    response = supabase.table("complaints").select("*", count="exact").eq('status', status).execute()
    num = response.count
    return num

def get_complaint_over_time(timeline: int = 30):
    now = datetime.now(pytz.utc)
    start_date = now - timedelta(days=timeline)

    # Fetch complaints created within the timeline
    response = supabase.table("complaints") \
        .select("created_at") \
        .gte("created_at", start_date.isoformat()) \
        .execute()

    complaints = response.data

    # Initialize a dictionary with all days set to 0
    all_days = OrderedDict()
    for i in range(timeline + 1):
        day = (start_date + timedelta(days=i)).date().isoformat()
        all_days[day] = 0

    # Count complaints per day
    for complaint in complaints:
        created_at = complaint.get("created_at")
        if created_at:
            dt = datetime.fromisoformat(created_at).astimezone(pytz.utc).date().isoformat()
            if dt in all_days:
                all_days[dt] += 1

    return all_days


def get_resolution_rate(resolved: int, total: int):

    resolution_rate = (resolved / total) * 100

    return round(resolution_rate, 2)


def get_percentage(total:int, num:int):
    percentage = (num / total) * 100

    return round(percentage, 2)