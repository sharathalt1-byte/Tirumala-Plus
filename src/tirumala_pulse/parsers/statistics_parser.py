import re
from datetime import datetime

from bs4 import BeautifulSoup

from tirumala_pulse.models.daily_statistics import DailyStatistics


class StatisticsParser:

    @staticmethod
    def is_statistics_post(post):
        title = post["title"]["rendered"]
        return title.startswith("Total pilgrims who had darshan")

    @staticmethod
    def extract_text(post):

        html = post["content"]["rendered"]

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(separator="\n", strip=True)

    @staticmethod
    def _extract(pattern, text):

        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

        if match:
            return match.group(1).strip()

        return None

    @staticmethod
    def _clean_numeric(value):
        """
        Normalizes numeric strings.

        Examples:
            "..2.94" -> "2.94"
            "...4.05" -> "4.05"
            "4,567" -> "4567"
            " 2.94 " -> "2.94"
        """

        if value is None:
            return None

        value = value.strip()

        value = value.replace(",", "")

        match = re.search(r"\d+(?:\.\d+)?", value)

        if match:
            return match.group(0)

        return None

    @staticmethod
    def _number(value):

        value = StatisticsParser._clean_numeric(value)

        if value is None:
            return None

        return int(float(value))

    @staticmethod
    def _lac_to_number(value):

        value = StatisticsParser._clean_numeric(value)

        if value is None:
            return None

        return round(float(value) * 100000)

    @staticmethod
    def _crore_to_number(value):

        value = StatisticsParser._clean_numeric(value)

        if value is None:
            return None

        return round(float(value) * 10000000)

    @staticmethod
    def parse(post):

        text = StatisticsParser.extract_text(post)

        report_date = StatisticsParser._extract(
            r"darshan on (\d{2}\.\d{2}\.\d{4})", text
        )

        report_date = datetime.strptime(report_date, "%d.%m.%Y").date()

        pilgrims = StatisticsParser._number(
            StatisticsParser._extract(r"darshan.*?:\s*([\d,]+)", text)
        )

        tonsures = StatisticsParser._number(
            StatisticsParser._extract(r"Tonsures\s*:\s*([\d,]+)", text)
        )

        hundi = StatisticsParser._crore_to_number(
            StatisticsParser._extract(r"Hundi.*?:\s*([^\n]+)", text)
        )

        laddu_sale = StatisticsParser._lac_to_number(
            StatisticsParser._extract(r"Laddu.*?([^\n]+?)\s*Lac", text)
        )

        annaprasadams = StatisticsParser._lac_to_number(
            StatisticsParser._extract(r"Annaprasadams.*?([^\n]+?)\s*Lac", text)
        )

        medical = StatisticsParser._number(
            StatisticsParser._extract(r"Medical treatment.*?([\d,]+)", text)
        )

        waiting = StatisticsParser._extract(r"Waiting Compartments.*?([^\n]+)", text)

        if waiting:
            waiting = waiting.replace("…", "").replace(".", "").strip()

        darshan = StatisticsParser._extract(r"Approx.*?(\d+)\s*H", text)

        darshan_hours = int(darshan) if darshan else None

        return DailyStatistics(
            report_date=report_date,
            pilgrims=pilgrims,
            tonsures=tonsures,
            hundi_amount_rupees=hundi,
            laddu_sale=laddu_sale,
            annaprasadams=annaprasadams,
            medical_treatment=medical,
            waiting_compartments=waiting,
            darshan_time_hours=darshan_hours,
        )
