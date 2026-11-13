CREATE TABLE clientes (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessoes (
    id UUID PRIMARY KEY,
    cliente_id UUID NOT NULL,
    token_jwt TEXT NOT NULL,
    expiracao TIMESTAMP NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
