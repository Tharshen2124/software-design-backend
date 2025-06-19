from clients.supabase_client import supabase
from datetime import datetime, timedelta
from collections import OrderedDict
import pytz
import httpx
import time

def get_user_complaint_over_time(user_id: str, timeline: int):
    now = datetime.now(pytz.utc)
    start_date = now - timedelta(days=timeline)

    max_retries = 2
    delay = 0.5  # seconds
    complaints = []

    for attempt in range(max_retries):
        try:
            response = supabase.table("complaints") \
                .select("created_at") \
                .eq("citizen_id", user_id) \
                .gte("created_at", start_date.isoformat()) \
                .execute()
            complaints = response.data or []
            break  # success, exit loop
        except httpx.ReadError as e:
            print(f"Attempt {attempt + 1}: Socket ReadError: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break  # non-retryable error

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

def get_user_complaint_over_time_in_range(user_id: str, start_date, end_date):
    # Ensure start_date and end_date are datetime objects in UTC
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date).astimezone(pytz.utc)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date).astimezone(pytz.utc)

    max_retries = 2
    delay = 0.5  # seconds
    complaints = []

    for attempt in range(max_retries):
        try:
            response = supabase.table("complaints") \
                .select("created_at") \
                .eq("citizen_id", user_id) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()
            complaints = response.data or []
            break  # Success
        except httpx.ReadError as e:
            print(f"[Retry {attempt+1}] ReadError during complaints fetch: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Non-retryable error during complaints fetch: {e}")
            break

    # Initialize a dictionary with all days set to 0
    num_days = (end_date.date() - start_date.date()).days
    all_days = OrderedDict()
    for i in range(num_days + 1):
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

def get_total_complaints_by_user(user_id: str):
    max_retries = 2
    delay = 0.5  # seconds

    for attempt in range(max_retries):
        try:
            response = supabase.table("complaints").select("*", count="exact").eq('citizen_id', user_id).execute()
            num = response.count
            return num or 0
        
        except httpx.ReadError as e:
            print(f"[Retry {attempt + 1}] ReadError fetching complaints for user '{user_id}': {e}")
            time.sleep(delay)

        except Exception as e:
            print(f"Error fetching complaints for user '{user_id}':", e)
            return 0
    return 0  # Return 0 if all retries fail

def get_total_complaints_status_by_user(user_id: str, status: str):
    max_retries = 2
    delay = 0.5  # seconds

    for attempt in range(max_retries):
        try:
            response = supabase.table("complaints").select("*", count="exact") \
                .eq('citizen_id', user_id) \
                .eq('status', status) \
                .execute()
            num = response.count
            return num or 0
        except httpx.ReadError as e:
            print(f"[Retry {attempt + 1}] ReadError fetching complaints for user '{user_id}': {e}")
            time.sleep(delay)

        except Exception as e:
            print(f"Error fetching complaints for user '{user_id}' with status '{status}':", e)
            return 0
        
    return 0  # Return 0 if all retries fail

def get_all_total_complaints(): 
    max_retries = 2
    delay = 0.5  # seconds

    for attempt in range(max_retries):
        try:
            response = supabase.table("complaints").select("*", count="exact").execute()
            num = response.count
            return num or 0
        
        except httpx.ReadError as e:
            print(f"[Retry {attempt + 1}] ReadError fetching all complaints: {e}")
            time.sleep(delay)

        except Exception as e:
            print("Error fetching total complaints:", e)
            return 0

    return 0  # Return 0 if all retries fail

def get_status_complaints(status:str):
    max_retries = 2
    delay = 0.5  # seconds

    for attempt in range(max_retries):
        try:
            response = supabase.table("complaints").select("*", count="exact").eq('status', status).execute()
            return response.count or 0
        
        except httpx.ReadError as e:
            print(f"[Retry {attempt + 1}] ReadError fetching complaints with status '{status}': {e}")
            time.sleep(delay)
        
        except Exception as e:
            print(f"Error fetching complaints with status '{status}':", e)
            return 0
        
    return 0  # Return 0 if all retries fail

def get_complaint_over_time(timeline: int):
    now = datetime.now(pytz.utc)
    start_date = now - timedelta(days=timeline)

    max_retries = 2
    delay = 0.5  # seconds
    complaints = []
    for attempt in range(max_retries):
        try:
            response = supabase.table("complaints") \
                .select("created_at") \
                .gte("created_at", start_date.isoformat()) \
                .execute()
            complaints = response.data or []
            break  # success, exit loop
        except httpx.ReadError as e:
            print(f"Attempt {attempt + 1}: Socket ReadError: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

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

def get_complaint_over_time_in_range(start_date, end_date):
    # Ensure start_date and end_date are datetime objects in UTC
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date).astimezone(pytz.utc)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date).astimezone(pytz.utc)

    # Max retries and delay for handling potential read errors
    max_retries = 2
    delay = 0.5  # seconds
    complaints = []
    for attempt in range(max_retries):
        try:
            response = supabase.table("complaints") \
                .select("created_at") \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()
            complaints = response.data or []
            break  # Success
        except httpx.ReadError as e:
            print(f"[Retry {attempt+1}] ReadError during complaints fetch: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Non-retryable error during complaints fetch: {e}")
            break

    # Initialize a dictionary with all days set to 0
    num_days = (end_date.date() - start_date.date()).days
    all_days = OrderedDict()
    for i in range(num_days + 1):
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

