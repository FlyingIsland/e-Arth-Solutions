var readlineSync = require('readline-sync');

const fs = require('fs');
const path = require('path');

var path_given = process.argv[2];
function getDirectories(path_got) {
	return fs.readdirSync(path_got).filter(function (file) {
		return fs.statSync(path_got+'/'+file).isDirectory();
	});
}

function filewalker(dir, done) {
		let results = [];

		fs.readdir(dir, function(err, list) {
				if (err) return done(err);

				var pending = list.length;
				if (!pending) return done(null, results);

				list.forEach(function(file){
						file = path.resolve(dir, file);

						fs.stat(file, function(err, stat){
								// If directory, execute a recursive call
								if (stat && stat.isDirectory()) {
										filewalker(file, function(err, res){
												results = results.concat(res);
												if (!--pending) done(null, results);
										});
								} else {
										results.push(file);

										if (!--pending) done(null, results);
								}
						});
				});
		});
};

dir = getDirectories(path_given);
var regex = /^[0-9]{4}[\-|_][0-9]{2}[\-|_][0-9]{2}/;
dir.forEach(
		function(folder){
			folder_matches = regex.test(folder);
			if(folder_matches == true)
			{
				path_scan = path_given + folder + '/';
				filewalker(path_scan, function(err, data)
				{
					if(err){
							throw err;
					}
					if(data.length > 0)
					{
						dir_to_make =  path_given + folder.substring(0,4) + '-'+ folder.substring(5,7)+"/";
						if(!fs.existsSync(dir_to_make))
						{
							fs.mkdirSync(dir_to_make);
						}
						let files_to_process = []
						files_to_process = data;
						console.log("Following are "+files_to_process.length+" files to move to :"+dir_to_make);

						files_to_process.forEach(file_to_process_1 => {
							console.log(file_to_process_1);
						});
						console.log("")
						var Answer = readlineSync.question('Would you like to copy the Files? (yes/no)');
						if(Answer == 'yes')
						{
							files_to_process.forEach(file_to_process_2 => {
								splited_file_to_process = file_to_process_2.split('/');
	            	file_name = splited_file_to_process[splited_file_to_process.length-1];
	            	source_file = file_to_process_2;
	            	destination_file = dir_to_make+file_name;
	            	var file_exists = fs.existsSync(destination_file);
	            	if(file_exists)
	            	{
	            		size_matches = false;
	            		var destination_file_stats = fs.statSync(destination_file);
	            		var destination_file_fileSizeInBytes = destination_file_stats["size"];
	            		var source_file_stats = fs.statSync(source_file);
	            		var source_file_fileSizeInBytes = source_file_stats["size"];
	            		if(destination_file_fileSizeInBytes == source_file_fileSizeInBytes)
	            		{
	            			size_matches = true;
	            		}
	            	}  
	            	if(file_exists && size_matches)
	            	{
	        				console.log('Duplicate File Found. Source file : '+source_file+". Duplicate : "+destination_file);
	          		}
	          		else
	          		{
	          			fs.rename(source_file, destination_file, function (err) {
	          				if (err) throw err
	          			});
	          			console.log('Successfully moved '+source_file+" to "+destination_file);
	          		}
	          	})
						}
						else
						{
							console.log("No Files copied")
						}
						console.log('--------');
					}
					else
					{
						return;
					}
				});

			}
		});
