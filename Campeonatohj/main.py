from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Dados dos times
times = {
    1: {"id": 1, "nome": "Barcelona HJ"},
    2: {"id": 2, "nome": "São José"},
    3: {"id": 3, "nome": "ADS"},
    4: {"id": 4, "nome": "Flamengo"},
    5: {"id": 5, "nome": "União"}
}

# Dados das partidas entre os times
partidas = {
    1: {
        "id": 1,
        "time_1": "Barcelona",
        "time_2": "São José",
        "data": "2024-11-26",
        "resultado": "Barcelona 3 x 2 São José",
"gols": [
    {"jogador": "Guilherme", "time": "Barcelona"},
    {"jogador": "Guilherme", "time": "Barcelona"},
    {"jogador": "Gustavo ", "time": "Barcelona"},
    {"jogador": "Rodrigo", "time": "São José"},
    {"jogador": "Rodrigo", "time": "São José"}
]

    },
    2: {
        "id": 2,
        "time_1": "ADS",
        "time_2": "Flamengo",
        "data": "2024-11-18",
        "resultado": "ADS 2 x 0 Flamengo",
        "gols": [
            {"jogador": "Vini ", "time": "ADS"},
            {"jogador": "Michel Jr.", "time": "ADS"}
        ]
    }
}

# Dados dos jogadores
jogadores = {
    1: {"id": 1, "nome": "Guilherme", "posicao": "Atacante", "time": "Barcelona", "gols": 10},
    2: {"id": 2, "nome": "João ", "posicao": "Atacante", "time": "Barcelona", "gols": 12},
    3: {"id": 3, "nome": "Vini", "posicao": "Atacante", "time": "ADS", "gols": 7},
    4: {"id": 4, "nome": " Paiva", "posicao": "Meio-campo", "time": "ADS", "gols": 5},
    5: {"id": 5, "nome": "Michel ", "posicao": "Defensor", "time": "ADS", "gols": 2},
    6: {"id": 6, "nome": "Pedro ", "posicao": "Atacante", "time": "Flamengo", "gols": 8},
    7: {"id": 7, "nome": "Pablo", "posicao": "Atacante", "time": "Flamengo", "gols": 6},
    8: {"id": 8, "nome": "Gil", "posicao": "Meio-campo", "time": "Flamengo", "gols": 4},
    9: {"id": 9, "nome": "Rodrigo", "posicao": "Meio-campo", "time": "São José", "gols": 7},
    10: {"id": 10, "nome": "Gustavo", "posicao": "Defensor", "time": "São José", "gols": 3},
    11: {"id": 11, "nome": "Rogilson", "posicao": "Meio-campo", "time": "União", "gols": 4},
    12: {"id": 12, "nome": "Gabriel", "posicao": "Atacante", "time": "União", "gols": 5}
}

class Time(BaseModel):
    nome: str

class Partida(BaseModel):
    time_1: str
    time_2: str
    data: str
    resultado: str = None

class PartidaUpdate(BaseModel):
    time_1: str
    time_2: str
    data: str
    resultado: str


class GolsInput(BaseModel):
    jogador_id: int
    quantidade_gols: int

contador_jogadores = max(jogadores.keys())  # Último ID usado nos jogadores

# Classe base (model) para representar um jogador
class Jogador(BaseModel):
    nome: str
    posicao: str
    time: str
    gols: int = 0

# Rota raiz
@app.get("/", tags=["Raiz"])
def home():
    return {"mensagem": "Bem-vindo ao Campeonato de inverno HJ"}


# Rotas para Times
@app.get("/times/", tags=["Times"])
def listar_times():
    return {"times": list(times.values())}


@app.get("/times/{time_id}", tags=["Times"])
def buscar_time(time_id: int):
    time = times.get(time_id)
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado.")
    return time


@app.post("/times/", tags=["Times"])
def adicionar_time(time: Time):
    novo_id = max(times.keys(), default=0) + 1
    time_data = {"id": novo_id, "nome": time.nome}
    times[novo_id] = time_data
    return time_data



@app.delete("/times/{time_id}", tags=["Times"])
def deletar_time(time_id: int):
    time = times.pop(time_id, None)
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado.")
    return {"mensagem": "Time deletado com sucesso.", "time": time}


# Rotas para Partidas
@app.get("/partidas/", tags=["Partidas"])
def listar_partidas():
    return {"partidas": list(partidas.values())}


@app.post("/partidas/", tags=["Partidas"])
def adicionar_partida(partida: Partida):
    novo_id = max(partidas.keys(), default=0) + 1
    partida_data = {
        "id": novo_id,
        "time_1": partida.time_1,
        "time_2": partida.time_2,
        "data": partida.data,
        "resultado": partida.resultado,
        "gols": []
    }
    partidas[novo_id] = partida_data
    return partida_data

@app.put("/partidas/{partida_id}/gols", tags=["Partidas"])
def registrar_gols(partida_id: int, input: GolsInput):
    if partida_id not in partidas:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    if input.jogador_id not in jogadores:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")

    jogador = jogadores[input.jogador_id]
    partida = partidas[partida_id]

    # Atualizar a lista de gols na partida
    for _ in range(input.quantidade_gols):
        partida["gols"].append({"jogador": jogador["nome"], "time": jogador["time"]})

    # Atualizar o total de gols do jogador
    jogador["gols"] += input.quantidade_gols

    return {
        "mensagem": f"{jogador['nome']} marcou {input.quantidade_gols} gol(s) na partida {partida_id}.",
        "partida": partida,
        "jogador": jogador
    }


@app.put("/partidas/{partida_id}", tags=["Partidas"])
def atualizar_partida(partida_id: int, partida_update: PartidaUpdate):
    if partida_id not in partidas:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")

    partida = partidas[partida_id]

    # Atualizar os dados da partida
    partida["time_1"] = partida_update.time_1
    partida["time_2"] = partida_update.time_2
    partida["data"] = partida_update.data
    partida["resultado"] = partida_update.resultado

    return partida


@app.delete("/partidas/{partida_id}", tags=["Partidas"])
def deletar_partida(partida_id: int):
    partida = partidas.pop(partida_id, None)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    return {"mensagem": "Partida deletada com sucesso.", "partida": partida}


# Rotas para Jogadores
@app.get("/jogadores/", tags=["Jogadores"])
def listar_jogadores():
    return {"jogadores": list(jogadores.values())}


@app.get("/jogadores/{jogador_id}", tags=["Jogadores"])
def buscar_jogador(jogador_id: int):
    jogador = jogadores.get(jogador_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")
    return jogador


@app.post("/jogadores/", tags=["Jogadores"])
def adicionar_jogador(jogador: Jogador):
    global contador_jogadores
    contador_jogadores += 1
    jogadores[contador_jogadores] = jogador.dict()
    return {"id": contador_jogadores, **jogador.dict()}


@app.delete("/jogadores/{jogador_id}", tags=["Jogadores"])
def deletar_jogador(jogador_id: int):
    jogador = jogadores.pop(jogador_id, None)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")
    return {"mensagem": "Jogador deletado com sucesso.", "jogador": jogador}
