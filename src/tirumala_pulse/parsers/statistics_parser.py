import re
from bs4 import BeautifulSoup


class StatisticsParser:

    @staticmethod
    def is_statistics_post(post):
        title = post["title"]["rendered"]
        return title.startswith("Total pilgrims who had darshan")

    @staticmethod
    def extract_text(post):

        html = post["content"]["rendered"]

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(
            separator="\n",
            strip=True
        )

    @staticmethod
    def _extract(pattern, text):

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        return None

    @staticmethod
    def _number(value):

        if value is None:
            return None

        return int(value.replace(",", ""))

    @staticmethod
    def parse(post):

        text = StatisticsParser.extract_text(post)

        report = {}

        report["report_date"] = StatisticsParser._extract(
            r"darshan on (\d{2}\.\d{2}\.\d{4})",
            text
        )

        report["pilgrims"] = StatisticsParser._number(
            StatisticsParser._extract(
                r"darshan.*?:\s*([\d,]+)",
                text
            )
        )

        report["tonsures"] = StatisticsParser._number(
            StatisticsParser._extract(
                r"Tonsures:\s*([\d,]+)",
                text
            )
        )

        hundi = StatisticsParser._extract(
            r"Hundi.*?:\s*([\d.]+)",
            text
        )

        if hundi:
            report["hundi_amount_rupees"] = int(float(hundi) * 10000000)

        laddu = StatisticsParser._extract(
            r"Laddu.*?([\d.]+)\s*Lac",
            text
        )

        if laddu:
            report["laddu_sale"] = int(float(laddu) * 100000)

        anna = StatisticsParser._extract(
            r"Annaprasadams.*?([\d.]+)\s*Lac",
            text
        )

        if anna:
            report["annaprasadams"] = int(float(anna) * 100000)

        report["medical_treatment"] = StatisticsParser._number(
            StatisticsParser._extract(
                r"Medical treatment.*?([\d,]+)",
                text
            )
        )

        report["waiting_compartments"] = StatisticsParser._extract(
            r"Waiting Compartments.*?([^\n]+)",
            text
        )

        darshan = StatisticsParser._extract(
            r"(\d+)\s*H",
            text
        )

        if darshan:
            report["darshan_time_hours"] = int(darshan)

        return report