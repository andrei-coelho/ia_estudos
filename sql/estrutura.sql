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

create table if not exists clientes (
    id bigint not null auto_increment,
    nome varchar(255) not null,
    sobrenome varchar(255) not null,
    email varchar(255) not null,
    data_nascimento date not null,
    data_criacao date not null,
    genero varchar(100) not null,
    ativo tinyint(1) not null default 1, /* 1 para ativo | 2 para bloqueado */
    primary key(id),
    unique(email)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

create table if not exists produtos_visualizados (
    cliente_id bigint not null,
    produto_id bigint not null,
    visualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foreign key (cliente_id) references clientes(id),
    foreign key (produto_id)  references produtos(id)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

create table if not exists carrinhos (
    id bigint not null auto_increment,
    cliente_id bigint not null,
    status_cart tinyint(1) not null default 0, /* 0 para aberto | 1 para cancelado | 2 para compra finalizada | 3 para produtos entregues */
    foreign key (cliente_id) references clientes(id),
    primary key(id)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;

create table if not exists produtos_carrinho (
    id bigint not null auto_increment,
    produto_id bigint not null,
    carrinho_id bigint not null,
    foreign key (produto_id)  references produtos(id),
    foreign key (carrinho_id) references carrinhos(id),
    primary key(id)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;