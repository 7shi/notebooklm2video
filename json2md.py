import re, json

def convert(history):
    markdown_text = ""
    for h in history:
        if text := "\n".join(t for t in h["parts"] if isinstance(t, str)):
            text = text.rstrip()
            if h["role"] == "user":
                markdown_text += f"# Prompt\n\n{text}\n\n"
            elif h["role"] == "model":
                markdown_text += f"model:  \n{text}\n\n"
    # Combine consecutive blank lines into one
    markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)
    return markdown_text.rstrip() + "\n"

def print_convert(history):
    print(convert(history), end="")

def convert_json_to_markdown(json_data):
    history = []
    for chunk in json_data["chunkedPrompt"]["chunks"]:
        if text := chunk.get("text", ""):
            history.append({"role": chunk["role"], "parts": [text]})
    return convert(history)

def convert_json_file_to_markdown(json_file, md_file):
    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    markdown_text = convert_json_to_markdown(json_data)
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown_text)

if __name__ == "__main__":
    import sys, os
    args = sys.argv[1:]
    if len(args) < 1:
        print(f"Usage: python {sys.argv[0]} json [...]", file=sys.stderr)
        sys.exit(1)
    for arg in args:
        md = os.path.splitext(arg)[0] + ".md"
        convert_json_file_to_markdown(arg, md)
        print(f"{arg} => {md}")
