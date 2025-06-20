# Analytics interfaces
from abc import ABC, abstractmethod
from .. import analytics
from datetime import datetime
import calendar

# interface class
class Analytics(ABC):
    @abstractmethod
    def setupAnalytics(self):
        pass

# concrete classes
class AdminAnalytics(Analytics):

    def __init__(self, timeline, year):
        self.timeline = timeline
        self.year = year

    def update_complaints_over_time(self):

        if self.timeline in ["7days", "30days"]:
            days_map = {"7days": 7, "30days": 30} # dict of labels and int
            days = days_map.get(self.timeline, 30) # return int
            complaints_over_time = analytics.get_complaint_over_time(days) # run the code
        
        else:
            # for specific month
            try: 
                month_number = list(calendar.month_name).index(self.timeline.capitalize())
                
                if self.year is None:
                    current_year = datetime.now().year
                else: 
                    current_year = int(self.year)

                start_date = datetime(current_year, month_number, 1)
                end_day = calendar.monthrange(current_year, month_number)[1]
                end_date = datetime(current_year, month_number, end_day)
                
                complaints_over_time = analytics.get_complaint_over_time_in_range(start_date, end_date)
            except ValueError:
                return "Error fetching data"

        return complaints_over_time

    # only for the first time setup
    def setupAnalytics(self):

        # summary
        total = analytics.get_all_total_complaints()
        pending = analytics.get_status_complaints("pending")
        filtered = analytics.get_status_complaints("filtered")
        approved = analytics.get_status_complaints("approved")
        in_progress = analytics.get_status_complaints("in_progress")
        resolved = analytics.get_status_complaints("resolved")
        rejected = analytics.get_status_complaints("rejected")

        # sum up
        summary = {
            "total": total, 
            "pending": pending, 
            "filtered": filtered, 
            "approved": approved, 
            "in_progress": in_progress,
            "resolved": resolved
        }

        # complaints over time, by default it's 30 days
        complaints_over_time = self.update_complaints_over_time()

        # breakdowns 
        pending_percentage = analytics.get_percentage(total, pending)
        filtered_percentage = analytics.get_percentage(total, filtered)
        in_progress_percentage = analytics.get_percentage(total, in_progress)
        resolved_percentage = analytics.get_percentage(total, resolved)
        rejected_percentage = analytics.get_percentage(total, rejected)

        status_breakdown = {
            "pending_percentage": pending_percentage, 
            "filtered_percentage": filtered_percentage, 
            "in_progress_percentage": in_progress_percentage, 
            "resolved_percentage": resolved_percentage, 
            "rejected_percentage": rejected_percentage
        }

        # rates
        resolution_rate = analytics.get_resolution_rate(resolved, total)

        return {
            "summary": summary,
            "complaints_over_time": complaints_over_time,
            "resolution_rate": resolution_rate,
            "status_breakdown": status_breakdown
        }
    
class CitizenAnalytics(Analytics):

    def __init__(self, user_id, timeline, year):
        self.user_id = user_id
        self.timeline = timeline
        self.year = year

    def update_complaints_over_time(self):

        if self.timeline in ["7days", "30days"]:
            days_map = {"7days": 7, "30days": 30} # dict of labels and int
            days = days_map.get(self.timeline, 30) # return int
            complaints_over_time = analytics.get_user_complaint_over_time(self.user_id, days) # run the code
        
        else:
            # for specific month
            try: 
                month_number = list(calendar.month_name).index(self.timeline.capitalize())
                
                if self.year is None:
                    current_year = datetime.now().year
                else: 
                    current_year = int(self.year)

                start_date = datetime(current_year, month_number, 1)
                end_day = calendar.monthrange(current_year, month_number)[1]
                end_date = datetime(current_year, month_number, end_day)
                
                complaints_over_time = analytics.get_user_complaint_over_time_in_range(self.user_id, start_date, end_date)
            except ValueError:
                return "Error fetching data"

        return complaints_over_time

    def setupAnalytics(self):
        total = analytics.get_total_complaints_by_user(self.user_id)
        pending = analytics.get_total_complaints_status_by_user(self.user_id, "pending")
        filtered = analytics.get_total_complaints_status_by_user(self.user_id, "filtered")
        approved = analytics.get_total_complaints_status_by_user(self.user_id, "approved")
        in_progress = analytics.get_total_complaints_status_by_user(self.user_id, "in_progress")
        resolved = analytics.get_total_complaints_status_by_user(self.user_id, "resolved")
        
        summary = {
            "total": total, 
            "pending": pending, 
            "filtered": filtered, 
            "approved": approved, 
            "in_progress": in_progress,
            "resolved": resolved
        }

        complaints_over_time = self.update_complaints_over_time()

        return {
            "summary": summary,
            "complaints_over_time": complaints_over_time
        }
    
