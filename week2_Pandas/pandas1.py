import pandas as pd

data = {
    'Name': ['An', 'Bình', 'Chi', 'Dũng', 'Em', 'Giang', 'Hà', 'Hùng', 'Lan', 'Minh'],
    'Age': [20, 21, 19, 22, 20, 23, 21, 22, 20, 21],
    'Gender': ['Male', 'Male', 'Female', 'Male', 'Female', 'Female', 'Female', 'Male', 'Female', 'Male'],
    'Score': [8.5, 6.0, 4.5, 7.2, 5.0, 9.1, 3.5, 6.8, 8.0, 4.0]
}
df_students = pd.DataFrame(data)
print("DataFrame ban đầu:")
print(df_students)

print("\n#######3 cột đầu tiên #######")
print(df_students.head(3))

print("\n###### index = 2 , cột name ########")
print(df_students.loc[2,"Name"])

print("\n#####index = 9 cột age #########")
print(df_students.loc[9, "Age"])

print("\n######hiển thị 2 cột name và score ########")
print(df_students[["Name" , "Score"]])

print("\n#####add côt pass và true nếu score > 5 #########")
df_students['Pass'] = df_students['Score'] >= 5
print(df_students)
print("\n##### sắp xếp #########")

df_sorted = df_students.sort_values(by='Score', ascending=False)
print(df_sorted)
