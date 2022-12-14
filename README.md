# Backend da aplicação iDotPet


## Configuração do Ambiente

### Docker

1 - **Para instalar o Docker siga o [tutorial oficinal](https://docs.docker.com/engine/install/)**

2 - **Com o Docker instalado, suba o ambiente de desenvolvimento**

```bash
docker-compose up --build
```

A flag **_--build_** deve ser usada sempre que alguma configuração do ambiente for alterada, como o arquivo _requirements.txt_ por exemplo.

3 - **Execute as migrations para atualizar o banco de dados**

```bash
docker-compose exec app sh -c "PYTHONPATH=/app/src alembic upgrade head"
```

4 - **Conectando no postgres via terminal**

Quando a senha for solicitada, insira 'postgres' sem as aspas.

```bash
docker-compose exec db psql -d idotpet -U postgres -W
```

**Parabéns** você configurou seu ambiente de desenvolvimento!!

### Local

#### PostgreSQL

1 - **Instalar o banco de gerenciador de banco de dados PostgreSQL**

No _Linux_:

```bash
$ sudo apt install postgresql-12
```

Outros sistemas operacionais:

[Documentação de download do PostgreSQL](https://www.postgresql.org/download/)

O próximo passo é alterar a senha do usuário padrão do postgres, para poder logar.

2 - **Alterar senha do usuário padrão do postgres**

Logue como root no seu terminal e, em seguida, altere a senha:

```bash
$ su - root
$ passwd postgres
```

3 - **Logar no usuário do postgres**

```bash
$ su - postgres
# Inserir senha do item anterior
```

4 - **Importar o script de criação do banco**

No usuário do postgres execute

```bash
$ psql
```

para entrar no postgresql. 

Digite

```bash
$ \i <caminho_ate_este_respositório>/2022.2_G4_IdotPet_Backend/sql/initdb.sql
```
alterando a flag **_<caminho_ate_este_respositório>_** para sua árvore de arquivos. O comando ```\i``` é usado para realizar o import do script SQL para sua database.

Pronto! Seu ambiente PostgreSQL está pronto!

#### Aplicação

Caso esteja no _Windows_ substitua `python3` por `python` nos comandos abaixo

1 - **Crie um ambiente virtual para as dependências**

```bash
python3 -m venv venv
```

2 - **Ative o ambiente virtual**

_Windows_:

```ps1
.\venv\Scripts\Activate.ps1
```

_Linux_:

```bash
source ./venv/bin/activate
```

3 - **Instale as dependências do projeto**

Primeiro, atualize a versão do pip. Geralmente ela não vem na ultima versão ao criar um novo ambiente virtual.

```bash
pip3 install -U pip
```

Com o pip atualizado, instale as dependências.

```bash
pip3 install -r requirements.txt
```

4 - **Execute as migrations para atualizar o banco de dados**

Para esta etapa é importante que o seu PostgreSQL já tenha sido configurado e esteja em execução.

_Windows_:

```ps1
$Env:PYTHONPATH='.\src\'
alembic upgrade head
```

_Linux_:

```bash
PYTHONPATH=/app/src alembic upgrade head
```

5 - **Execute a aplicação**

```bash
python3 src/main.py
```

**Parabéns** você configurou seu ambiente de desenvolvimento!!
