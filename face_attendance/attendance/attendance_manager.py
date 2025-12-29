from utils.time_utils import now_string, hours_between


class AttendanceManager:
    def __init__(self, db):
        self.db = db

    def check_in(self, person_id):
        timestamp = now_string()
        self.db.add_attendance(person_id, timestamp)
        return timestamp

    def daily_summary(self, start_time=None, end_time=None):
        rows = self.db.list_daily_summary(start_time, end_time)
        summary = []
        for person_id, name, day, first_time, last_time in rows:
            hours = hours_between(first_time, last_time)
            summary.append({
                "person_id": person_id,
                "name": name,
                "day": day,
                "first_time": first_time,
                "last_time": last_time,
                "hours": hours,
            })
        return summary
