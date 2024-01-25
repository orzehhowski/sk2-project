# sk2-project

Prosta konsola do wykonywania shellowych poleceń na zdalnym urządzeniu, na którym został uruchomiony `server.py`. Po nawiązaniu połączenia poprzez uruchomienie `client.py` klient proszony jest o podanie nazwy użytkownika i hasła, które zostanie wykorzystane do próby autentykacji na konto systemowe systemu na którym odpalony jest serwer. Następnie użytkownik może wpisywać komendy niewymagające uprawnień administratora oraz niepytające o kolejny input. Programy działają na systemie Linux z zainstalowanym Pythonem.

### how to run

w terminalu w głównym folderze projektu:

```
python3 -m venv venv
source ./venv/bin/activate
pip install -r ./requirements.txt
python3 ./server.py
```

i w kolejnych terminalach, które będą klientami (również w głównym folderze):

```
source ./venv/bin/activate
python3 ./client.py
```
