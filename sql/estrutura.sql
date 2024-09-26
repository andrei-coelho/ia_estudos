create table if not exists produtos (
    id bigint(255) not null auto_increment,
    nome varchar(255) not null,
    descricao varchar(255) not null,
    avaliacao decimal(3,2) not null default(0),
    categoria varchar(255),
    primary key(id)
) ENGINE=MyISAM DEFAULT CHARACTER SET=utf8;