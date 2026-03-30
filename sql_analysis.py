import sqlite3
import pandas as pd

# CSVファイルのパス
INPUT_FILE = "sample_data.csv"


def load_data(file_path):
    """CSVデータを読み込み、列名を整える"""
    df = pd.read_csv(file_path)

    # 列名の前後スペース削除
    df.columns = df.columns.str.strip()

    # 列名ゆれ対応（50m走だけ例）
    df = df.rename(columns={
        "５０ｍ走": "50m走",
    })

    return df


def run_sql_analysis(df):
    """DataFrameをSQLiteに読み込み、SQLで分析"""
    # メモリ上に一時的なDBを作成
    conn = sqlite3.connect(":memory:")

    # DataFrame → SQLテーブルに変換
    df.to_sql("fitness", conn, index=False, if_exists="replace")

    # 学年ごとの50m走平均を計算するSQLクエリ
    query = """
    SELECT 学年, AVG("50m走") AS avg_50m
    FROM fitness
    GROUP BY 学年
    """

    # SQL実行結果をDataFrameで取得
    result = pd.read_sql(query, conn)
    return result


def main():
    # データ読み込み
    df = load_data(INPUT_FILE)

    # SQL分析実行
    result = run_sql_analysis(df)

    # 結果表示
    print("SQL集計結果（学年別50m走平均）")
    print(result)


if __name__ == "__main__":
    main()
