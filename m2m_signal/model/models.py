from django.db import models
from django.db.models.signals import m2m_changed


class Products(models.Model): 
    
    description = models.TextField(
            "Descrição",
            help_text="Fale brevemente sobre o produto e suas caracteristicas mais importantes",
            max_length=1000,blank=True)
    short_description = models.CharField(
        "Descrição Curta",
          max_length=200, blank=True)
    product_information = models.TextField(
        "Informação do Produto",
            help_text="Descreva como esta o estado do produto",
            max_length=1000,blank=True )
    stock = models.PositiveIntegerField("Quantidade em estoque", default=1)
    available = models.BooleanField("Disponível",default=True)    

    class Meta: 
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


class OpenSearch(models.Model):
    
    own_product = models.OneToOneField(Products, blank=True, on_delete=models.CASCADE, verbose_name="Produto em Busca",
    help_text="Esse é o Produto que esta em busca, estar em qualquer uma das listas resultará em erro")
    like_list = models.ManyToManyField(Products, related_name="likes" , verbose_name="Lista de Curtidos", blank=True)
    dislike_list = models.ManyToManyField(Products, related_name="unlikes" , verbose_name="Lista de Não Curtidos", blank=True)
    match =  models.ManyToManyField(Products, related_name="matches", verbose_name="Lista de Combinações", blank=True)


    def total_likes(self):
        return self.like_list.count()

    def total_matches(self):
        return self.match.count()

    class Meta: 
        verbose_name = "Aberto para Busca"
        verbose_name_plural = "Abertos para Busca"


def matching(sender,*args, **kwargs):

    print(kwargs)

    instance = kwargs['instance']
    search_pk = instance.pk
    own_product_pk = instance.own_product.pk    
    like_list = list(instance.like_list.values_list('pk', flat=True))
    match_list = list(instance.match.values_list('pk', flat=True))

    if like_list :

        print(">"*50)
        
        for el in like_list:
                prod = Products.objects.get(id=el)
                own_pk = prod.pk
                open_search = OpenSearch.objects.get(own_product=prod)
                likes = list(open_search.like_list.values_list('pk', flat=True))                
                
                if own_product_pk in likes :
                    try :                       
                        open_search.match.add(prod)
                    except Exception as e :
                        print(e)

    # In case that doesn't exist likes, delete the remaining matches
    if not like_list:
        for el in match_list :
            produto = Products.objects.get(pk=el)
            instance.match.remove(produto)

m2m_changed.connect(matching, sender=OpenSearch.like_list.through)

