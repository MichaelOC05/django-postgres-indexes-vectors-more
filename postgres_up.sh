
read -sp "Enter password: " PASSWORD
echo
export PASSWORD

docker compose -f postgres.yaml up -d