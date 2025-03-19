import os
import markdown
import jinja2

env = jinja2.Environment(loader= jinja2.FileSystemLoader("."))

data = {}

def generate_posts() -> None:
    posts = []
    with os.scandir("./md") as it:
        for entry in it:
            with open(entry, "r") as file:
                lines = file.readlines()
                metadata = {}
                content_start = 0
                if lines[0].strip() == "---":
                    for i, line in enumerate(lines[1:], start=1):
                        if line.strip() == "---":
                            content_start = i + 1
                            break
                        key, value = line.split(":", 1)
                        metadata[key.strip()] = value.strip()
                content = "".join(lines[content_start:])
                rendered = markdown.markdown(content, extensions=["fenced_code", "codehilite"])
                rendered = "<meta name='viewport' content='width=device-width, initial-scale=1.0' /><link rel='stylesheet' type='text/css' href='/gen/style.css?r=a'><!-- Google tag (gtag.js) --><script async src='https://www.googletagmanager.com/gtag/js?id=G-HQESZYRT07'></script><script>window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-HQESZYRT07');</script><title>" + metadata['title'] + "</title><h1>"+ metadata['title'] + "</h1><p class='date'>published on " + metadata['date'] + "</p><hr>" + rendered
                with open(f"./gen/{entry.name.rstrip('.md')}.html", "w") as f:
                    f.write(rendered)
                data[f"/gen/{entry.name.rstrip('.md')}.html"] = metadata
                posts.append({"url": f"/gen/{entry.name.rstrip('.md')}.html", "metadata": metadata})

    # Render index.html
    template = env.get_template("index.jinja")
    print(posts)
    with open("./index.html", "w") as f:
        f.write(template.render(blogs=data))

if __name__ == "__main__":
    generate_posts()
