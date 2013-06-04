import zipfile, os

def create_mimetype(epub_path, mimetype_filename):
    f = '%s/%s' % (epub_path, 'mimetype')
    f = open(f, 'w')
    # Be careful not to add a newline here
    f.write('application/epub+zip')
    f.close()
	
'''
Create the ZIP archive.  The mimetype must be the first file in the archive 
and it must not be compressed.

Example: http://www.ibm.com/developerworks/xml/tutorials/x-epubtut/section5.html
'''
def create_archive(epub_path, mimetype_filename):
    epub_name = '%s.epub' % os.path.basename(epub_path)

    # Open a new zipfile for writing
    epub = zipfile.ZipFile(epub_name, 'w')

    # Change to the EPUB directory to access the files of the EPUB
    os.chdir(epub_path)
    
    # Write the mimetype file uncompressed
    epub.write(mimetype_filename, compress_type = zipfile.ZIP_STORED)

    # For the remaining paths in the EPUB, add all of their files
    # using normal ZIP compression
    # See http://mayankjohri.wordpress.com/2008/07/02/create-list-of-files-in-a-dir-tree/
    for root, subFolders, files in os.walk('.'):
        for file in files:
            # Don't add mimetype file twice
            if not (mimetype_filename in os.path.join(root, file)):
                print os.path.join('Adding file to %s: ' % epub_name, root, file)
                epub.write(os.path.join(root, file), compress_type = zipfile.ZIP_DEFLATED)
    
    epub.close()

if __name__ == '__main__':
	mimetype_filename = 'mimetype'
	create_mimetype(epub_path = 'accordion', mimetype_filename = mimetype_filename)
	create_archive(epub_path = 'accordion', mimetype_filename = mimetype_filename)
