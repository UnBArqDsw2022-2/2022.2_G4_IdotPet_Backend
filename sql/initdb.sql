DROP DATABASE IF EXISTS db_idotpet;

CREATE DATABASE db_idotpet;

-- Criando domínios

CREATE DOMAIN POSITIVE_INT INTEGER CHECK (VALUE > 0);
CREATE DOMAIN NON_NEGATIVE_INT INTEGER CHECK (VALUE >= 0);

-- Criando as tabelas

CREATE TABLE pet (
  id_pet SERIAL NOT NULL,
  nome_pet TEXT NOT NULL,
  idade_pet NON_NEGATIVE_INT NOT NULL,
  foto_pet BYTEA,
  porte_pet CHAR NOT NULL,
  genero_pet CHAR NOT NULL,
  raca_pet TEXT NOT NULL,
  especie_pet TEXT NOT NULL,
  vacinas_pet TEXT,
  descricao_pet TEXT,

  CHECK (porte_pet IN ('G', 'g', 'M', 'm', 'P', 'p')),
  CHECK (genero_pet IN ('M', 'm', 'F', 'f')),
  PRIMARY KEY (id_pet, nome)
);


CREATE TABLE usuario (
  id_usuario SERIAL NOT NULL,
  cpf TEXT NOT NULL,
  nome TEXT NOT NULL,
  email TEXT NOT NULL,
  dia_n NON_NEGATIVE_INT NOT NULL,
  mes_n NON_NEGATIVE_INT NOT NULL,
  ano_n NON_NEGATIVE_INT NOT NULL,
  telefone TEXT NOT NULL,
  enderecos TEXT NOT NULL, -- Chave primaria da tabela de endereco


  CHECK (dia_n BETWEEN 1 AND 31),
  CHECK (mes_n BETWEEN 1 AND 12),
  CHECK (ano_n < 2004),
  PRIMARY KEY(id_usuario, cpf)
);

CREATE TABLE endereco (
  nome_endereco TEXT PRIMARY KEY,
  cep TEXT NOT NULL,
  logradouro TEXT NOT NULL,
  numero TEXT NOT NULL,
  bairro TEXT NOT NULL,
  cidade TEXT NOT NULL,
  uf TEXT NOT NULL,
  complemento TEXT,
  referencia TEXT,
  
  CHECK (uf IN ('RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO', 'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA', 'MG', 'ES', 'RJ', 'SP', 'PR', 'SC', 'RS', 'MS', 'MT', 'GO', 'DF')),
);

CREATE TABLE mensagem (
  id SERIAL PRIMARY KEY,
  data_mensagem CURRENT_DATE NOT NULL,
  destinatario INTEGER NOT NULL, -- chave estrangeira de usuario
  remetente INTEGER NOT NULL, -- chave estrangeira de usuario
  texto TEXT,

  CHECK (destinatario != remetente)
);

CREATE TABLE anuncio (
  id_anuncio
);