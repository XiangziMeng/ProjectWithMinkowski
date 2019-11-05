#coding: utf-8
import os

def extract(input_file, output_file):
    try:
        output_file_fp = open(output_file, "w")
        with open(input_file, 'rb') as fp:
            html_text = fp.read()
            html_text = str(html_text, encoding="gbk")
            start, end = 0, 0
            while start >= 0 and end >= 0: 
                output_text = html_text[start:end]
                output_text = output_text.replace("<font color=E6E6DD> www.6park.com</font><p>", " ")
                output_text = output_text.replace("<br>", " ")
                output_text = output_text.replace("<pre>", "")
                output_text = output_text.replace("</pre>", "")
                output_file_fp.write(output_text)
                output_file_fp.write("\n")
                start, end = start + 1, end + 1
                start, end = html_text.find("<pre>", start), html_text.find("</pre>", end)
        output_file_fp.close()
    except Exception as e:
        print (input_file, e)
        os.remove(output_file)

if __name__ == "__main__":
    root = "data/20191105" 
    html_file_list = os.listdir("%s/raw" % root)
    for html_file in html_file_list:
        html_file_full_path = os.path.join(root, "raw", html_file)

        text_file = html_file.replace("html", "txt")
        text_file_full_path = os.path.join(root, "clean", text_file)

        extract(html_file_full_path, text_file_full_path)
