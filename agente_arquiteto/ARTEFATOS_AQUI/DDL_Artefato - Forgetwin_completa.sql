CREATE TABLE maquina_ativo (
    id SERIAL PRIMARY KEY,
    codigo_tag VARCHAR(50) UNIQUE NOT NULL,
    criticidade CHAR(1) CHECK (criticidade IN ('A', 'B', 'C')),
    status_operacional VARCHAR(20)
);

CREATE TABLE leitura_telemetria (
    id BIGSERIAL PRIMARY KEY,
    sensor_id INT NOT NULL,
    valor_medido NUMERIC(12,4),
    timestamp_leitura TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sensor FOREIGN KEY (sensor_id) REFERENCES sensor_iot(id)
);

CREATE TABLE ordem_servico (
    id SERIAL PRIMARY KEY,
    numero_os VARCHAR(20) UNIQUE NOT NULL,
    maquina_id INT NOT NULL,
    status_os VARCHAR(20),
    CONSTRAINT fk_maquina FOREIGN KEY (maquina_id) REFERENCES maquina_ativo(id)
);
