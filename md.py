from readwise import read_from_file, write_to_file
from dotenv import load_dotenv
import os
import markdown
load_dotenv()

amazon_tag= os.environ.get("AMAZON_TAG")


def convert_to_md(data):
    md = ""
    idx = 0
    if data['books'] is not None and len(data['books']) > 0:
        md += "# Books\n\n"
        for res in data['books']:
            md += f"## {res['readable_title']}\n"
            md += f"*{res['author']}*\n\n"
            md += f"[(affiliate link)](https://www.amazon.com/dp/{res['asin']}/?ref=nosim?tag={amazon_tag})\n\n"
            for highlight in res['highlights']:
                md += f'<div id="highlight-{idx}" styles="all: initial;">\n\n'
                md += f"{highlight['note']}\n\n" if highlight['note'] and len(highlight['note']) > 0 else "{note}\n\n"
                md += "<br />\n\n"
                md += f"> {highlight['text']}\n\n"
                md += '</div>\n\n'
                md += generate_copy_text_to_clipboard_button(idx, res['readable_title'], res['author']) + "\n\n"
                md += "---\n\n"
                idx += 1
            md += "\n\n"
    if data['articles'] is not None and len(data['articles']) > 0:
        md += "# Articles\n\n"
        for res in data['articles']:
            md += f"## {res['readable_title']}\n"
            md += f"*{res['author']}*\n\n"
            md += f"[(source)]({res['source_url']})\n\n"
            for highlight in res['highlights']:
                md += f'<div id="highlight-{idx}" styles="all: initial;">\n\n'
                md += f"{highlight['note']}\n\n" if highlight['note'] and len(highlight['note']) > 0 else "{note}\n\n"
                md += "<br />\n\n"
                md += f"> {highlight['text']}\n\n"
                md += '</div>\n\n'
                md += generate_copy_text_to_clipboard_button(idx, res['readable_title'], res['author']) + "\n\n"
                md += "---\n\n"
                idx += 1
            md += "\n\n"
    return md


def md_to_html(md):
    return markdown.markdown(md)

def generate_copy_text_to_clipboard_button(idx, title, author):
    # generate html button
    btn_str = f'''<button 
 id="copyToClipboard-{idx}" 
 style="
background-color: transparent;
border: 2px solid #C7C6C1; /* your border color */
color: #C7C6C1; /* text color, same as border */
padding: 10px 20px;
text-align: center;
text-decoration: none;
display: inline-block;
font-size: 16px;
margin: 4px 2px;
cursor: pointer;
transition: all 0.3s ease 0s;"
 onmouseover="mouseOverCopyShareButton({idx})"
 onmouseout="mouseOutCopyShareButton({idx})"
 onclick="copyTextToClipboardCopyShareButton({idx}, '{str(idx) + " " + title + " " + author}', 'Copy to Clipboard')"
>Copy to Clipboard</button>
    '''
    # remove all newlines
    btn_str = btn_str.replace('\n', '')

    return btn_str

def main(read_path="small_readwise.data.clean.json", write_path="readwise.md"):
    data = read_from_file(read_path)
    md = convert_to_md(data)
    write_to_file(md, write_path, is_json=False)
    html = md_to_html(md)
    split_path = write_path.split(".")
    write_path_html = ".".join(split_path[:-1]) + ".html" + ".txt"
    write_to_file(html, write_path_html, is_json=False)

if __name__ == "__main__":
    main()