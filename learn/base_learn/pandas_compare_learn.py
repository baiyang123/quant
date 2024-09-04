import pandas as pd

'''
https://blog.csdn.net/a13407142317/article/details/141232312 数据的合并与对比
'''
# 必须一样大的两个DataFrame
'''
 comparison_df3 = df1.compare(df2, keep_equal=True)
 self       other self       other self       other
0  NaN         NaN  NaN         NaN  NaN         NaN
1   A1  A1_changed  NaN         NaN  NaN         NaN
2  NaN         NaN   B2  B2_changed  NaN         NaN
3   A3  A3_changed  NaN         NaN   C3  C3_changed
'''


def pandas_compare():
    # 示例数据
    df1 = pd.DataFrame({
        'A': ['A0', 'A1', 'A2', 'A3'],
        'B': ['B0', 'B1', 'B2', 'B3'],
        'C': ['C0', 'C1', 'C2', 'C3'],
    })

    df2 = pd.DataFrame({
        'A': ['A0', 'A1_changed', 'A2', 'A3_changed'],
        'B': ['B0', 'B1', 'B2_changed', 'B3'],
        'C': ['C0', 'C1', 'C2', 'C3_changed']
    })
    comparison_df1 = df1.compare(df2)
    comparison_df2 = df1.compare(df2, keep_shape=True)
    comparison_df3 = df1.compare(df2, keep_equal=True)
    comparison_df4 = df1.compare(df2, align_axis=0)
    print(df1,df2)
    print(comparison_df1,comparison_df2,comparison_df3,comparison_df4)


'''
  key  value
0   A      1
1   B      2
2   C      3
3   D      4
4   E      5
   0  1    2    3
0  A  1    D  4.0
1  B  2    E  5.0
2  C  3  NaN  NaN
  key  value
0   A      1
1   B      2
2   C      3
3   D      4
  key  value
0   A     10
1   B     20
2   C     30
3   D     40
'''


def pandas_change():
    df1 = pd.DataFrame({
        'key': ['A', 'B', 'C'],
        'value': [1, 2, 3]
    })
    df2 = pd.DataFrame({
        'key': ['D', 'E'],
        'value': [4, 5]
    })
    # 追加数据 ignore_index=True：重新索引合并后的 DataFrame。
    df3 = df1._append(df2, ignore_index=True)
    #  同df4 = pd.concat([df1, df2], axis=0, ignore_index=True)
    print(df3)
    # 使用 concat 追加数据
    df4 = pd.concat([df1, df2], axis=1, ignore_index=True)
    print(df4)
    df1.loc[len(df1)] = ['D', 4]
    print(df1)
    # 追加新列或改列
    df1 = df1.assign(value=[10, 20, 30, 40])
    print(df1)

'''
  key  value_x  value_y
0   A      1.0      NaN
1   B      2.0      5.0
2   C      3.0      NaN
3   D      4.0      6.0
4   E      NaN      7.0
5   F      NaN      8.0
'''


def pandas_merge():
    df1 = pd.DataFrame({
        'key': ['A', 'B', 'C', 'D'],
        'value': [1, 2, 3, 4]
    })
    df2 = pd.DataFrame({
        'key': ['B', 'D', 'E', 'F'],
        'value': [5, 6, 7, 8]
    })
    # 使用 key 列进行内连接
    print(df1)
    print(df2)
    merged_df = pd.merge(df1, df2, on='key', how='inner')
    print(merged_df)
    left_merged_df = pd.merge(df1, df2, on='key', how='left')
    print(left_merged_df)
    # 右连接，保留右表的所有数据
    right_merged_df = pd.merge(df1, df2, on='key', how='right')
    print(right_merged_df)
    # 外连接，保留两表的并集
    outer_merged_df = pd.merge(df1, df2, on='key', how='outer')
    print(outer_merged_df)
    # 基于不同列名进行合并
    df11 = pd.DataFrame({
        'key1': ['A', 'B', 'C', 'D'],
        'value1': [1, 2, 3, 4]
    })
    df22 = pd.DataFrame({
        'key2': ['B', 'D', 'E', 'F'],
        'value2': [5, 6, 7, 8]
    })
    merged_df_diff_keys = pd.merge(df11, df22, left_on='key1', right_on='key2', how='inner')
    print(merged_df_diff_keys)
    # 合并时，避免列名冲突------------有用得mr
    merged_df_suffix = pd.merge(df1, df2, on='key', how='outer', suffixes=('_left', '_right'))
    print(merged_df_suffix)


# 数据拼接
def pandas_concatenate():
    df1 = pd.DataFrame({
        'A': ['A0', 'A1', 'A2', 'A3'],
        'B': ['B0', 'B1', 'B2', 'B3'],
        'C': ['C0', 'C1', 'C2', 'C3']
    })

    df2 = pd.DataFrame({
        'A': ['A0', 'A1_changed', 'A2', 'A3_changed'],
        'B': ['B0', 'B1', 'B2_changed', 'B3'],
        'C': ['C0', 'C1', 'C2', 'C3_changed']
    })

    # 比较两个 DataFrame 的不同
    print(df1)
    print(df2)
    comparison_df = df1.compare(df2)
    print(comparison_df)
    comparison_df = df1.compare(df2, keep_shape=True)
    print(comparison_df)
    comparison_df = df1.compare(df2, keep_equal=True)
    print(comparison_df)
    comparison_df = df1.compare(df2, align_axis=0)
    print(comparison_df)
    # 详细示例
    df1 = pd.DataFrame({
        'Experiment': ['Exp1', 'Exp2', 'Exp3', 'Exp4'],
        'Result': [0.95, 0.85, 0.78, 0.65]
    })

    df2 = pd.DataFrame({
        'Experiment': ['Exp1', 'Exp2', 'Exp3', 'Exp4'],
        'Result': [0.95, 0.82, 0.78, 0.67]
    })
    print(df1)
    print(df2)
    comparison_df = df1.compare(df2)
    print(comparison_df)



if __name__ == '__main__':
    pandas_merge()