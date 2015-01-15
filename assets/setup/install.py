
#!/usr/bin/python

import subprocess
import os
import shutil

TOMCAT_VERSION = "8.0.15"
TOMCAT_HOME = "/opt/tomcat"
APP_SETUP = "/app/setup"

JAVAMELODY_VERSION = "1.54.0"

POSTGRESQL_VERSION = "9.3-1102"
MYSQL_VERSION = "5.1.34"

def install_tomcat():
  global TOMCAT_VERSION
  global TOMCAT_HOME
  global APP_SETUP

  # First, we get the tomcat archive
  os.chdir("/usr/src")
  return_code = subprocess.call("curl -L -O http://mirrors.ircam.fr/pub/apache/tomcat/tomcat-8/v"+ TOMCAT_VERSION +"/bin/apache-tomcat-"+ TOMCAT_VERSION +".tar.gz", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to download tomcat archive")

  # Next, we untar the archive
  return_code = subprocess.call("tar -xvzf apache-tomcat-"+ TOMCAT_VERSION +".tar.gz", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to untar the tomcat archive")

  # Then, we move the tomcat on target directory
  os.system("mkdir "+TOMCAT_HOME);
  return_code = subprocess.call("mv apache-tomcat-"+ TOMCAT_VERSION +"/* "+TOMCAT_HOME+ "/", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to move tomcat on target directory")

  # Then, we create group and account for tomcat process
  return_code = subprocess.call("groupadd tomcat", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to create tomcat group")

  return_code = subprocess.call("useradd --system --home "+ TOMCAT_HOME +" -g tomcat tomcat", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to create tomcat account")

  # To finish, we set the good right
  return_code = subprocess.call("chown -R tomcat:tomcat "+ TOMCAT_HOME, shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to change the owner of tomcat directory")

  shutil.rmtree("apache-tomcat-"+ TOMCAT_VERSION)

def install_javamelody():
  global TOMCAT_HOME
  global JAVAMELODY_VERSION  


  # First we get Javamelody
  os.chdir("/usr/src")
  return_code = subprocess.call("curl -OL https://github.com/javamelody/javamelody/releases/download/"+ JAVAMELODY_VERSION +"/javamelody-"+ JAVAMELODY_VERSION +".zip", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to download Javamelody archive")

  # We unzip Javamelody
  os.system("mkdir javamelody-"+ JAVAMELODY_VERSION)
  return_code = subprocess.call("unzip javamelody-"+ JAVAMELODY_VERSION  +".zip -d javamelody-"+ JAVAMELODY_VERSION, shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to unzip the Javamelody archive")

  # We install Javamelody on Tomcat
  shutil.copy("javamelody-"+ JAVAMELODY_VERSION +"/javamelody.jar", TOMCAT_HOME +"/lib/")
  return_code = subprocess.call("cp javamelody-"+ JAVAMELODY_VERSION +"/jrobin-*.jar "+ TOMCAT_HOME +"/lib/", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to copy jrobin on Tomcat folder")
  shutil.rmtree("javamelody-"+ JAVAMELODY_VERSION)

def install_postgresql_driver():
  global POSTGRESQL_VERSION
  global TOMCAT_HOME

  # First we get postgresql driver
  os.chdir("/usr/src")
  return_code = subprocess.call("curl -OL http://jdbc.postgresql.org/download/postgresql-"+ POSTGRESQL_VERSION +".jdbc41.jar", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to download PostgreSQL driver")

  # Then we move driver on tomcat folder
  return_code = subprocess.call("mv postgresql-*.jar "+ TOMCAT_HOME +"/lib/", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to move PostgreSQL driver on Tomcat lib")

def install_mysql_driver():
  global MYSQL_VERSION
  global TOMCAT_HOME

  # First we get postgresql driver
  os.chdir("/usr/src")
  return_code = subprocess.call("curl -OL http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-"+ MYSQL_VERSION +".tar.gz", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to download MySQL driver")

  # Then we untar driver
  return_code = subprocess.call("tar -xvzf mysql-connector-java-*.tar.gz", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to untar MySQL driver")

  # Then we move driver on tomcat folder
  return_code = subprocess.call("mv mysql-connector-java-"+ MYSQL_VERSION  +"/*.jar "+ TOMCAT_HOME +"/lib/", shell=True)
  if return_code != 0 :
    raise Exception("Problem when try to move MySQL driver on Tomcat lib")


def install_custom_file():
  global TOMCAT_HOME
  global APP_SETUP

  shutil.copy(APP_SETUP +"/config/tomcat-users.xml", TOMCAT/HOME +"/conf/")
  shutil.copy(APP_SETUP +"/config/tomcat-users.xml", TOMCAT/HOME +"/conf/")
  shutil.copy(APP_SETUP +"/config/web.xml", TOMCAT/HOME +"/conf/")
  shutil.copy(APP_SETUP +"/config/server.xml", TOMCAT/HOME +"/conf/")
  shutil.copy(APP_SETUP +"/config/logging.properties", TOMCAT/HOME +"/conf/")


#install_tomcat()
#install_javamelody()
#install_postgresql_driver()
install_mysql_driver()

