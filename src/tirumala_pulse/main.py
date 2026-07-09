from tirumala_pulse.services.etl_service import ETLService


def main():

    print("===================================")
    print(" Tirumala Pulse ETL")
    print("===================================\n")

    etl = ETLService()

    etl.run()


if __name__ == "__main__":
    main()