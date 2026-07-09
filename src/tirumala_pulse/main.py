from tirumala_pulse.database.connection import supabase


def main():

    print("Connecting to Supabase...")

    response = (
        supabase
        .table("daily_statistics")
        .select("*")
        .limit(1)
        .execute()
    )

    print("✅ Connected Successfully!")

    print(response.data)


if __name__ == "__main__":
    main()