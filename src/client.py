"""Service client"""
import requests
from src.config import HOLIDAY_HOST, SCHDULER_HOST
from src.schemas import QueryCalendarSchema


class ClientScheduler:
    """Scheduler client"""

    def create_event(self, user_id: int, date: str, title: str):
        """Creates new event in user calendar"""
        data = {
            "user_id": user_id,
            "date": date,
            "title": title,
        }
        response = requests.post(
            url=f"{SCHDULER_HOST}calendar/user/", json=data, timeout=10
        )
        return response.json(), response.status_code

    def get_calendar(self, user_id: int, query: QueryCalendarSchema):
        """Get user calendar"""
        params = {
            "user_id": user_id,
            "year": query.year,
            "month": query.month,
        }
        response = requests.get(
            url=f"{SCHDULER_HOST}calendar/user/", params=params, timeout=10
        )
        return response.json(), response.status_code


class ClientHoliday:
    """Holiday client"""

    def validate_cpf(self, cpf: str) -> bool:
        """Validate cpf"""
        response = requests.get(
            f"{HOLIDAY_HOST}validator/", params={"value": cpf}, timeout=2
        )
        if response.status_code == 200:
            data_response = response.json()
            return data_response["valid"]

        return False
