import csv

def main(model_type):

    if model_type == 'LivedoorNewscorpus':
        from mining_apps.models import LivedoorNewscorpus
        LivedoorNewscorpus.objects.all().delete()

    elif model_type == 'fetch_20newsgroups':
        pass
        #fetch_20newsgroups.objects.all().delete()

    else:
        pass