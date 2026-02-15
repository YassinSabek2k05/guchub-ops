## GucHub-ops
An automation suite for deploying the GucHub Spring Boot backend.
##### operations performed:
- building the springboot project using maven `mvn clean package` command (the build is done on the local machine)
- after the build is done, the jar is copied to the server using `sftp`
- finally, the service is restarted using `sudo systemctl restart <service-name>`
##### Python libraries used:
- `paramiko`
- `os` 
- `subprocess`
- `dotenv`

##### how the script is run:
```bash
$  ./deploy_backend.sh #then enter the password when prompted 
```
##### Environment variables:
- `DB_USER` -> linux server username
- `HOST` -> linux server ip address
- `SPRINGBOOT_PATH` -> path to the springboot project root
- `FINAL_NAME` -> name of the final jar file (defined in the pom.xml <finalName> tag)
- `REMOTE_PATH`-> target path on the server where the jar file will be copied