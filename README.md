
# Backend Web com FastAPI para Gestão de Campeonato Esportivo

**Python + API Rápida**

## Descrição
Este projeto backend realiza a gestão de um campeonato esportivo, onde os times competem em várias partidas e acumulam pontos de acordo com os resultados dos jogos. O sistema permite a criação de times, registro de partidas, controle de pontuação e consulta dos resultados do campeonato. As regras de pontuação seguem um modelo simples onde cada vitória concede 3 pontos, empate 1 ponto e derrota 0 pontos.

Além disso, o sistema oferece a funcionalidade de listar os times, partidas, e consultar a tabela de classificação.

## Regras de Negócio
- Cada time possui um nome único e uma cidade de origem.
- Cada partida tem um código único de identificação, a data da partida, os times envolvidos e o resultado.
- A tabela de classificação é atualizada automaticamente após cada partida, levando em conta os pontos conquistados pelos times.
- O campeonato só pode ser encerrado após todas as partidas serem realizadas.

## Como Criar o Projeto na Sua Máquina?

Abra o terminal e digite:

```bash
mkdir campeonato_project
cd campeonato_project
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv
```

Para Windows:

```bash
venv\Scripts\activate
```

Para Linux/macOS:

```bash
source venv/bin/activate
```

Instale o framework FastAPI e o servidor Uvicorn:

```bash
pip install fastapi uvicorn
```

Abra o Visual Studio Code:

```bash
code .
```

Crie um arquivo `main.py` e escreva o código conforme abaixo. Depois, execute o servidor com:

```bash
uvicorn main:app --reload
```

Ou, se preferir, faça o git clone deste projeto:

```bash
git clone git@github.com:SeuUsuario/campeonato_project.git
```

## Estrutura do Projeto

O projeto estará dividido em três principais entidades: **Times**, **Jogos** e **Classificação**.

### Criando o arquivo `main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelos
class Time(BaseModel):
    id: int
    nome: str
    cidade: str

class Jogo(BaseModel):
    id: int
    time1_id: int
    time2_id: int
    gols_time1: int
    gols_time2: int
    data: str

class Classificacao(BaseModel):
    time: str
    pontos: int

# Dados em memória
times_db = []
jogos_db = []
classificacao_db = []

# Endpoints
@app.post("/times/")
def cadastrar_time(time: Time):
    times_db.append(time)
    return {"message": "Time cadastrado com sucesso!"}

@app.get("/times/", response_model=List[Time])
def listar_times():
    return times_db

@app.post("/jogos/")
def registrar_jogo(jogo: Jogo):
    jogos_db.append(jogo)
    # Atualizar classificação
    atualizar_classificacao(jogo)
    return {"message": "Jogo registrado com sucesso!"}

@app.get("/jogos/", response_model=List[Jogo])
def listar_jogos():
    return jogos_db

@app.get("/classificacao/", response_model=List[Classificacao])
def tabela_classificacao():
    return sorted(classificacao_db, key=lambda x: x.pontos, reverse=True)

# Função para atualizar a classificação após cada jogo
def atualizar_classificacao(jogo: Jogo):
    # Verificar e atualizar os times na classificação
    time1 = next((t for t in times_db if t.id == jogo.time1_id), None)
    time2 = next((t for t in times_db if t.id == jogo.time2_id), None)
    
    if time1 and time2:
        # Verificar o resultado do jogo
        if jogo.gols_time1 > jogo.gols_time2:
            pontos_time1 = 3
            pontos_time2 = 0
        elif jogo.gols_time1 < jogo.gols_time2:
            pontos_time1 = 0
            pontos_time2 = 3
        else:
            pontos_time1 = 1
            pontos_time2 = 1
        
        # Atualizar classificação dos times
        atualizar_time_classificacao(time1.nome, pontos_time1)
        atualizar_time_classificacao(time2.nome, pontos_time2)

# Função para atualizar ou adicionar um time na classificação
def atualizar_time_classificacao(nome_time: str, pontos: int):
    time_classificacao = next((c for c in classificacao_db if c.time == nome_time), None)
    
    if time_classificacao:
        time_classificacao.pontos += pontos
    else:
        classificacao_db.append(Classificacao(time=nome_time, pontos=pontos))

```

### Como Funciona:
- **Cadastro de Times**: A rota `POST /times/` permite cadastrar times com um nome e cidade de origem.
- **Registro de Jogos**: A rota `POST /jogos/` permite registrar partidas entre dois times, informando o número de gols de cada time e a data da partida.
- **Classificação**: A rota `GET /classificacao/` retorna a classificação dos times com base nos pontos acumulados.
- **Listagem de Times e Jogos**: A rota `GET /times/` lista todos os times cadastrados e `GET /jogos/` lista todos os jogos registrados.

