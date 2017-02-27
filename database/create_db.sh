docker run -d -it --name Oracle12cDB --hostname osbdb -p 1521:1521 -p 5500:5500 -e ORACLE_SID=ORCL -e ORACLE_PDB=OSB -v /opt/oracle/oradata/OracleDB oracle/database:12.1.0.2-ee
