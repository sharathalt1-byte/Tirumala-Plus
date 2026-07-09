from tirumala_pulse.parsers.statistics_parser import StatisticsParser
from tirumala_pulse.repositories.daily_statistics_repository import (
    DailyStatisticsRepository,
)
from tirumala_pulse.services.etl_service import run


def main():

    print("===================================")
    print(" Tirumala Pulse ETL")
    print("===================================\n")

    repository = DailyStatisticsRepository()

    posts = run()

    statistics_posts = [
        post
        for post in posts
        if StatisticsParser.is_statistics_post(post)
    ]

    print(f"Statistics Posts Found : {len(statistics_posts)}\n")

    for post in statistics_posts:

        statistics = StatisticsParser.parse(post)

        print(statistics)

        repository.insert(statistics)


if __name__ == "__main__":
    main()