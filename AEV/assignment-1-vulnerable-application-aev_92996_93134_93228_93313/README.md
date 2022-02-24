# AEV_92996_93134_93228_93313

This work was developed by under the course of analysis and exploration of vulnerabilities:
- Guilherme Pereira  93134
- Jose Costa         92996
- Diogo Amaral       93228
- Daniel Andrade     93313

The application is an online shop application where a user can login and buy products, the administrator of the website (admin@mail.com) can also upload new items to put on sale.

The project structure is as follows:

-app folder contains the vulnerable app, the docker build file and the docker image run file.

-appfix contains the app with fixes to the vulnerabilities implemented, the respective docker file and the docker image run file.

-the analysis folder contains scripts, files, and a detail report that explains everything about the project from how to use the website, to showcase the vulnerabilities exploited and how to fix them

To run the docker containers, on both folders, a build.sh and run.sh script exist.
First the build.sh should be executed, then the run.sh to start the docker container.
This is the same process for both the vulnerable and fixed app.

The vulnerabilities implemented were the following:

- SQL Injection
- XSS cross site scripting
- PHP loose comparison
- Security misconfiguration - apt
- Crontab rsync backup
- Unrestricted upload of file
- Broken access control
- SetUid Personal File   # This vulnerability is extra, but does not fit the context of the project


The base code of the online shop was developed by the user Ghost173 on github and
the code can be found in github.
Link: https://github.com/Ghost173/simple-e-commerce-website-with-php-mysqli

The details of this project are described in the report.pdf, located in the analysis folder.
