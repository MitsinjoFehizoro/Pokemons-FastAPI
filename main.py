import json
from dataclasses import asdict, dataclass
from typing import Union
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware

# =======================================================================================
with open("pokemons.json") as file:
    list_pokemons = json.load(file)

pokemonsLists = {index + 1: pokemon for index, pokemon in enumerate(list_pokemons)}

# =======================================================================================


@dataclass
class Pokemon:
    id: int
    name: str
    types: list[str]
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    evolutionId: Union[int, None] = None


# =======================================================================================

app = FastAPI()

origins = [
   "http://localhost:5173/"
]

app.add_middleware(
   CORSMiddleware,
   allow_origins = origins,
   allow_method = ['*'],
   allow_credentials = True
)
# ================================ END POINT ==========================================


@app.get("/total-pokemons")
def get_total_pokemons() -> dict:
   return {"total": len(pokemonsLists)}


@app.get("/pokemons")
def get_all_pokemons() -> list[Pokemon]:
   res = []
   for id in pokemonsLists:
      res.append(Pokemon(**pokemonsLists[id]))
   return res


@app.get("/pokemon/{id}")
def get_pokemon_by_id(id: int = Path(ge=1)) -> Pokemon:
   if id not in pokemonsLists:
      raise HTTPException(status_code=404, detail="Pokemon not found.")
   return Pokemon(**pokemonsLists[id])


@app.post("/pokemon/")
def create_pokemon(pokemon: Pokemon) -> Pokemon:
   if pokemon.id in pokemonsLists:
      raise HTTPException(
         status_code=409, detail=f"Pokemon with id : {pokemon.id} already exist."
      )
   pokemonsLists[pokemon.id] = asdict(pokemon)
   return pokemon


@app.put("/pokemon/{id}")
def update_pokemon(pokemon: Pokemon, id: int = Path(ge=1)) -> Pokemon:
   if id not in pokemonsLists:
      raise HTTPException(status_code=404, detail="Pokemon not found.")
   pokemonsLists[id] = asdict(pokemon)
   return pokemon

@app.delete('/pokemon/{id}')
def delete_pokemon(id:int = Path(ge=1)) -> Pokemon :
   if id not in pokemonsLists:
      raise HTTPException(status_code=404, detail="Pokemon not found.")
   pokemon = Pokemon(**pokemonsLists[id])
   del pokemonsLists[id]
   return pokemon

@app.get("/types")
def get_all_types()->list[str] :	
   types = []
   for pokemon in list_pokemons :
      for type in pokemon['types'] :
         if type not in types :
            types.append(type)
   types.sort()
   return types