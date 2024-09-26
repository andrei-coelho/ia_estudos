create table if not exists produtos (
    id bigint not null auto_increment,
    urli varchar(255) not null,
    nome varchar(255) not null,
    descricao varchar(255) not null,
    avaliacao decimal(3,2) not null default 0,
    categoria varchar(255),
    primary key(id),
    unique(urli)
) ENGINE=MyISAM DEFAULT CHARACTER SET=utf8;