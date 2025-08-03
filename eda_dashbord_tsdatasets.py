
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display, clear_output


def create_eda_dashboard(df, target_cols=['price_actual', 'total_load_actual']):
    """
    インタラクティブなEDAダッシュボードを表示します。

    Parameters:
    -----------
    df : pd.DataFrame
        DatetimeIndexをインデックスに持ち、分析対象となる数値列を含むデータフレーム。
    target_cols : list of str
        相関ヒートマップで表示したい主要変数名のリスト。
    """

    assert isinstance(df.index, pd.DatetimeIndex), "データフレームのインデックスがDatetimeIndexである必要があります。"
    
    #ウィジェット設定
    col_selector = widgets.Dropdown(
        options=df.columns,
        description='列名:',
        layout=widgets.Layout(width='50%')
    )

    plot_selector = widgets.Dropdown(
        options=['ヒストグラム', '時系列プロット', '相関ヒートマップ'],
        description='可視化:',
        layout=widgets.Layout(width='50%')
    )

    window_slider = widgets.IntSlider(value=24, 
                                      min=1, maz=168,
                                      step=1,
                                      description='MA時間:')
    
    start_picker = widgets.DatePicker(description=f'開始日:')
    end_picker = widgets.DatePicker(description=f'終了日:')
    
    weekday_selecter = widgets.SelectMultiple(
        options=[('月', 0), ('火', 1), ('水', 2), ('木', 3), ('金', 4), ('土', 5), ('日', 6)],
        value=[0,1,2,3,4],
        description='曜日:'
    )

    time_range_slider = widgets.IntRangeSlider(
        value=[0,12],
        min=0,
        max=23,
        step=1,
        description='時間帯:',
        readout=True,
        layout=widgets.Layout(width='60%')
    )

    out = widgets.Output()
 
    # 更新関数
    def update_dashboard(change=None):
        with out:
            clear_output(wait=True)
            col = col_selector.value
            plot_type = plot_selector.value
            window = window_slider.value

            filtered_df = df.copy()
            #期間指定-----------
            start_date, end_date = start_picker.value, end_picker.value
            if start_date and end_date:
                filtered_df = df.loc[start_date:end_date]
            #曜日指定------------
            filtered_df = filtered_df[filtered_df['weekday'].isin(list(weekday_selecter.value))]
            # 時刻帯指定（hour単位）------------
            start_hour, end_hour = time_range_slider.value
            filtered_df = filtered_df[(filtered_df.index.hour >= start_hour) & (filtered_df.index.hour <= end_hour)]

            #情報出力
            print(f'期間:{df.index[0]}～{df.index[-1]}')
            print(f"\n📌 対象列: {col}\n")
            print(f"📋 データ型: {filtered_df[col].dtype}")
            print(f"🧩 欠損値数: {filtered_df[col].isnull().sum()}")
            print("\n📊 要約統計量:\n", filtered_df[col].describe())

            fig, ax = plt.subplots(figsize=(10, 4))
            if plot_type == 'ヒストグラム':
                filtered_df[col].hist(bins=50, ax=ax)
                ax.set_title(f"{col} のヒストグラム")
            elif plot_type == '時系列プロット':
                filtered_df[col].plot(ax=ax, label=col)
                filtered_df[col].rolling(window).mean().plot(label=f'{col} {window}時間移動平均')
                ax.set_title(f"{col}とその移動平均")
                ax.legend()
            elif plot_type == '相関ヒートマップ':
                corr_df = filtered_df[[col] + [c for c in target_cols if c in filtered_df.columns]].corr()
                sns.heatmap(corr_df, annot=True, cmap='coolwarm', ax=ax)
                ax.set_title(f"{col} と主要変数との相関ヒートマップ")
            plt.tight_layout()
            plt.show()

    # イベント設定
    for widget in [col_selector, plot_selector, window_slider, weekday_selecter, start_picker, end_picker, time_range_slider]:
        widget.observe(update_dashboard, names='value')

    display(widgets.VBox([col_selector, plot_selector, window_slider, weekday_selecter, start_picker, end_picker, time_range_slider]))
    display(out)
    update_dashboard()