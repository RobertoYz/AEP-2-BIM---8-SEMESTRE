CREATE TABLE pacientes (
    paciente_id UUID PRIMARY KEY,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL
);

CREATE TABLE profissionais (
    profissional_id UUID PRIMARY KEY,
    crm VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    especialidade VARCHAR(100)
);

CREATE TABLE consultas (
    consulta_id UUID PRIMARY KEY,
    paciente_id UUID REFERENCES pacientes(paciente_id),
    profissional_id UUID REFERENCES profissionais(profissional_id),
    data_hora TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'AGENDADA'
);
