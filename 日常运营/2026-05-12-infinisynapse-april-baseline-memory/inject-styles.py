import re, sys, base64

html = open('article-official.html', 'r', encoding='utf-8').read()

# 各标签默认样式(不覆盖已有 style 的元素, 例如图片占位符 p)
TAG_STYLES = {
    'h2': 'font-size:18px;color:#1e6fff;line-height:1.75;text-align:left;font-weight:bold;margin:1.2em 0 0.6em;',
    'h3': 'font-size:16px;color:#333;line-height:1.75;text-align:left;font-weight:bold;margin:1em 0 0.5em;',
    'p':  'font-size:15px;line-height:1.75;text-align:left;letter-spacing:0.5px;',
    'li': 'font-size:15px;line-height:1.75;text-align:left;',
    'blockquote': 'font-size:15px;line-height:1.75;color:#666;border-left:3px solid #1e6fff;padding-left:12px;margin:1em 0;',
    'td': 'font-size:14px;line-height:1.75;padding:6px 8px;',
    'th': 'font-size:14px;line-height:1.75;padding:6px 8px;font-weight:bold;background:#f5f8ff;',
    'table': 'font-size:14px;line-height:1.75;border-collapse:collapse;width:100%;margin:1em 0;',
}

# 用负向先行断言 (?![^>]*style=) 跳过已经有 style 的标签
for tag, style in TAG_STYLES.items():
    html = re.sub(
        r'<' + tag + r'(?![^>]*style=)([^>]*)>',
        f'<{tag} style="{style}"\\1>',
        html
    )

with open('article-official.html', 'w', encoding='utf-8') as f:
    f.write(html)
b64 = base64.b64encode(html.encode('utf-8')).decode('ascii')
with open('article-official.html.b64', 'w', encoding='utf-8') as f:
    f.write(b64)

print(f"Styled HTML: {len(html)} chars")
print(f"Base64: {len(b64)} chars")
