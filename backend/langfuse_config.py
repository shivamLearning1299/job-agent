from dotenv import load_dotenv
load_dotenv()

import os
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

def get_langfuse_handler():
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host       = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    if not public_key or not secret_key:
        print("⚠️  LangFuse keys not found in .env — skipping tracing")
        return None

    Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=host
    )

    handler = CallbackHandler(
        public_key=public_key,
        update_trace=True
    )

    print("✅ LangFuse handler ready — traces will appear in dashboard")
    return handler

if __name__ == "__main__":
    handler = get_langfuse_handler()
    if handler:
        print("🎉 LangFuse connected successfully!")
        print("   Dashboard: https://cloud.langfuse.com")
