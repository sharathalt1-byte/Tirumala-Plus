from pprint import pprint

from tirumala_pulse.services.etl_service import run
from tirumala_pulse.parsers.statistics_parser import StatisticsParser


def main():

    print("===================================")
    print(" Tirumala Pulse ETL")
    print("===================================\n")

    posts = run()

    statistics_posts = [
        p
        for p in posts
        if StatisticsParser.is_statistics_post(p)
    ]

    print(f"Statistics Posts Found : {len(statistics_posts)}\n")

    for post in statistics_posts:

        report = StatisticsParser.parse(post)

        pprint(report)


if __name__ == "__main__":
    main()