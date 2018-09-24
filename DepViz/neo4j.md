# neo4j

## run with docker

```
docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    --volume=$HOME/neo4j/logs:/logs \
    neo4j:3.4.7
```

## example queries

### show all
`MATCH (n) OPTIONAL MATCH (n)-[r]-() RETURN n, r;`

### show all that that 'uses' activemq
``MATCH (n)-[:USES]->(m) WHERE m.name = 'activemq' RETURN n,m;