## Setup do Airflow

A primeira coisa é criar uma pasta e entrar nela (ou clonar este repositório):

    mkdir etl-156-airflow
    cd etl-156-airflow

Vamos usar o Python 3, e é recomendável criar um ambiente virtual dentro desta pasta para que esse Python 3 fique isolado do resto do seu sistema operacional. Para isso, vamos usar o `virtualenv`:

    # esse comando abaixo cria um ambiente virtual com Python 3, chamado "python-env"
    virtualenv -p python3 python-env

E então, vamos ativar esse ambiente:

    source python-env/bin/activate

Agora, podemos instalar o Airflow (instruções para Linux):

    # instalando dependências
    sudo apt-get update
    sudo apt-get install build-essential

    # instalando o Airflow
    pip install apache-airflow

O Airflow procura por uma pasta onde ele irá instalar seus arquivos de configuração. Por padrão, ele irá tentar usar `~/airflow`, na raiz das pastas do seu usuário. Isso funciona, porém significa que você terá uma pasta de configuração do Airflow para todos seus projetos.

Para ter uma configuração específica do Airflow para este projeto, recomendamos que você defina essa configuração manualmente:

    # defina sua pasta atual como a "casa" do Airflow neste projeto
    export AIRFLOW_HOME=$(pwd)

Da primeira vez que você utilizar o Airflow, você terá que rodar esse comando (só da primeira vez!):

    airflow initdb

Veja que o Airflow vai criar uma série de arquivos de configuração na pasta atual. Veja o arquivo `airflow.cfg` para mais detalhes.

Agora, para rodar o Airflow, ligue o servidor:

    source python-env/bin/activate
    export AIRFLOW_HOME=$(pwd)
    airflow webserver -p 8080

E em uma outra janela, ligue o "scheduler":

    source python-env/bin/activate
    export AIRFLOW_HOME=$(pwd)
    airflow scheduler

No seu browser, navegue para [http://localhost:8080/](http://localhost:8080/) e pronto!
