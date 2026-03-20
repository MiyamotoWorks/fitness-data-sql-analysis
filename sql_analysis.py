import sqlite3
import pandas as pd

INPUT_FILE = "/sample_data.csv"


def load_data(file_path):
    df = pd.read_csv(file_path)

    # 列名の前後スペース削除
    df.columns = df.columns.str.strip()

    # 列名ゆれ対応
    df = df.rename(columns={
        "５０ｍ走": "50m走",
    })

    return df


def run_sql_analysis(df):
    # メモリ上にDB作成
    conn = sqlite3.connect(":memory:")

    # DataFrame → SQLテーブル
    df.to_sql("fitness", conn, index=False, if_exists="replace")

    # SQLクエリ
    query = """
    SELECT 学年, AVG("50m走") AS avg_50m
    FROM fitness
    GROUP BY 学年
    """

    result = pd.read_sql(query, conn)
    return result


def main():
    df = load_data(INPUT_FILE)
    result = run_sql_analysis(df)

    print("SQL集計結果（学年別50m走平均）")
    print(result)


if __name__ == "__main__":
    main()