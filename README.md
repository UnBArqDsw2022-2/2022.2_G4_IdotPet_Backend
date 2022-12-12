# Backend da aplicação iDotPet


## Configuração Banco de Dados

### Docker

1 - Para instalar o Docker siga o [tutorial oficinal](https://docs.docker.com/engine/install/)

2 - Com o Docker instalado, suba o ambiente de desenvolvimento

```bash
# Na raiz do projeto
$ docker-compose up --build
```

A flag **_--build_** deve ser usada sempre que alguma configuração do ambiente for alterada, como o arquivo _requirements.txt_ por exemplo.

3 - Conectando no postgres via terminal

```bash
# Na raiz do projeto
docker-compose exec db psql -d idotpet -U postgres -W
# Quando solicitado insira 'postgres' sem as aspas
```

### PostgreSQL Local


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

## Pronto! Seu ambiente PostgreSQL está pronto!