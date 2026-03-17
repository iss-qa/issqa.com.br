import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to find cv-item blocks
# We will identify if it's in the 'Formação' column or 'Profissional' column
# Actually, let's just find each cv-item block and inject sequentially.

formacao_count = 1
prof_count = 1
def replace_cv_item(match):
    global formacao_count, prof_count
    
    block = match.group(0)
    
    # Check which column it belongs to based on some context, 
    # but since regex sub is sequential, we can just use a counter.
    # There are 12 formacao, then 10 profissionais
    if formacao_count <= 12:
        prefix = f"cv-f{formacao_count}"
        formacao_count += 1
    else:
        prefix = f"cv-p{prof_count}"
        prof_count += 1
        
    # Replace h5
    block = re.sub(r'<h5>(.*?)</h5>', fr'<h5 data-i18n="{prefix}-t">\1</h5>', block, count=1)
    # Replace p with em
    block = re.sub(r'<p><em>(.*?)</em></p>', fr'<p><em data-i18n="{prefix}-i">\1</em></p>', block, count=1)
    # Replace last p
    block = re.sub(r'<p>((?!<).+?)</p>', fr'<p data-i18n="{prefix}-d">\1</p>', block, count=1)
    
    return block

# Find all cv-item divs
new_content = re.sub(r'<div class=\'cv-item\' data-anime="up">.*?</div>', replace_cv_item, content, flags=re.DOTALL)

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("CV tags updated.")
