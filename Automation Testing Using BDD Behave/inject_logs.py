import re

with open('tests/test_test_case.py', 'r') as f:
    lines = f.readlines()

new_lines = []
has_logging = False
for line in lines:
    if 'import logging' in line:
        has_logging = True

if not has_logging:
    new_lines.append('import logging\n')
    new_lines.append('logger = logging.getLogger()\n')

for line in lines:
    new_lines.append(line)
    match = re.search(r'(\s+)with allure\.step\("([^"]+)"\):', line)
    if match:
        indent = match.group(1)
        step_text = match.group(2)
        new_lines.append(f'{indent}    logger.info("Executing step: {step_text}")\n')

with open('tests/test_test_case.py', 'w') as f:
    f.writelines(new_lines)
