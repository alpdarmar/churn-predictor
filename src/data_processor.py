import pandas as pd
from pathlib import Path
from tqdm import tqdm

RANDOM_SEED = 1337

# number of samples of each class
N_PER_CLASS = 5000

# size of chunk of data that is read
CHUNK_SIZE = 1_000_000


RAW_ROOT = Path("data/raw")
SAMPLED_ROOT = Path("data/sampled")


MEMBERS_PATH = RAW_ROOT / "members_v3.csv"
TRAIN_PATH = RAW_ROOT / "train.csv"
TRANSACTIONS_PATH = RAW_ROOT / "transactions.csv"
USER_LOGS_PATH = RAW_ROOT / "user_logs.csv"


SAMPLED_MEMBERS_PATH = SAMPLED_ROOT / "members.parquet"
SAMPLED_USERS_PATH = SAMPLED_ROOT / "users.parquet"
SAMPLED_TRANSACTIONS_PATH = SAMPLED_ROOT / "transactions.parquet"
SAMPLED_USER_LOGS_PATH = SAMPLED_ROOT / "user_logs.parquet"


def sample_users():
    if SAMPLED_USERS_PATH.exists():
        df = pd.read_parquet(SAMPLED_USERS_PATH)
        return set(df["msno"])
    users = pd.read_csv(TRAIN_PATH)
    churners = users[users["is_churn"] == 1]
    non_churners = users[users["is_churn"] == 0]
    churner_sample = churners.sample(n=N_PER_CLASS, random_state=RANDOM_SEED)
    non_churner_sample = non_churners.sample(n=N_PER_CLASS, random_state=RANDOM_SEED)
    combined_sample = pd.concat([churner_sample, non_churner_sample])
    combined_sample = combined_sample.sample(frac=1, random_state=RANDOM_SEED)
    combined_sample = combined_sample.reset_index(drop=True)
    combined_sample.to_parquet(SAMPLED_USERS_PATH, index=False)
    return set(combined_sample["msno"])


def filter_members(user_ids):
    if SAMPLED_MEMBERS_PATH.exists():
        return
    members = pd.read_csv(MEMBERS_PATH)
    filtered = members[members["msno"].isin(user_ids)]
    filtered.to_parquet(SAMPLED_MEMBERS_PATH, index=False)
    print(
        f"Filtered members: {len(filtered)} rows kept (out of {len(user_ids)} sampled users)"
    )


def filter_chunked(input_path, output_path, user_ids, desc):
    if output_path.exists():
        return
    chunks = []
    reader = pd.read_csv(input_path, chunksize=CHUNK_SIZE)
    for chunk in tqdm(reader, desc=desc):
        filtered_chunk = chunk[chunk["msno"].isin(user_ids)]
        chunks.append(filtered_chunk)
    filtered = pd.concat(chunks, ignore_index=True)
    filtered.to_parquet(output_path, index=False)
    print(f"{desc}: {len(filtered)} rows kept")


def main():
    SAMPLED_ROOT.mkdir(parents=True, exist_ok=True)
    sampled_user_ids = sample_users()
    filter_members(sampled_user_ids)
    filter_chunked(
        TRANSACTIONS_PATH,
        SAMPLED_TRANSACTIONS_PATH,
        sampled_user_ids,
        "Filtering transactions",
    )
    filter_chunked(
        USER_LOGS_PATH, SAMPLED_USER_LOGS_PATH, sampled_user_ids, "Filtering user logs"
    )


if __name__ == "__main__":
    main()
