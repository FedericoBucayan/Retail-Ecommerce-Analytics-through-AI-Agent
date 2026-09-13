import subprocess
import json

res = subprocess.run('powerbi-report-author validate Retail_Ecommerce_Analytics.Report', shell=True, capture_output=True, text=True)
data = json.loads(res.stdout)
d = data.get('data', {})
print('Result:', d.get('result'))
print('Error Count:', d.get('errorCount'))
print('Warning Count:', d.get('warningCount'))

diag = d.get('diagnostics', {})
errors = diag.get('errors', {})
if errors:
    print('\n=== ERRORS ===')
    for code, val in errors.items():
        items = val.get('items', [])
        print(f"[{code}] ({len(items)} items):")
        for it in items[:5]:
            print("  -", it.get('message'))

warnings = diag.get('warnings', {})
if warnings:
    print('\n=== WARNINGS ===')
    for code, val in warnings.items():
        items = val.get('items', [])
        print(f"[{code}] ({len(items)} items):")
        for it in items[:5]:
            print("  -", it.get('message'))
