import os
import warnings
import pandas as pd
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent

warnings.filterwarnings("ignore")

load_dotenv()


def load_file(file_path):
    """Load CSV, XLSX, or XLS files safely."""

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        try:
            return pd.read_csv(file_path, encoding="cp1252")
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding="utf-8")

    elif ext == ".xlsx":
        return pd.read_excel(file_path, engine="openpyxl")

    elif ext == ".xls":
        return pd.read_excel(file_path, engine="xlrd")

    else:
        raise ValueError(f"Unsupported file type: {ext}")


def create_audit_agent():
    """Initializes the LLM and search tool."""

    llm = ChatOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url=os.getenv("GROQ_BASE_URL"),
        model=os.getenv("GROQ_MODEL"),
        temperature=0.0
    )

    search_tool = DuckDuckGoSearchRun()

    system_message = """
You are AuditEye, an elite forensic procurement auditor.

Your job is to analyze procurement data for anomalies.

RULES:
1. Detect the currency used in the prompt.
2. Always use the search tool to find the current market price of the item.
3. Convert the market price to match the currency in the prompt before comparing.
4. Calculate the markup percentage between the listed price and the market price.
5. If the markup is over 50%, flag it as an ANOMALY.
6. Be concise, professional, and clearly explain your math.
"""

    agent = create_agent(
        model=llm,
        tools=[search_tool],
        system_prompt=system_message
    )

    return agent


if __name__ == "__main__":
    print("🧠 Booting up AuditEye Agent...")

    auditor = create_audit_agent()

    print("📂 Loading procurement data...")

    try:
        file_path = "contracts_raw.xlsx"

        df = load_file(file_path)

        print("✅ File loaded successfully.")
        print("Columns found:")
        print(df.columns.tolist())

        sample_row = df.iloc[1]

        item_desc = sample_row["Project Name"]
        price = sample_row["Amount Awarded"]

        test_case = f"""
Analyze this real COVID-19 procurement item in the Philippines:

Item Description: {item_desc}
Listed Total Price Paid: ₱{price:,.2f}
"""

        print(f"\n🚨 Investigating: {item_desc}")
        print(f"💰 Price to verify: ₱{price:,.2f}")
        print("\n🔎 Watch the agent search and analyze...\n")

        result = auditor.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": test_case
                }
            ]
        })

        final_message = result["messages"][-1].content

        print("\n==================================")
        print("FINAL FORENSIC REPORT:")
        print("==================================\n")
        print(final_message)

    except FileNotFoundError:
        print("❌ Error: File not found.")
        print(f"👉 Make sure '{file_path}' is in the same folder as this script.")

    except KeyError as e:
        print(f"❌ Missing column: {e}")
        print("👉 Check your CSV/Excel column names.")
        print("Available columns are:")
        print(df.columns.tolist())

    except Exception as e:
        print("❌ Unexpected error:")
        print(e)
