#!/usr/bin/python

import fileinput
import sys
import os
import shutil

TOMCAT_HOME = "/opt/tomcat"




def replace_all(file, searchRegex, replaceExp):
  for line in fileinput.input(file, inplace=1):
    if searchRegex in line:
      line = line.replace(searchRegex,replaceExp)  
    sys.stdout.write(line)

  fileinput.close()


def do_setting_tomcat_user(user, password):
  global TOMCAT_HOME

  if(user is None or user == ""):
    raise Exception("You must set the tomcat admin account")
  if(password is None or password == ""):
    raise Exception("You must set the password for admin account")
  
  replace_all(TOMCAT_HOME +"/conf/tomcat-users.xml", "{{TOMCAT_ADMIN_LOGIN}}", user)
  replace_all(TOMCAT_HOME +"/conf/tomcat-users.xml", "{{TOMCAT_ADMIN_PASSWORD}}", password)


def do_setting_javamelody_user(user, password):
  global TOMCAT_HOME

  if(user is not None and password is not None):
    if(user == ""):
      raise Exception("The user for Javamelody can't be an empty string")
    if(password == ""):
      raise Exception("The password for Javamelody can't be an empty string")
    
    javamelody_user = '<user username="'+ user +'" password="'+ password +'" roles="tomcat"/>'

    replace_all(TOMCAT_HOME +"/conf/tomcat-users.xml", "{{TOMCAT_JAVAMELODY_ACCOUNT}}", javamelody_user)

  else:
    replace_all(TOMCAT_HOME +"/conf/tomcat-users.xml", "{{TOMCAT_JAVAMELODY_ACCOUNT}}", "")

def do_setting_javamelody(enable_javamelody, user, password):
  global TOMCAT_HOME


  if(enable_javamelody is "false"):
    replace_all(TOMCAT_HOME +"/conf/web.xml", "{{TOMCAT_JAVAMELODY_ACCESS}}", "")
    os.remove(TOMCAT_HOME +"/lib/javamelody.jar")

  elif(user is not None and password is not None):
    javamelody_access = '''
	<login-config>
   		<auth-method>BASIC</auth-method>
   		<realm-name>Monitoring</realm-name>
	</login-config>
	<security-role>
   		<role-name>monitoring</role-name>
	</security-role>
	<security-constraint>
   	<web-resource-collection>
      		<web-resource-name>Monitoring</web-resource-name>
         	<url-pattern>/monitoring</url-pattern>
      	</web-resource-collection>
      	<auth-constraint>
         	<role-name>monitoring</role-name>
      	</auth-constraint>
      	<!-- if SSL enabled (SSL and certificate must then be configured in the server)
      	<user-data-constraint>
         	<transport-guarantee>CONFIDENTIAL</transport-guarantee>
       	</user-data-constraint> 
       	-->
	</security-constraint>
    '''
    replace_all(TOMCAT_HOME +"/conf/web.xml", "{{TOMCAT_JAVAMELODY_ACCESS}}", javamelody_access)


  else:
    replace_all(TOMCAT_HOME +"/conf/web.xml", "{{TOMCAT_JAVAMELODY_ACCESS}}", "")

def do_setting_session_timeout(timeout):
  global TOMCAT_HOME

  if(timeout is None or timeout == ""):
    raise Exception("You must specify the session timeout")

  replace_all(TOMCAT_HOME +"/conf/web.xml", "{{TOMCAT_SESSION_TIMEOUT}}", timeout)


def do_setting_log_level(log_level):
  global TOMCAT_HOME
  if(log_level is None or log_level == ""):
    raise Exception("You must specify the log level")

  replace_all(TOMCAT_HOME +"/conf/logging.properties", "{{TOMCAT_LOG_LEVEL}}", log_level) 



def do_setting_cluster(cluster_ip, cluster_port):
  global TOMCAT_HOME

  if(cluster_ip is None and cluster_port is None):
    replace_all(TOMCAT_HOME +"/conf/server.xml", "{{TOMCAT_CLUSTER}}", "")

  elif(cluster_ip is not None and cluster_ip != "" and cluster_port is not None and cluster_port != ""):
    cluster = '''
	<Cluster className="org.apache.catalina.ha.tcp.SimpleTcpCluster"
                 channelSendOptions="8">

          		<Manager className="org.apache.catalina.ha.session.DeltaManager"
                   	expireSessionsOnShutdown="false"
                   	notifyListenersOnReplication="true"/>

          		<Channel className="org.apache.catalina.tribes.group.GroupChannel">
            			<Membership className="org.apache.catalina.tribes.membership.McastService"
                        	address="'''+ cluster_ip +'''"
                        	port="'''+ cluster_port +'''"
                        	frequency="500"
				domain="app"
                        	dropTime="3000"/>
            			<Receiver className="org.apache.catalina.tribes.transport.nio.NioReceiver"
                      		address="auto"
                      		port="4000"
                      		autoBind="100"
                      		selectorTimeout="5000"
                      		maxThreads="6"/>

            			<Sender className="org.apache.catalina.tribes.transport.ReplicationTransmitter">
              				<Transport className="org.apache.catalina.tribes.transport.nio.PooledParallelSender"/>
            			</Sender>
            			<Interceptor className="org.apache.catalina.tribes.group.interceptors.TcpFailureDetector"/>
            			<Interceptor className="org.apache.catalina.tribes.group.interceptors.MessageDispatch15Interceptor"/>
         		 </Channel>

          		<Valve className="org.apache.catalina.ha.tcp.ReplicationValve"
                 		filter=""/>
          		<Valve className="org.apache.catalina.ha.session.JvmRouteBinderValve"/>

          		<Deployer className="org.apache.catalina.ha.deploy.FarmWarDeployer"
                    		tempDir="/tmp/war-temp/"
                    		deployDir="/tmp/war-deploy/"
                    		watchDir="/tmp/war-listen/"
                    		watchEnabled="false"/>

          		<ClusterListener className="org.apache.catalina.ha.session.JvmRouteSessionIDBinderListener"/>
          		<ClusterListener className="org.apache.catalina.ha.session.ClusterSessionListener"/>
       </Cluster>

    '''

    replace_all(TOMCAT_HOME +"/conf/server.xml", "{{TOMCAT_CLUSTER}}", cluster)

  else:
    raise Exception("If you should set the current tomcat as a cluster, you must specify the cluster IP and the cluster port")
  

