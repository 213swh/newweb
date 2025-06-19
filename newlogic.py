import pandas as pd
import numpy as np

def merge_excel_files():
    # 文件路径
    file11 = '/Users/handing1993/Desktop/merged_resultww.xlsx'  # 11.xlsx 现在是被匹配和更新的文件
    file_output = '/Users/handing1993/Desktop/output.xlsx'  # output.xlsx 现在是主表
    output_result_file = '/Users/handing1993/Desktop/11_updated.xlsx'  # 修改后的11.xlsx保存到新文件

    # 读取Excel文件
    df11 = pd.read_excel(file11)  # 被匹配和更新的文件
    df_output = pd.read_excel(file_output, header=1)  # 主表，从第二行开始读取，将第二行作为列头

    # 处理df_output中的合并单元格：对用于生成key的列进行ffill操作
    cols_to_fill = [0, 1, 8]  # 第1,2,9列的索引
    for col in cols_to_fill:
        df_output.iloc[:, col] = df_output.iloc[:, col].fillna(method='ffill')

    # 为df_output创建主键列（使用第1、2、9列）
    df_output['output_key'] = (
        df_output.iloc[:, 0].astype(str) + '|' +
        df_output.iloc[:, 1].astype(str) + '|' +
        df_output.iloc[:, 8].astype(str)
    )

    # 为df11创建主键列（使用app_name, event_name, key）
    df11['11_key'] = (
        df11['app_name'].astype(str) + '|' +
        df11['event_name'].astype(str) + '|' +
        df11['key'].astype(str)
    )

    # 初始化/更新"有设计"列
    df11['有设计'] = df11['有设计'].fillna('N')

    # 执行左合并，找出df_output中在df11中没有匹配的行
    merged_df = pd.merge(
        df_output,
        df11[['11_key', '有设计']],  # 只合并需要的列
        left_on='output_key',
        right_on='11_key',
        how='left',
        indicator=True
    )

    # 找出df_output中未在df11中找到匹配的行
    unmatched_in_11 = merged_df[merged_df['_merge'] == 'left_only']

    # 安全检查：确保有足够的列
    if len(df_output.columns) < 10:
        raise ValueError("output.xlsx需要至少10列数据")

    # 提取output.xlsx中未匹配行的指定列
    cols_to_extract = {
        'app_name': 0,    # 第1列
        'event_name': 1,   # 第2列
        'key': 4,         # 第5列
        'col_5': 7,       # 第7列(重复)
        'col_7': 8,       # 第9列
        'col_9': 9
    }

    # 创建新行的DataFrame
    new_rows = []
    for _, row in unmatched_in_11.iterrows():
        new_row = {
            'app_name': row.iloc[cols_to_extract['app_name']],
            'event_name': row.iloc[cols_to_extract['event_name']],
            'key': row.iloc[cols_to_extract['key']],
            'output_col_5': row.iloc[cols_to_extract['col_5']],
            'output_col_7': row.iloc[cols_to_extract['col_7']],
            '有上报': 'N',
            '有设计': 'Y'
        }
        new_rows.append(new_row)

    new_rows_df = pd.DataFrame(new_rows)

    # 将新行追加到df11
    df11_final = pd.concat([df11, new_rows_df], ignore_index=True)

    # 更新"有设计"列状态
    matched_keys = set(df_output['output_key'])
    df11_final['有设计'] = np.where(
        df11_final['11_key'].isin(matched_keys),
        'Y',
        'N'
    )

    # 清理临时列
    df11_final.drop(columns=['11_key'], inplace=True, errors='ignore')

    # 保存结果
    df11_final.to_excel(output_result_file, index=False)
    print(f"处理完成！更新后的11.xlsx已保存至: {output_result_file}")
    print(f"新增了{len(new_rows_df)}行数据")

if __name__ == "__main__":
    merge_excel_files()