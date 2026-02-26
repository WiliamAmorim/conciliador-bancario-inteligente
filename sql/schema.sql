CREATE TABLE execucoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_execucao DATETIME NOT NULL,
    tolerancia_centavos DECIMAL(10,2),
    tolerancia_dias INT,
    similaridade_minima DECIMAL(5,2)
);

CREATE TABLE transacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    execucao_id INT NOT NULL,
    data_movimento DATE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(15,2) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    categoria VARCHAR(100),
    origem VARCHAR(20) NOT NULL,
    conciliado BOOLEAN DEFAULT 0,
    FOREIGN KEY (execucao_id) REFERENCES execucoes(id)
);
CREATE INDEX idx_execucao ON transacoes(execucao_id);
CREATE INDEX idx_execucao_conciliado ON transacoes(execucao_id, conciliado);

CREATE TABLE conciliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    execucao_id INT NOT NULL,
    lancamento_banco_id INT NOT NULL,
    lancamento_controle_id INT NOT NULL,
    diferenca_valor DECIMAL(15,2),
    diferenca_dias INT,
    similaridade DECIMAL(5,2),
    status VARCHAR(20),
    FOREIGN KEY (execucao_id) REFERENCES execucoes(id),
    FOREIGN KEY (lancamento_banco_id) REFERENCES transacoes(id),
    FOREIGN KEY (lancamento_controle_id) REFERENCES transacoes(id)
);
CREATE INDEX idx_conc_execucao ON conciliacoes(execucao_id);