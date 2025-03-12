# EasyPlanning

EasyPlanning é uma aplicação web desenvolvida para facilitar a criação, gerenciamento e resposta de formulários de forma a auxiliar no planejamento do Scrum. Os desenvolvedores respondem aos formulários de cada história criada. A plataforma consegue observar os campos mais selecionados, a média dos valores, etc. Isso permite auxiliar na definição dos valores de cada história criada. O projeto é composto por um frontend desenvolvido em Vue.js e um backend em Django, utilizando Django REST Framework para a criação da API.

## Funcionalidades

- **Criação de Formulários**: Permite a criação de formulários com perguntas de diferentes tipos, como escala linear e múltipla escolha.
- **Gerenciamento de Formulários**: Possibilita a edição e exclusão de formulários existentes.
- **Resposta a Formulários**: Usuários podem responder aos formulários criados.
- **Visualização de Respostas**: Permite visualizar as respostas submetidas para cada formulário, incluindo informações agregadas como média de respostas em perguntas de escala linear e a opção mais escolhida em perguntas de múltipla escolha.

## Estrutura do Projeto

- **Frontend**: Localizado na pasta `frontend`, desenvolvido em Vue.js.
- **Backend**: Localizado na pasta `project_easyretro`, desenvolvido em Django.

## Configuração do Ambiente de Desenvolvimento

### Backend

1. Crie um ambiente virtual:
    ```sh
    python -m venv venv
    ```

2. Ative o ambiente virtual:
    - No Windows:
        ```sh
        venv\Scripts\activate
        ```
    - No Unix ou MacOS:
        ```sh
        source venv/bin/activate
        ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Execute as migrações do banco de dados:
    ```sh
    python manage.py migrate
    ```

5. Inicie o servidor de desenvolvimento:
    ```sh
    python manage.py runserver
    ```

### Frontend

1. Navegue até a pasta [frontend](http://_vscodecontentref_/0):
    ```sh
    cd frontend
    ```

2. Instale as dependências:
    ```sh
    npm install
    ```

3. Inicie o servidor de desenvolvimento:
    ```sh
    npm run serve
    ```

## Uso

1. Acesse o frontend em `http://localhost:8080`.
2. Utilize a interface para criar, gerenciar e responder formulários.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.