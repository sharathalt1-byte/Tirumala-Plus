from dataclasses import dataclass
from datetime import date


@dataclass
class RawReport:

    report_date: date

    source_url: str

    raw_content: str

    parser_version: str = "1.0"

    def to_dict(self):

        return {
            "report_date": self.report_date.strftime("%Y-%m-%d"),
            "source_url": self.source_url,
            "raw_content": self.raw_content,
            "parser_version": self.parser_version,
        }

    def __str__(self):

        return f"RawReport(" f"date={self.report_date}, " f"url={self.source_url})"
