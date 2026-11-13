CREATE TABLE usuarios (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    perfil_id INT NOT NULL,
    status VARCHAR(20) NOT NULL
);

CREATE TABLE chamados (
    id UUID PRIMARY KEY,
    solicitante_id UUID REFERENCES usuarios(id),
    status VARCHAR(20) NOT NULL,
    prioridade INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interacoes (
    id UUID PRIMARY KEY,
    chamado_id UUID REFERENCES chamados(id),
    autor_id UUID REFERENCES usuarios(id),
    conteudo TEXT NOT NULL,
    tipo VARCHAR(10) CHECK (tipo IN ('publica', 'interna'))
);
