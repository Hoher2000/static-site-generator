import os, shutil, pathlib
from block import *

def main():

    def recursiv_copy(src, dest, f=True):
        from datetime import datetime
        logtext = []
        if f:            
            with open('logfile.txt', 'w'): pass
        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.mkdir(dest)
        if not f: 
            log = f'{datetime.now()}: directory {src} copied to directory {dest}\n'
            logtext.extend([log])
        for cur_path in os.listdir(src):            
            if os.path.isfile(os.path.join(src, cur_path)):
                shutil.copy(os.path.join(src, cur_path), dest)
                log = f'{datetime.now()}: file {os.path.join(src, cur_path)} copied to directory {dest}\n'
                logtext.extend([log])
            else:
                new_src = os.path.join(src, cur_path)
                new_dest = os.path.join(dest, cur_path)
                recursiv_copy(new_src, new_dest, False)
        with open('logfile.txt', 'a') as l:
            for log in logtext: l.write(log)

    def generate_page(from_path, template_path, dest_path):
        print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
        with open(from_path, 'r') as fp, open(template_path, 'r') as tp:
            markdown = fp.read()
            template = tp.read()
        html_node = markdown_to_html_node(markdown)
        html = html_node.to_html()
        title = extract_title(markdown)
        new_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'w') as gp:
            gp.write(new_html)

    def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
        with open(template_path, 'r') as tp:            
            template = tp.read()
        for cur_path in os.listdir(dir_path_content): 
            path = pathlib.Path(os.path.join(dir_path_content, cur_path))          
            if os.path.isfile(path):
                markdown = path.read_text()
                html_node = markdown_to_html_node(markdown)
                html = html_node.to_html()
                title = extract_title(markdown)
                new_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
                dest_path = pathlib.Path(os.path.join(dest_dir_path, f'{cur_path.split('.')[0]}.html'))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                dest_path.write_text(new_html)
            else:
                new_dir_path_content = path
                new_dest_dir_path = os.path.join(dest_dir_path, cur_path)
                template_path = template_path
                generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path)


    src = '/home/paulina/workspace/github.com/Hoher2000/static_site_generator/static'
    dest = '/home/paulina/workspace/github.com/Hoher2000/static_site_generator/public'

    template_path = '/home/paulina/workspace/github.com/Hoher2000/static_site_generator/template.html'

    dir_path_content = '/home/paulina/workspace/github.com/Hoher2000/static_site_generator/content'
    dest_dir_path = '/home/paulina/workspace/github.com/Hoher2000/static_site_generator/public'

    recursiv_copy(src, dest)
    
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)
           
    
if __name__ == '__main__': 
    main()
