# Descargamos el archivo .dump de https://monarchinitiative.org/kg/downloads
wget https://data.monarchinitiative.org/monarch-kg/latest/monarch-kg.neo4j.dump

# Copiamos el archivo descargado .dump a la carpeta /import
sudo mv ~/Descargas/monarch-kg.neo4j.dump ~/neo4j/import/monarchkg.dump

# Cargamos el dump
docker exec -u neo4j -it neo4j_local neo4j-admin database load monarchkg --from-path=/import/ --overwrite-destination=true

# Migración. la base de datos se creo en Neo4J 4.3 y el contenedor es de Neo4J >5
docker exec -u neo4j -it neo4j_local neo4j-admin database migrate monarchkg

# Reinicio del contenedor
docker compose restart neo4j

# Creamos la base de datos apuntando a los nuevos datos
CREATE DATABASE monarchkg;
