import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv('.env.local')

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")


def test_connection():
    """Test basic connection to Supabase"""
    try:
        # Print connection details (without exposing full key)
        print(f"URL: {supabase_url}")
        if supabase_key:
            key_preview = supabase_key[:5] + "..." + \
                supabase_key[-5:] if len(supabase_key) > 10 else "***"
            print(f"Key: {key_preview}")

        # Validate URL and key
        if not supabase_url or not supabase_url.startswith("https://"):
            print("❌ Invalid Supabase URL format. Should start with 'https://'")
            return False

        if not supabase_key:
            print("❌ Missing Supabase key")
            return False

        # Create client
        print("\nAttempting to create Supabase client...")
        supabase = create_client(supabase_url, supabase_key)

        # Make the simplest possible request - just fetch the schema
        print("Attempting simple connection test...")

        # This is the simplest possible query that should work on any Supabase instance
        response = supabase.table("_dummy_query_for_connection_test_").select(
            "*").limit(1).execute()

        # We expect this to fail with a "relation does not exist" error, which means
        # the connection was successful but the table doesn't exist (which is expected)
        print("❌ Unexpected success - this shouldn't happen")
        return True

    except Exception as e:
        error_str = str(e)

        # Check if the error is about the table not existing, which actually means
        # the connection was successful
        if "does not exist" in error_str and "relation" in error_str:
            print("\n✅ Successfully connected to Supabase!")
            print(
                "(The error about a missing table is expected and confirms the connection works)")
            return True
        else:
            print(f"\n❌ Connection failed: {error_str}")

            # Provide more helpful error messages for common issues
            if "JWSInvalidSignature" in error_str:
                print("\nTroubleshooting tips:")
                print("- Check that your SUPABASE_SERVICE_KEY is correct")
                print(
                    "- Make sure you're using the 'service_role' key, not the 'anon' key")
                print("- Verify that the URL and key are from the same project")
            elif "Connection refused" in error_str:
                print("\nTroubleshooting tips:")
                print("- Check that your Supabase instance is running")
                print("- Verify that your SUPABASE_URL is correct")
                print("- Check if there are any network restrictions")

            return False


if __name__ == "__main__":
    print("Testing Supabase connection...")
    test_connection()
