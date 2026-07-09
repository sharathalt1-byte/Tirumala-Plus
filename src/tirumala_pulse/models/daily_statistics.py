from dataclasses import dataclass
from typing import Optional


@dataclass
class DailyStatistics:
    """
    Represents one day's Tirumala statistics.
    """

    report_date: str

    pilgrims: Optional[int] = None
    tonsures: Optional[int] = None
    hundi_amount_rupees: Optional[int] = None
    laddu_sale: Optional[int] = None
    annaprasadams: Optional[int] = None
    medical_treatment: Optional[int] = None
    waiting_compartments: Optional[str] = None
    darshan_time_hours: Optional[int] = None

    source: str = "TTD Official"
    parser_version: str = "1.0"

    def to_dict(self):
        """
        Convert the object into a dictionary for database insertion.
        """

        return {
            "report_date": self.report_date,
            "pilgrims": self.pilgrims,
            "tonsures": self.tonsures,
            "hundi_amount_rupees": self.hundi_amount_rupees,
            "laddu_sale": self.laddu_sale,
            "annaprasadams": self.annaprasadams,
            "medical_treatment": self.medical_treatment,
            "waiting_compartments": self.waiting_compartments,
            "darshan_time_hours": self.darshan_time_hours,
            "source": self.source,
            "parser_version": self.parser_version
        }

    def __str__(self):
        return (
            f"DailyStatistics("
            f"report_date={self.report_date}, "
            f"pilgrims={self.pilgrims}, "
            f"tonsures={self.tonsures}, "
            f"hundi={self.hundi_amount_rupees})"
        )