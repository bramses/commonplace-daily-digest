from readwise import read_from_file, write_to_file

def convert_to_md(data):
    md = ""
    if data['books'] is not None and len(data['books']) > 0:
        md += "# Books\n\n"
        for res in data['books']:
            md += f"## {res['readable_title']}\n"
            md += f"*{res['author']}*\n\n"
            md += f"[(affiliate link)](https://www.amazon.com/dp/{res['asin']})\n\n"
            for highlight in res['highlights']:
                md += "{note}\n\n"
                md += f"> {highlight['text']}\n\n"
                md += "---\n\n"
            md += "\n\n"
    if data['articles'] is not None and len(data['articles']) > 0:
        md += "# Articles\n\n"
        for res in data['articles']:
            md += f"## {res['readable_title']}\n"
            md += f"*{res['author']}*\n\n"
            md += f"[(source)]({res['source_url']})\n\n"
            for highlight in res['highlights']:
                md += "{note}\n\n"
                md += f"> {highlight['text']}\n\n"
                md += "---\n\n"
            md += "\n\n"
    return md

def main(read_path="small_readwise.data.clean.json", write_path="readwise.md"):
    data = read_from_file(read_path)
    md = convert_to_md(data)
    write_to_file(md, write_path, is_json=False)

if __name__ == "__main__":
    main()