import re
import os
import bs4
from bs4 import BeautifulSoup

"""
Script for simplifying html files
This script can be used for:
- Removing all sub-trees of the HTML DOM which do not contain textual elements 
- Filtering out all headers, footers, copyrights, images, and iFrames. 
- Folding consecutive <div> elements into a singular <div> element with merged attributes. 
- Removing hidden elements
- Removing scripts and internal CSS style
"""

# remove comments from html file
def remove_comments(html):
    return re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

# remove html header from html file
def remove_header(html):
    return re.sub(r'<head>.*?</head>', '', html, flags=re.DOTALL)

# remove html footer from html file
def remove_footer(html):
    return re.sub(r'<footer>.*?</footer>', '', html, flags=re.DOTALL)

# remove html copyright from html file
def remove_copyright(html):
    return re.sub(r'<p class="copyright">.*?</p>', '', html, flags=re.DOTALL)

# remove iframe from html file
def remove_iframe(html):
    return re.sub(r'<iframe.*?>', '', html, flags=re.DOTALL)

# remove images from html file
def remove_images(html):
    return re.sub(r'<img.*?>', '', html, flags=re.DOTALL)

# remove script tags from html file
def remove_script(html):
    return re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)

# getcomputedstyle from scratch (not in browser)
def get_computed_style(element, style_property, html):
    style = get_element_style(element, html)
    if style:
        style = re.findall(r'\{.*?\}', style, flags=re.DOTALL)
        style=''.join(style).replace('{','').replace('}','')
        style = style.split(';')
        for s in style:
            if s.startswith(style_property):
                return s.split(':')[1]
    return element.get(style_property)

# extract style from html file
def get_element_style(element, html):
    style = re.findall(r'<style.*?</style>', html, flags=re.DOTALL)
    # concatenate all style tags
    style = ''.join(style)
    # remove /n and space from style
    style = style.replace('\n', '').replace(' ', '').replace('\t', '')
    styles = re.findall(r'.*?{.*?}', style, flags=re.DOTALL)
    if element.get('id'):
        if find_element(styles,'#' + element.get('id')):
            return find_element(styles,'#' + element.get('id'))
    elif element.get('class'):
        for c in element.get('class'):
            if find_element(style,'.' + c):
                return find_element(style,'.' + c)
    else:
        return element.get('style')

# find an element in the list starting with a specific string
def find_element(list, string):
    for element in list:
        if element.startswith(string):
            return element
    return None

# remove hidden elements using getcomputedstyle javascript
def remove_hidden_elements(dom, html):
    elements = dom.find_all()
    for element in elements:
        if get_computed_style(element, 'display', html) == 'none' or get_computed_style(element, 'visibility', html) == 'hidden' or get_computed_style(element, 'opacity', html) == '0' or get_computed_style(element, 'height', html) == '0' or get_computed_style(element, 'width', html) == '0':
            element.extract()
    return dom
    
# return html Document Object Model (DOM)
def get_dom(html):
    return BeautifulSoup(html, 'html.parser')

# remove subtrees of DOM that do not contain text
def remove_empty_nodes(dom):
    for node in dom.find_all(): 
        # if node is not input, html tag and has no text, remove it
        if node.name != 'input' and node.name != 'html' and not node.text:
            node.extract()
    return dom

# remove hidden elements and non textual elements from the DOM
def clean_dom(html):
    dom = remove_hidden_elements(get_dom(html), html)
    dom = remove_empty_nodes(dom)
    return dom.prettify()

# merge content of divs into one div
def merge_divs(html):
    soup = BeautifulSoup(html, 'html.parser')
    for div in soup.find_all('div'):
        if div.text:
            div.unwrap()
    # wrap soup in div tag
    soup = BeautifulSoup('<div>' + soup.prettify() + '</div>', 'html.parser')
    return soup.prettify()
    
# remove style from html file
def remove_style(html):
    return re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)

# clean the html file
def clean_html(html):
    html = remove_comments(html)
    html = remove_header(html)
    html = remove_footer(html)
    html = remove_copyright(html)
    html = remove_iframe(html)
    html = remove_images(html)
    html = remove_script(html)
    html = clean_dom(html)
    html = merge_divs(html)
    html = remove_style(html)
    return html

# find the html files in a nested directory
def find_html_files(directory):
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def clean_html_files(directory):
    for html in find_html_files(directory):
        with open(html, 'r') as f:
            data = f.read()
        data = clean_html(data)
        with open(html, 'w') as f:
            f.write(data)

if __name__ == '__main__':
    clean_html_files('tasks/')
    print('Done')