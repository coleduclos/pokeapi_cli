# PokeAPI CLI

## Ready the Environment
### Create the Virtual Environmnent
```
python3 -m venv ./env
```
### Activate the Virtual Environment
```
source ./env/bin/activate
```
### Install Dependencies
```
pip install -r requirements.txt
```

## Usage
### Get Pokemon
```
python main.py get_pokemon --id 1 --outfile output.txt
```
### List Pokemon
```
python main.py list_pokemon --paginate --outfile list_output.txt
```



