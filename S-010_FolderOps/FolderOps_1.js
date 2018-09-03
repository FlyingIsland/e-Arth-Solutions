const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

var path_given = process.argv[2];

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

filewalker(path_given, function(err, data){
	if(err){
		throw err;
	}
	path_given_splited_length = path_given.split("/").length;
	let files_to_process = []
	data.forEach(file => {
		file_splited_length = file.split("/").length;
		if(file_splited_length != path_given_splited_length)
		{
			files_to_process.push(file);
		}
	 })
	if(files_to_process.length > 0)
	{
		console.log("Following are "+files_to_process.length+" files to move :")
		files_to_process.forEach(file_to_process => {
			console.log(file_to_process);
		});
		console.log("Would you like to copy the Files? (yes/no)");
		rl.question('', (answer) => {
			if(answer == 'yes')
			{
				file_moved_count = 0;
				duplicate_moved_count = 0;
				files_to_process.forEach(file_to_process => {
					splited_file_to_process = file_to_process.split('/');
					file_name = splited_file_to_process[splited_file_to_process.length-1];
					source_file = file_to_process;
					destination_file = path_given+file_name;
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
						duplicate_moved_count = duplicate_moved_count + 1;
					}
					else
					{
						fs.rename(source_file, destination_file, function (err) {
						if (err) throw err
						})
						console.log('Successfully moved '+source_file+" to "+destination_file);
						file_moved_count = file_moved_count + 1;
					}
					
				});
				console.log('Duplicate '+duplicate_moved_count+' files found.')
				console.log('Successfully moved '+file_moved_count+' files.')
				rl.close();
				process.exit();
			}
			else
			{
				console.log("No files are copied.");
				rl.close();
				process.exit();
			}
		});
	}
	else
	{
		console.log("No files to move");
		process.exit();
	}
});

