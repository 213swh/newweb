import pandas as pd
import numpy as np

def merge_excel_files():
    # 文件路径
    file1 = '/Users/handing1993/Desktop/11.xlsx'
    file2 = '/Users/handing1993/Desktop/22.xlsx'
    output_file = '/Users/handing1993/Desktop/merged_result66.xlsx'

    # 读取Excel文件
    df1 = pd.read_excel(file1)  # 主体文件
    # 读取22.xlsx时，假设没有列头，或者第一行就是数据，直接使用索引0和1作为主键
    df2 = pd.read_excel(file2, header=None)  # 被匹配文件，不带列头读取

    # 处理df2中的合并单元格：对用于key的列进行ffill操作
    # 假设合并单元格主要影响用于key的列，这里对第1、2列进行ffill
    df2.iloc[:, 0] = df2.iloc[:, 0].fillna(method='ffill')
    df2.iloc[:, 1] = df2.iloc[:, 1].fillna(method='ffill')
    

    # 为df2创建临时主键列（使用第1、2列，即索引0和1）
    df2['temp_key'] = (
        df2.iloc[:, 0].astype(str) + '|' +  # 第1列（索引0）
        df2.iloc[:, 1].astype(str)          # 第2列（索引1）
    )

    # 为df1创建主键列（使用第二列和第三列，即索引1和2）
    df1['main_key'] = (
        df1.iloc[:, 1].astype(str) + '|' +  # 第二列（索引1）
        df1.iloc[:, 2].astype(str)          # 第三列（索引2）
    )

    # 初始化“有设计”列为'N'
    # 确保“有设计”列存在，如果不存在则创建并填充'N'
    if '有设计' not in df1.columns:
        df1['有设计'] = 'N'
    else:
        df1['有设计'] = df1['有设计'].fillna('N')

    # 获取df2中所有主键的集合
    matched_keys_from_df2 = set(df2['temp_key'])

    # 使用向量化操作更新df1的“有设计”列
    df1['有设计'] = np.where(
        df1['main_key'].isin(matched_keys_from_df2),
        'Y',
        'N'
    )

    # 删除临时创建的主键列
    df1.drop(columns=['main_key'], inplace=True)

    # 保存修改后的df1到新的Excel文件
    df1.to_excel(output_file, index=False)
    print(f"处理完成！修改后的11.xlsx已保存至: {output_file}")

if __name__ == "__main__":
    merge_excel_files()