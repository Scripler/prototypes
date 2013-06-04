import sys
import zipfile
import os
import shutil
import logging

class EpubCreator:

    def __create_mimetype(self, epub_src_dir, res_dir_name, mimetype_filename):
        mimetype_filename_src = res_dir_name + '/' + mimetype_filename
        mimetype_filename_dst = epub_src_dir + '/' + mimetype_filename    
        #logging.debug("relpath: " + os.path.relpath(mimetype_filename_src))
        shutil.copy(mimetype_filename_src, mimetype_filename_dst)
        
    def __create_meta_inf(self, epub_src_dir, res_dir_name):
        dir_name = 'META-INF'
        shutil.copytree(res_dir_name + '/' + dir_name, epub_src_dir + '/' + dir_name, symlinks = False, ignore = shutil.ignore_patterns('desktop.ini'))
        
    def __create_oebps(self, epub_src_dir, res_dir_name, title, text, creator):
        oepbs_dir_name = 'OEBPS'
        oepbs_dir_name_src = res_dir_name + '/' + oepbs_dir_name
        oepbs_dir_name_dst = epub_src_dir + '/' + oepbs_dir_name
        
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
        
    def __create_archive(self, base_dir, epub_src_dir, title, mimetype_filename):
        zipped_dir = base_dir + '/' + 'epubs/zipped'
        epub_dst = zipped_dir + '/' + title
        epub_filename = epub_dst + '.epub'

        # Open a new zipfile for writing
        epub = zipfile.ZipFile(epub_filename, 'w')

        # Change to the EPUB directory to access the files of the EPUB
        os.chdir(epub_src_dir)
        
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

    def create_epub(self, title, text, creator):    
        #logging.debug('EpubCreator.create_epub(): ' + os.path.dirname(os.path.abspath(__file__)))
    
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
        unzipped_dir = base_dir + '/' + 'epubs/unzipped'
        epub_src_dir = unzipped_dir + '/' + title
        
        #1 Create EPUB directory
        if not os.path.exists(epub_src_dir):
            os.makedirs(epub_src_dir)
        
        res_dir_name = base_dir + '/resources'

        #2 Create mimetype file
        mimetype_filename = 'mimetype'
        self.__create_mimetype(epub_src_dir = epub_src_dir, res_dir_name = res_dir_name, mimetype_filename = mimetype_filename)
        
        #3 Create META-INF
        self.__create_meta_inf(epub_src_dir = epub_src_dir, res_dir_name = res_dir_name)
        
        #4 Create OEBPS
        self.__create_oebps(epub_src_dir = epub_src_dir, res_dir_name = res_dir_name, title = title, text = text, creator = creator)
        
        #5 Create EPUB archive
        self.__create_archive(base_dir = base_dir, epub_src_dir = epub_src_dir, title = title, mimetype_filename = mimetype_filename)
