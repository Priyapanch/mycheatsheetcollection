import pandas as pd
from functools import reduce

# Sample DataFrames
df1 = pd.DataFrame({"id":[1,2,3], "dept":["HR","IT","FIN"]})
df2 = pd.DataFrame({"id":[1,2,4], "salary":[50,60,80]})
df3 = pd.DataFrame({"id":[1,3,4], "bonus":[5,7,9]})
df4 = pd.DataFrame({"id":[2,3,5], "location":["NY","SF","CHI"]})
df5 = pd.DataFrame({"id":[1,2,3,6], "grade":["A","B","C","D"]})
df6 = pd.DataFrame({"id":[1,3,5,6], "manager":["M1","M2","M3","M4"]})

# ---- 1. Sequential Merge (step-by-step, less readable with many DFs) ----
merged_seq = df1.merge(df2, on="id", how="outer") \
                .merge(df3, on="id", how="outer") \
                .merge(df4, on="id", how="outer") \
                .merge(df5, on="id", how="outer") \
                .merge(df6, on="id", how="outer")

print("Sequential Merge Result:")
print(merged_seq)


# ---- 2. Functional Reduce (scales better for 5–6+ DataFrames) ----
dfs = [df1, df2, df3, df4, df5, df6]

merged_reduce = reduce(lambda left, right: pd.merge(left, right, on="id", how="outer"), dfs)

print("\nReduce Merge Result:")
print(merged_reduce)


# ---- 3. Conditional / Mixed Joins (different join types per DF) ----
merged_mixed = df1.merge(df2, on="id", how="inner") \
                  .merge(df3, on="id", how="left") \
                  .merge(df4, on="id", how="outer") \
                  .merge(df5, on="id", how="inner") \
                  .merge(df6, on="id", how="left")

print("\nMixed Join Result:")
print(merged_mixed)
import pandas as pd
from functools import reduce

# Example DataFrames with two join keys: (id, year)
df1 = pd.DataFrame({
    "id":[1,2,3],
    "year":[2020,2020,2021],
    "dept":["HR","IT","FIN"]
})

df2 = pd.DataFrame({
    "id":[1,2,4],
    "year":[2020,2020,2021],
    "salary":[50,60,80]
})

df3 = pd.DataFrame({
    "id":[1,3,4],
    "year":[2020,2021,2021],
    "bonus":[5,7,9]
})

df4 = pd.DataFrame({
    "id":[2,3,5],
    "year":[2020,2021,2021],
    "location":["NY","SF","CHI"]
})

df5 = pd.DataFrame({
    "id":[1,2,3,6],
    "year":[2020,2020,2021,2021],
    "grade":["A","B","C","D"]
})

df6 = pd.DataFrame({
    "id":[1,3,5,6],
    "year":[2020,2021,2021,2021],
    "manager":["M1","M2","M3","M4"]
})

# ---- 1. Sequential Multi-key Merge ----
merged_seq = df1.merge(df2, on=["id","year"], how="outer") \
                .merge(df3, on=["id","year"], how="outer") \
                .merge(df4, on=["id","year"], how="outer") \
                .merge(df5, on=["id","year"], how="outer") \
                .merge(df6, on=["id","year"], how="outer")

print("Sequential Multi-Key Merge:")
print(merged_seq)


# ---- 2. Functional Reduce with Multi-keys ----
dfs = [df1, df2, df3, df4, df5, df6]
merged_reduce = reduce(
    lambda left, right: pd.merge(left, right, on=["id","year"], how="outer"), dfs
)

print("\nReduce Multi-Key Merge:")
print(merged_reduce)


# ---- 3. Mixed Join Types (different strategies per DF) ----
merged_mixed = df1.merge(df2, on=["id","year"], how="inner") \
                  .merge(df3, on=["id","year"], how="left") \
                  .merge(df4, on=["id","year"], how="outer") \
                  .merge(df5, on=["id","year"], how="inner") \
                  .merge(df6, on=["id","year"], how="left")

print("\nMixed Multi-Key Join:")
print(merged_mixed)


