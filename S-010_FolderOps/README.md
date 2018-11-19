1. Collapse content files of all sub folders into specified home folder.

Usage :
node FolderOps_1.js /home/ec2-user/e-Arth/S-010_FolderOps/test/

All files of all sub folders in /home/ec2-user/e-Arth/S-010_FolderOps/test/ directory will be copied to /home/ec2-user/e-Arth/S-010_FolderOps/test/
/home/ec2-user/e-Arth/S-010_FolderOps/test/ is the home folder specified as a script argument.

2. Given a home folder that has day wise sub folders of the following types:  YYYY_MM_DD
   YYYY_MM_DD*
   YYYY-MM-DD
   YYYY-MM-DD*
   YYYY[_-]MM[_-]DD.* - Summarized pseudo regular expression
  create a month wise folder YYYY-MM under the some folder if it does not exist and move(not copy) contents of the day wise folders into the month wise folders.

Usage :
node FolderOps_2.js /home/ec2-user/e-Arth/S-010_FolderOps/test/

All files in day wise sub folders will be moved to new folder YYYY-MM.
