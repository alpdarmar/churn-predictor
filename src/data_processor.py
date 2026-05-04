import pandas as pd
from pathlib import Path

RAW_ROOT = Path("data/raw")
SAMPLED_ROOT = Path("data/sampled")
MEMBERS_PATH = RAW_ROOT / "members_v3.csv"
TRAIN_PATH = RAW_ROOT / "train.csv"
TRANSACTIONS_PATH = RAW_ROOT / "transactions.csv"
USER_LOGS_PATH = RAW_ROOT / "user_logs.csv"

def main():
    SAMPLED_ROOT.mkdir(parents=True, exist_ok=True)




if __name__ == "__main__":
    main()