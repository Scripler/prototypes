var fs = require('fs');
var filewalker = require('filewalker');
var archiver = require('archiver');

var output = fs.createWriteStream('book.epub');

var archive = archiver('zip', {zlib: {level: 9}});

archive.on('error', function(err) {
  throw err;
});

filewalker('resources')
  .on('file', function(p) {
    console.log('dir:  %s', p);
	//Add all files to the zip file. Compress all files, except mimetype.
	archive.append(fs.createReadStream('./resources/'+p), { name: p, store: (p=='mimetype') });
  })
  .on('error', function(err) {
    console.error(err);
  })
  .on('done', function() {
    console.log('Found: %d dirs, %d files, %d bytes', this.dirs, this.files, this.bytes);
	archive.finalize(function(err, bytes) {
	  if (err) {
		throw err;
	  }
	  console.log('Done. Compressed to ' + bytes + ' bytes');
	});
  })
.walk();

archive.pipe(output);

output.on('close', function() {
  console.log('Archiver has been finalized and the output file descriptor has closed.');
});