def get_total_projects():

    max_retries = 2
    delay = 0.5  # seconds  
    for attempt in range(max_retries):
        try:
            response = supabase.table("maintenance_projects").select("*", count="exact").execute()
            return response.count or 0
        
        except httpx.ReadError as e:
            print(f"[Retry {attempt + 1}] ReadError fetching total projects: {e}")
            time.sleep(delay)
        
        except Exception as e:
            print("Error fetching total complaints:", e)
            return 0
        
    return 0  # Return 0 if all retries fail

def get_status_projects(status:str):
    max_retries = 2
    delay = 0.5  # seconds

    for attempt in range(max_retries):
        try:
            response = supabase.table("maintenance_projects").select("*", count="exact").eq('status', status).execute()
            return response.count or 0
        
        except httpx.ReadError as e:
            print(f"[Retry {attempt + 1}] ReadError fetching complaints with status '{status}': {e}")
            time.sleep(delay)
        
        except Exception as e:
            print(f"Error fetching complaints with status '{status}':", e)
            return 0
        
    return 0  # Return 0 if all retries fail
    
def get_projects_over_time(timeline: int):
    now = datetime.now(pytz.utc)
    start_date = now - timedelta(days=timeline)

    max_retries = 2
    delay = 0.5  # seconds
    complaints = []
    for attempt in range(max_retries):
        try:
            response = supabase.table("maintenance_projects") \
                .select("created_at") \
                .gte("created_at", start_date.isoformat()) \
                .execute()
            complaints = response.data or []
            break  # success, exit loop
        except httpx.ReadError as e:
            print(f"Attempt {attempt + 1}: Socket ReadError: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

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

def get_projects_over_time_in_range(start_date, end_date):
    # Ensure start_date and end_date are datetime objects in UTC
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date).astimezone(pytz.utc)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date).astimezone(pytz.utc)

    max_retries = 2
    delay = 0.5  # seconds
    complaints = []
    for attempt in range(max_retries):
        try:
            response = supabase.table("maintenance_projects") \
                .select("created_at") \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()
            complaints = response.data or []
            break  # Success
        except httpx.ReadError as e:
            print(f"[Retry {attempt+1}] ReadError during complaints fetch: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Non-retryable error during complaints fetch: {e}")
            break

    # Initialize a dictionary with all days set to 0
    num_days = (end_date.date() - start_date.date()).days
    all_days = OrderedDict()
    for i in range(num_days + 1):
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

def get_total_projects_of_user(user_id: str):
    max_retries = 2
    delay = 0.5  # seconds

    for attempt in range(max_retries):
        try:
            response = supabase.table("maintenance_projects").select("*", count="exact").eq("maintenance_company_id", user_id).execute()
            return response.count or 0
        
        except httpx.ReadError as e:
            print(f"[Retry {attempt + 1}] ReadError fetching total projects for user '{user_id}': {e}")
            time.sleep(delay)
        except Exception as e:
            print("Error fetching total complaints:", e)
            return 0
        
    return 0  # Return 0 if all retries fail

def get_status_projects_of_user(user_id: str, status:str):
    max_retries = 2
    delay = 0.5  # seconds
    for attempt in range(max_retries):
        try:
            response = supabase.table("maintenance_projects").select("*", count="exact").eq('status', status).eq("maintenance_company_id", user_id).execute()
            return response.count or 0
        except httpx.ReadError as e:
            print(f"[Retry {attempt + 1}] ReadError fetching projects for user '{user_id}' with status '{status}': {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Error fetching complaints with status '{status}':", e)
            return 0
    return 0  # Return 0 if all retries fail
    
def get_projects_over_time_of_user(user_id:str, timeline: int):
    now = datetime.now(pytz.utc)
    start_date = now - timedelta(days=timeline)

    max_retries = 2
    delay = 0.5  # seconds 
    complaints = []
    for attempt in range(max_retries):
        try:
            response = supabase.table("maintenance_projects") \
                .select("created_at") \
                .gte("created_at", start_date.isoformat()) \
                .eq("maintenance_company_id", user_id) \
                .execute()
            complaints = response.data or []
            break  # success, exit loop
        except httpx.ReadError as e:
            print(f"Attempt {attempt + 1}: Socket ReadError: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

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

def get_projects_over_time_in_range_of_user(user_id, start_date, end_date):
    # Ensure start_date and end_date are datetime objects in UTC
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date).astimezone(pytz.utc)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date).astimezone(pytz.utc)

    max_retries = 2
    delay = 0.5  # seconds
    complaints = []
    for attempt in range(max_retries):
        try:
            response = supabase.table("maintenance_projects") \
                .select("created_at") \
                .eq("maintenance_company_id", user_id) \
                .gte("created_at", start_date.isoformat()) \
                .lte("created_at", end_date.isoformat()) \
                .execute()
            complaints = response.data or []
            break  # Success
        except httpx.ReadError as e:
            print(f"[Retry {attempt+1}] ReadError during complaints fetch: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"Non-retryable error during complaints fetch: {e}")
            break

    # Initialize a dictionary with all days set to 0
    num_days = (end_date.date() - start_date.date()).days
    all_days = OrderedDict()
    for i in range(num_days + 1):
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