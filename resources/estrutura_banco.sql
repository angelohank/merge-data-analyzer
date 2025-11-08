alter table pipelines drop column if exists iid;
alter table pipelines add column iid INTEGER;

alter table pipelines drop column if exists status;
alter table pipelines add column status VARCHAR(10);

alter table pipelines drop column if exists link;
alter table pipelines add column link VARCHAR(200);

alter table pipelines drop column if exists fgdadoscoletados;
alter table pipelines add column fgdadoscoletados VARCHAR(1) default 'F';

alter table merges drop column if exists size_conjunto_atual;
alter table pipelines add column size_conjunto_atual INTEGER;

ALTER TABLE teste_unidade_falha drop column if exists id_teste_unidade_falha;
ALTER table teste_unidade_falha ADD COLUMN id_teste_unidade_falha SERIAL;

ALTER TABLE teste_unidade_falha drop column if exists desc_teste;
ALTER table teste_unidade_falha ADD COLUMN desc_teste VARCHAR(300);
