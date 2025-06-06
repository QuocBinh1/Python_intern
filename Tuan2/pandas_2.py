import pandas as pd
import numpy as np

#nhan vien
df_employee = {
    'ID': [101, 102, 103, 104, 105, 106],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'Age': [25, np.nan, 30, 22, 28, 35],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'Salary': [700, 800, 750, np.nan, 710, 770]
}
#phong ban 
df_department = {
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
}
dp_employee = pd.DataFrame(df_employee)
dp_department = pd.DataFrame(df_department)

#1 kiểm tra dữ liệu null    
# print(dp_employee.isnull())

#2 Xoá dòng có hơn 2 giá trị bị thiếu
# print(dp_employee[dp_employee.isnull().sum(axis=1) <= 2])

#3 thay thế tên bằng 'chưa rõ'
dp_employee['Name'] = dp_employee['Name'].fillna('Chưa rõ')

#3_1 tính giá trị trung bình cho cột Age và điền vào các giá trị thiếu
dp_employee['Age'] = dp_employee['Age'].fillna(dp_employee['Age'].mean())

#3_2 thay thế lương bằng giá trị trước đó
dp_employee['Salary'] = dp_employee['Salary'].fillna(method='ffill')

#3_3thay nan cột Department bằng 'Unknown'
dp_employee['Department'] = dp_employee['Department'].fillna('Unknown')

#4 Chuyển kiểu dữ liệu
dp_employee['Age'] = dp_employee['Age'].astype(int)
dp_employee['Salary'] = dp_employee['Salary'].astype(int)

#5 Tạo cột Salary_after_tax
dp_employee['Salary_after_tax'] = dp_employee['Salary'] * 0.9

#6 Lọc nhân viên phòng IT và tuổi > 25
filtered = dp_employee[(dp_employee['Department'] == 'IT') & (dp_employee['Age'] > 25)]
# print(filtered)

#7 Sắp xếp theo Salary_after_tax giảm dần
sorted_df = dp_employee.sort_values(by='Salary_after_tax', ascending=False)
# print(sorted_df)

#8 Nhóm theo Department và tính lương TB
mean_salary = dp_employee.groupby('Department')['Salary'].mean()
# print(mean_salary)

#9 Nối với bảng quản lý
merged_df = pd.merge(dp_employee, dp_department, on='Department', how='left')
print(merged_df)

#10 Thêm nhân viên mới
new_employees = pd.DataFrame({
    'ID': [107, 108],
    'Name': ['Phúc', 'Quỳnh'],
    'Age': [26, 29],
    'Department': ['Marketing', 'HR'],
    'Salary': [780, 800],
    'Salary_after_tax': [790 * 0.9, 810 * 0.9]
})
dp_employee_updated = pd.concat([dp_employee, new_employees], ignore_index=True)




# print(dp_employee)
