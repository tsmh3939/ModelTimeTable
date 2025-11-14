"""
Main setup script for database initialization and data import
Execute all setup tasks in the correct order
"""

from setup import seed, extractor, convert, insert


def main():
    """Execute all setup tasks in order"""
    print("=" * 60)
    print("Starting setup process...")
    print("=" * 60)

    try:
        # Step 1: Seed master data
        print("\n[1/4] Seeding master data...")
        seed()

        # Step 2: Extract CSV data
        print("\n[2/4] Extracting CSV data...")
        extractor()

        # Step 3: Convert CSV data
        print("\n[3/4] Converting CSV data...")
        convert()

        # Step 4: Insert CSV data
        print("\n[4/4] Inserting CSV data...")
        insert()

        print("\n" + "=" * 60)
        print("Setup process completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nSetup process failed: {e}")
        raise


if __name__ == "__main__":
    main()