import gspread
gc=gspread.service_account(filename='credentials.json')
sh=gc.open_by_key('1GeqprOdvt7H7nFVxM25fEb7t7crRm6TbuD3KSX3Z0c8')
worksheet=sh.sheet1
res=worksheet.get_all_records()
print(len(res))
print(res[0]['flame sensor'])