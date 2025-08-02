# EDA Interactive Dashboard

📊 Python × ipywidgets によるインタラクティブな EDA ダッシュボードです。  
日時インデックスを持つ時系列データを対象に、以下のような可視化ができます：

- ヒストグラム
- 時系列プロット（移動平均付き）
- 相関ヒートマップ

## 🚀 特徴

- 日付範囲、曜日、時間帯でのデータフィルタリング
- ドロップダウン・スライダーを使った直感的な操作
- `matplotlib` / `seaborn` による統計グラフ描画

## 📦 必要ライブラリ（requirements.txt あり）

- pandas
- matplotlib
- seaborn
- ipywidgets
- jupyter

インストール例：

```bash
pip install -r requirements.txt


## 使い方(Notebook例)
from eda_dashboard import create_eda_dashboard
create_eda_dashboard(df)

## DataFrameの前提条件：
インデックスが pd.DatetimeIndex であること
weekday 列（0〜6で曜日を表す）が含まれていること

## ディレクトリの前提条件
eda_dashbord_tsdatasets.py を作業用ディレクトリに格納してください。

## Tips：日本語フォントの警告が出る場合
Notebookで描画時に UserWarning: Glyph XXXX missing from font などが出る場合は、以下のコードをNotebookの先頭に追加してください：

import matplotlib
matplotlib.rcParams['font.family'] = 'Yu Gothic'  # Windows向け
matplotlib.rcParams['axes.unicode_minus'] = False