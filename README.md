### This READ.md template was written based on this [repository](https://github.com/FernandoSchett/github_readme_template).

<h1 align="center">🗄️ Archive manager with replication 🗄️</h1>

<div align="center">
	<a href="link_for_webite">
	<img height = "250em" src = "https://github.com/Danub2002/File-Deposit-App/assets/80331486/e666252d-88da-4fa1-ae94-79f7a5404119" />
    </a>
</div>

## Developed by 💻:
- [Fernando Schettini](https://linktr.ee/fernandoschett).
- [Guilherme Fontes](https://github.com/guichfontes).
- [Danilo Andrade](https://github.com/guichfontes).
- [João Pedro Costa Chaves](https://github.com/jompp).
- [Diego Qualloss](https://github.com/qualloss).

## Special thanks to 🥰:
- [Gustavo Bittencourt Figueiredo](http://buscatextual.cnpq.br/buscatextual/visualizacv.do;jsessionid=717F388996DEE35B7CBDC04F07273B02.buscatextual_0), our professor your experience and knowledge have been invaluable to our progress

## About 🤔:

This is a project developed as part of the Computer Networks I course that requires students to implement a file repository with replication using a client-server model. The application operate in deposit and retrieval modes, with the server storing multiple copies of files in different locations based on client-defined fault tolerance levels. For usage and more info, check out [this demo video](https://youtu.be/2gOGSE18ZCU?si=o19lE_-1cJf89G_y).

## Resourses 🧑‍🔬:

- **File Repository:** The project allows for the storage and retrieval of files through a central server.

- **Replication:** The system supports the replication of files across different locations (devices) to ensure availability and fault tolerance.

- **Operation Modes:** The project offers two operation modes, namely, deposit mode and retrieval mode, so that clients can send files to the server and request file retrieval.

- **Fault Tolerance:** Clients can define the level of fault tolerance, determining the number of replicas stored for each file.

- **Replica Consistency:** The system maintains replica consistency, automatically adjusting the number of replicas based on client requests.

## Dependencies 🚚:

The project dependencies are described in  ```./dependencies/requirements.``` within the repository. In summary, heres what you're gonna need in order to run the project:

- [```python-dotenv```](https://pypi.org/project/python-dotenv/).

For installing dependencies more quickly, you can run the following command at terminal, inside the clonned repository:

	sudo apt update && sudo apt install python3 python3-pip
    pip3 install -r ./dependencies/requirements.txt

Make sure you have all Dependencies before running the project.

## How to run it 🏃:

First, clone this repository. After that, execute the entity's file with the commands:

    sudo python3 ./src/client.py
	sudo python3 ./src/load_balancer.py
	sudo python3 ./src/server.py PORT=<your_port>

## Screens 🎬:

<div align="center">
	<a href="">
	<img height = "250em" src = "https://github.com/Danub2002/archive_manager/assets/80331486/0e9e5ec9-52e2-4d99-a8f4-b02c4aa0fe34" />
    </a>
</div>
<h4 align="center">Figure 1 - Running project image. </h4>


## Logic Model 🧮:

<div align="center">
	<a href="">
	<img height = "250em" src = "https://github.com/Danub2002/archive_manager/assets/80331486/48b680ca-665b-4183-9809-435932db0be1" />
    </a>
</div>
<h4 align="center">Figure 2 - System Logic Model.</h4>

### Tools Used 🛠️: 

- [Visual Studio Code](https://code.visualstudio.com). 

## How to contribute 🫂:

Feel free to create a new branch, fork the project, create a new Issue or make a pull request contact one of us to develop at archive manager.

## Licence 📜:

[Apache V2](https://choosealicense.com/licenses/apache-2.0/)
