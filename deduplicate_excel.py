import pandas as pd

def deduplicate_excel_by_columns(input_file, output_file):
    try:
        # 读取Excel文件，不指定header，让pandas自动生成列名，方便iloc索引
        df = pd.read_excel(input_file, header=None)
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径：{input_file}")
        return
    except Exception as e:
        print(f"读取Excel文件时发生错误：{e}")
        return

    # 检查列数是否足够
    if df.shape[1] < 10:
        print("错误：Excel文件至少需要10列数据（索引0-9）才能执行去重和条件判断。")
        return

    # 将第二列和第三列（索引1和2）作为唯一键
    # 使用astype(str)确保所有类型都可以进行字符串拼接，避免类型不一致导致的问题
    df['unique_key'] = df.iloc[:, 1].astype(str) + '_' + df.iloc[:, 2].astype(str)

    # 创建一个空的DataFrame来存储去重后的结果
    deduplicated_df = pd.DataFrame(columns=df.columns)

    # 按唯一键分组处理
    for key, group in df.groupby('unique_key'):
        # 取分组中的第一行作为基础行
        base_row = group.iloc[0].copy()

        # 检查第9列（索引8）和第10列（索引9）是否存在'Y'
        # 如果分组中任一行的第9列包含'Y'，则最终结果的第9列为'Y'，否则为'N'
        if 'Y' in group.iloc[:, 8].astype(str).values:
            base_row[8] = 'Y'
        else:
            base_row[8] = 'N'

        # 如果分组中任一行的第10列包含'Y'，则最终结果的第10列为'Y'，否则为'N'
        if 'Y' in group.iloc[:, 9].astype(str).values:
            base_row[9] = 'Y'
        else:
            base_row[9] = 'N'

        # 将处理后的行添加到结果DataFrame
        deduplicated_df = pd.concat([deduplicated_df, pd.DataFrame([base_row])], ignore_index=True)

    # 移除临时创建的unique_key列
    deduplicated_df = deduplicated_df.drop(columns=['unique_key'])

    try:
        # 保存处理后的Excel文件，不包含索引
        deduplicated_df.to_excel(output_file, index=False, header=False)
        print(f"Excel文件去重和更新完成，结果已保存至：{output_file}")
    except Exception as e:
        print(f"保存Excel文件时发生错误：{e}")

if __name__ == "__main__":
    # 请替换为您的输入和输出文件路径
    input_excel_file = '/Users/handing1993/Desktop/newresult.xlsx'  # 您的输入Excel文件路径
    output_excel_file = '/Users/handing1993/Desktop/newoutput.xlsx' # 处理后的输出Excel文件路径

    deduplicate_excel_by_columns(input_excel_file, output_excel_file)