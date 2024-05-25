from elasticsearch import Elasticsearch
from config import ElasticSearchConfig

elastic_config = ElasticSearchConfig()
client = Elasticsearch(f'https://{elastic_config.elastic_host}:{elastic_config.elastic_port}',
                       verify_certs=False, ca_certs=elastic_config.elastic_certificate_path,
                       basic_auth=(elastic_config.elastic_username, elastic_config.elastic_password))
