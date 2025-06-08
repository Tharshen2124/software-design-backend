# Analytics interfaces
from abc import ABC, abstractmethod
from .. import analytics

# interface class
class Analytics(ABC):
    @abstractmethod
    def setupAnalytics(self):
        pass

# concrete classes
class AdminAnalytics(Analytics):

    def update_complaints_over_time(self):
        complaints_over_time = analytics.get_complaint_over_time()

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
        summary = [total, pending, filtered, approved, in_progress, approved, in_progress, resolved]

        # complaints over time, by default it's 30 days
        complaints_over_time = self.update_complaints_over_time()

        # breakdowns 
        pending_percentage = analytics.get_percentage(total, pending)
        filtered_percentage = analytics.get_percentage(total, filtered)
        in_progress_percentage = analytics.get_percentage(total, in_progress)
        resolved_percentage = analytics.get_percentage(total, resolved)
        rejected_percentage = analytics.get_percentage(total, rejected)

        status_breakdown = [pending_percentage, filtered_percentage, in_progress_percentage, resolved_percentage, rejected_percentage]

        # rates
        resolution_rate = analytics.get_resolution_rate(resolved, total)

        return {
            "summary": summary,
            "complaints_over_time": complaints_over_time,
            "resolution_rate": resolution_rate,
            "status_breakdown": status_breakdown
        }
    
class CitizenAnalytics(Analytics):
    def setupAnalytics(self):
        return "citizen"
    
class MaintenanceCompanyAnalytics(Analytics):
    def setupAnalytics(self):
        return "maintenance company"
    
class GovtBodyAnalytics(Analytics):
    def setupAnalytics(self):
        return "govt body"