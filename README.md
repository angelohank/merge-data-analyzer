# Merge Data Analyzer

### O que é
Ferramenta criada para coletar informações sobre a execução de testes de unidade em pipelines que rodam, até o momento, no CI/CD do GitLab

### O que coleta
A ferramenta busca os merge requests que têm um estado (aberto, mergeado, etc) definidos no arquivo de configuração. <br>
Através dos dados retornados desse MR, pode-se conseguir os dados da pipeline relacionada a ele dentro da plataforma. <br>
Com os dados da pipeline, é possível verificar o resultado da execução dos testes de unidade do projeto alvo. <br>

### Para que serve
Os dados coletados pela ferramenta foram filtrados e estudados para construção de um artigo acadêmico entitulado "Análise de testes de unidade em software de larga escala", que surgiu como trabalho de conclusão de curso para o curso de Bacharel em Engenharia de Software pela Universidade Técnologica Federal do Paraná.

A ideia do artigo foi encontrar padrões de uso e crescimento para um determinado conjunto de testes de unidade, do ponto de vista dos desenvolvedores do projeto e dos times participantes desse projeto, que se dividem entre times de manutenção e melhorias.


### Fluxos

##### Busca dos Merge Requests abertos
![busca_merges](https://github.com/user-attachments/assets/7a237f52-ca23-4b13-9f79-49e95073c160)

##### Busca das pipelines relaacionadas a cada merge
![busca_pipelines](https://github.com/user-attachments/assets/12301177-e3e8-4f03-87f0-944d6ef1fa0c)

##### Busca do relatório de execução dos testes de unidade de cada pipeline
![busca_test_report](https://github.com/user-attachments/assets/3c97fd0e-d9bf-4833-a2bf-1b271ee25596)


### Configurações
#### Requerimentos
- Python 3.10
- private_token da plataforma de código
- url do servidor de hospedagem

#### Arquivos de configuração

- config.json
```
{
  "data": {
      "projectId": "",
      "privateToken": "",
      "apiUrl": "",
      "perPage": ,
      "state": [
          ""
      ],
      "ignoreAuthor": [""],
      "branchesBySquad": [
          {"":  0},
          {"":  1}
      ],
      "logDir": ""
  }
}
```

- config_db.json
```
{
  "database_name": "",
  "user":  "",
  "password": "",
  "host":  "",
  "port": ""
}
```
