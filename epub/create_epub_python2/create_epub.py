import sys
import zipfile
import os
import shutil

def create_mimetype(epub_name, res_dir_name, mimetype_filename):
    mimetype_filename_src = res_dir_name + '/' + mimetype_filename
    mimetype_filename_dst = epub_name + '/' + mimetype_filename    
    shutil.copy(mimetype_filename_src, mimetype_filename_dst)
    
def create_meta_inf(epub_name, res_dir_name):
    dir_name = 'META-INF'
    shutil.copytree(res_dir_name + '/' + dir_name, epub_name + '/' + dir_name, symlinks = False, ignore = shutil.ignore_patterns('desktop.ini'))
    
def create_oebps(epub_name, res_dir_name, title, text, creator):
    oepbs_dir_name = 'OEBPS'
    oepbs_dir_name_src = res_dir_name + '/' + oepbs_dir_name
    oepbs_dir_name_dst = epub_name + '/' + oepbs_dir_name
    
    if not os.path.exists(oepbs_dir_name_dst):
        os.makedirs(oepbs_dir_name_dst)
    
    # Images
    image_dir_name = 'images'
    shutil.copytree(oepbs_dir_name_src + '/' + image_dir_name, oepbs_dir_name_dst + '/' + image_dir_name, symlinks = False, ignore = shutil.ignore_patterns('desktop.ini'))
    
    # Process eacn of the following files as follows:
    #   1 Read file from resources dir into string variable
    #   2 Replace variables with values and save result
    #   3 Write result to file in EPUB dir
    
    # Title (HTML)
    title_filename = 'title.html'
    title_filename_src = oepbs_dir_name_src + '/' + title_filename
    title_filename_dst = oepbs_dir_name_dst + '/' + title_filename
    with open(title_filename_src, "r") as title_file_src:
        title_data = title_file_src.read().replace('$title', title)
    title_file_dst = open(title_filename_dst, 'w')
    title_file_dst.write(title_data)        
    
    # Content (HTML)
    content_filename_html = 'content.html'
    content_filename_html_src = oepbs_dir_name_src + '/' + content_filename_html
    content_filename_html_dst = oepbs_dir_name_dst + '/' + content_filename_html
    with open(content_filename_html_src, "r") as content_file_html_src:
        content_data = content_file_html_src.read().replace('$title', title).replace('$text', text)
    content_file_html_dst = open(content_filename_html_dst, 'w')
    content_file_html_dst.write(content_data)  

    # Stylesheet (CSS)
    stylesheet_filename = 'stylesheet.css'
    stylesheet_filename_src = oepbs_dir_name_src + '/' + stylesheet_filename
    stylesheet_filename_dst = oepbs_dir_name_dst + '/' + stylesheet_filename
    shutil.copy(stylesheet_filename_src, stylesheet_filename_dst)
    
    uuid = 'urn:uuid:0cc33c11-aaa2-49d1-906a-52ae16bc2658'
    
    # Content (OPF)
    content_filename_opf = 'content.opf'
    content_filename_opf_src = oepbs_dir_name_src + '/' + content_filename_opf
    content_filename_opf_dst = oepbs_dir_name_dst + '/' + content_filename_opf
    with open(content_filename_opf_src, "r") as content_file_opf_src:
        content_data = content_file_opf_src.read().replace('$title_filename', title_filename).replace('$content_filename_html', content_filename_html).replace('$image_dir_name', image_dir_name).replace('$title', title).replace('$creator', creator).replace('$uuid', uuid).replace('$stylesheet_filename', stylesheet_filename)
    content_file_opf_dst = open(content_filename_opf_dst, 'w')
    content_file_opf_dst.write(content_data)  
    
    # TOC (NCX)
    toc_filename = 'toc.ncx'
    toc_filename_src = oepbs_dir_name_src + '/' + toc_filename
    toc_filename_dst = oepbs_dir_name_dst + '/' + toc_filename
    with open(toc_filename_src, "r") as toc_file_src:
        toc_data = toc_file_src.read().replace('$title_filename', title_filename).replace('$title', title).replace('$uuid', uuid).replace('$content_filename_html', content_filename_html)
    toc_file_dst = open(toc_filename_dst, 'w')
    toc_file_dst.write(toc_data)        
	
def create_archive(epub_name, mimetype_filename):
    epub_filename = '%s.epub' % os.path.basename(epub_name)

    # Open a new zipfile for writing
    epub = zipfile.ZipFile(epub_filename, 'w')

    # Change to the EPUB directory to access the files of the EPUB
    os.chdir(epub_name)
    
    # Write the mimetype file uncompressed
    epub.write(mimetype_filename, compress_type = zipfile.ZIP_STORED)

    # For the remaining paths in the EPUB, add all of their files
    # using normal ZIP compression
    # See http://mayankjohri.wordpress.com/2008/07/02/create-list-of-files-in-a-dir-tree/
    for root, subFolders, files in os.walk('.'):
        for file in files:
            # Don't add mimetype file twice
            if not (mimetype_filename in os.path.join(root, file)):
                print os.path.join('Adding file to %s: ' % epub_filename, root, file)
                epub.write(os.path.join(root, file), compress_type = zipfile.ZIP_DEFLATED)
    
    epub.close()

if __name__ == '__main__':

    if len(sys.argv) < 2:
       sys.exit("An EPUB name (without .EPUB) must be specified.")

    epub_name = sys.argv[1]
    
    #1 Create EPUB directory
    if not os.path.exists(epub_name):
        os.makedirs(epub_name)
    
    res_dir_name = 'resources'

    #2 Create mimetype file
    mimetype_filename = 'mimetype'
    create_mimetype(epub_name = epub_name, res_dir_name = res_dir_name, mimetype_filename = mimetype_filename)
    
    #3 Create META-INF
    create_meta_inf(epub_name = epub_name, res_dir_name = res_dir_name)
    
    #4 Create OEBPS
    create_oebps(epub_name = epub_name, res_dir_name = res_dir_name, title = 'Anden og pythonen', text = 'Der var engang en and.<br/>Andens bedste ven var en Python.', creator = 'Morten Franck')
    
    #5 Create EPUB archive
    create_archive(epub_name = epub_name, mimetype_filename = mimetype_filename)
