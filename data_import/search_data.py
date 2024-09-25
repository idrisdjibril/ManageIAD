#from django_elasticsearch_dsl import Document, fields
#from django_elasticsearch_dsl.registries import registry
#from .models import DHIS2Data  # Assurez-vous que ce modèle existe

#@registry.register_document
#class DHIS2DataDocument(Document):
 #   class Index:
  #      name = 'dhis2data'
   #     settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    #commune_id = fields.TextField()
    #event = fields.TextField()
    #_date_de_saisie_ = fields.DateField()
    # Ajoutez d'autres champs selon votre modèle

    #class Django:
       # model = DHIS2Data