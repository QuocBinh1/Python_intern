#xu li file excel bang pandas(openpyxl)
import openpyxl as px
from openpyxl.styles import Font

workbook = px.Workbook()
sheet = workbook.active

# Ghi dữ liệu
sheet['A1'] = 'Hello'
font = Font(bold=True, color='000000')
sheet['A1'].font = font

# Lưu lại
workbook.save('data.xlsx')