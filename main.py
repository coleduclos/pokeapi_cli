import argparse
import json
import requests

class PokeApiClient():
    def __init__(self, limit=100):
        self.base_url = "https://pokeapi.co/api/v2"
        self.limit = 100

    def get_pokemon(self, id):
        url = "{}/{}/{}".format(self.base_url, "pokemon", id)
        print("Retrieving... {}".format(url))
        response = requests.get(url)
        return response.json()

    def list_pokemon(self, paginate=False):
        url = "{}/{}?limit={}".format(self.base_url, "pokemon", self.limit)
        print("Retrieving... {}".format(url))
        response = requests.get(url)
        response_json = response.json()
        output = response_json.get('results', [])
        if paginate:
            while response_json.get('next'):
                print("Retrieving... {}".format(response_json.get('next')))
                response = requests.get(response_json["next"])
                response_json = response.json()
                output += response_json.get('results',[])
                
        return output

def write_dict_to_file(data, filename):
    f = open(filename, 'w', encoding='utf-8')
    json.dump(data, f)

def get_pokemon(args):
    client = PokeApiClient()
    pokemon = client.get_pokemon(args.id)
    if args.print:
        print(json.dumps(pokemon))
    if args.outfile:
        write_dict_to_file(pokemon, args.outfile)

def list_pokemon(args):
    client = PokeApiClient()
    pokemon = client.list_pokemon(paginate=args.paginate)
    if args.print:
        print(json.dumps(pokemon))
    if args.outfile:
        write_dict_to_file(pokemon, args.outfile)

def format_pokemon(args):
    client = PokeApiClient()
    pokemon_list = client.list_pokemon(paginate=args.paginate)
    output = []
    for pokemon in pokemon_list:
        p = client.get_pokemon(pokemon["name"])
        types = []
        for t in p["types"]:
            types.append(t["type"]["name"])
        stats = []
        for s in p["stats"]:
            stats.append({
                "name" : s["stat"]["name"],
                "base_stat" : s["base_stat"],
                "effort": s["effort"]
            })
        moves = []
        for m in p["moves"]:
            moves.append({
                "name" : m["move"]["name"]
            })
        output.append(
            {
                "name": p["name"],
                "id" : p["id"],
                "height": p["height"],
                "moves" : moves,
                "types" : types,
                "stats" : stats,
                "weight": p["weight"]
            }
        )
    if args.print:
        print(json.dumps(output))
    if args.outfile:
        write_dict_to_file(output, args.outfile)

def build_parser():
    parser = argparse.ArgumentParser(description="PokeAPI CLI tool")

    # Sub-parsers
    subparsers = parser.add_subparsers(help='sub-command help')
    list_pokemon_parser = subparsers.add_parser("list_pokemon")
    list_pokemon_parser.add_argument("--outfile", 
        help="Filename to write results to."
    )
    list_pokemon_parser.add_argument('--paginate',
        action='store_true',
        help='Paginate to get all results.'
    )
    list_pokemon_parser.add_argument('--print',
        action='store_true',
        help='Print results to std out.'
    )
    list_pokemon_parser.set_defaults(func=list_pokemon)

    get_pokemon_parser = subparsers.add_parser("get_pokemon")
    get_pokemon_parser.add_argument('--id',
        required=True,
        help='Id or name of pokemon.'
    )
    get_pokemon_parser.add_argument('--print',
        action='store_true',
        help='Print results to std out.'
    )
    get_pokemon_parser.add_argument("--outfile", 
        help="Filename to write results to."
    )
    get_pokemon_parser.set_defaults(func=get_pokemon)

    format_pokemon_parser = subparsers.add_parser("format_pokemon")
    format_pokemon_parser.add_argument('--paginate',
        action='store_true',
        help='Paginate to get all results.'
    )
    format_pokemon_parser.add_argument('--print',
        action='store_true',
        help='Print results to std out.'
    )
    format_pokemon_parser.add_argument("--outfile", 
        help="Filename to write results to."
    )
    format_pokemon_parser.set_defaults(func=format_pokemon)

    return parser

def main():
    parser = build_parser()
    args, unknown = parser.parse_known_args()
    args.func(args)

if __name__ == "__main__":
    main()