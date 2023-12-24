# To start the docker stack
# ./start.sh
# ./start.sh --build    re-build the images before creating the containers

export HS_TELEGRAM_BOT_TOKEN="XXX" 
export HS_TELEGRAM_CHAT_ID="XXX"

if [ ! -z $1 ] 
then
    docker-compose up -d $1
else
    docker-compose up -d
fi