class MaintenanceCompanyAnalytics(Analytics):

    def __init__(self, user_id, timeline, year):
        self.user_id = user_id
        self.timeline = timeline
        self.year = year

    def update_projects_over_time(self):

        if self.timeline in ["7days", "30days"]:
            days_map = {"7days": 7, "30days": 30} # dict of labels and int
            days = days_map.get(self.timeline, 30) # return int
            complaints_over_time = analytics.get_projects_over_time_of_user(self.user_id, days) # run the code
        
        else:
            # for specific month
            try: 
                month_number = list(calendar.month_name).index(self.timeline.capitalize())
                
                if self.year is None:
                    current_year = datetime.now().year
                else: 
                    current_year = int(self.year)

                start_date = datetime(current_year, month_number, 1)
                end_day = calendar.monthrange(current_year, month_number)[1]
                end_date = datetime(current_year, month_number, end_day)
                
                complaints_over_time = analytics.get_projects_over_time_in_range_of_user(self.user_id, start_date, end_date)
            except ValueError:
                return "Error fetching data"

        return complaints_over_time
    
    def setupAnalytics(self):
        assigned_raw = analytics.get_status_projects_of_user(self.user_id, "approved")
        in_progress = analytics.get_status_projects(self.user_id, "in_progress")
        resolved = analytics.get_status_projects(self.user_id, "resolved")
        
        assigned = assigned_raw + in_progress + resolved  # total assigned projects
        summary = {
            "assigned": assigned, 
            "in_progress": in_progress,
            "resolved": resolved
        }

        projects_over_time = self.update_projects_over_time()

        # breakdowns 
        assigned_percentage = analytics.get_percentage(assigned, assigned_raw)
        in_progress_percentage = analytics.get_percentage(assigned, in_progress)

        status_breakdown = {
            "assigned_percentage": assigned_percentage,
            "in_progress_percentage": in_progress_percentage, 
        }

        resolution_rate = analytics.get_resolution_rate(resolved, assigned)

        return {
            "summary": summary,
            "complaints_over_time": projects_over_time,
            "status_breakdown": status_breakdown,
            "resolution_rate": resolution_rate
        }
    
class GovtBodyAnalytics(Analytics):

    def __init__(self, timeline, year):
        self.timeline = timeline
        self.year = year

    def update_projects_over_time(self):

        if self.timeline in ["7days", "30days"]:
            days_map = {"7days": 7, "30days": 30} # dict of labels and int
            days = days_map.get(self.timeline, 30) # return int
            complaints_over_time = analytics.get_projects_over_time(days) # run the code
        
        else:
            # for specific month
            try: 
                month_number = list(calendar.month_name).index(self.timeline.capitalize())
                
                if self.year is None:
                    current_year = datetime.now().year
                else: 
                    current_year = int(self.year)

                start_date = datetime(current_year, month_number, 1)
                end_day = calendar.monthrange(current_year, month_number)[1]
                end_date = datetime(current_year, month_number, end_day)
                
                complaints_over_time = analytics.get_projects_over_time_in_range(start_date, end_date)
            except ValueError:
                return "Error fetching data"

        return complaints_over_time
    
    def setupAnalytics(self):
        filtered_raw = analytics.get_status_complaints("filtered")
        approved = analytics.get_status_projects("approved")
        in_progress = analytics.get_status_projects("in_progress")
        resolved = analytics.get_status_projects("resolved")
        
        assigned = filtered_raw + approved + in_progress + resolved  # total assigned projects
        print(assigned)

        summary = {
            "assigned": assigned, 
            "approved": approved,
            "in_progress": in_progress,
            "resolved": resolved
        }

        projects_over_time = self.update_projects_over_time()

        # breakdowns 
        assigned_percentage = analytics.get_percentage(assigned, filtered_raw)
        approved_percentage = analytics.get_percentage(assigned, approved)
        in_progress_percentage = analytics.get_percentage(assigned, in_progress)

        status_breakdown = {
            "assigned_percentage": assigned_percentage,
            "approved_percentage": approved_percentage,
            "in_progress_percentage": in_progress_percentage, 
        }

        resolution_rate = analytics.get_resolution_rate(resolved, assigned)

        return {
            "summary": summary,
            "complaints_over_time": projects_over_time,
            "status_breakdown": status_breakdown,
            #"resolution_rate": resolution_rate
        }