from datetime import datetime

from artists.models import FeaturedArtist

def retrieve_featured_artists(amt):
    featured_artists = FeaturedArtist.objects.all().filter(active=True).select_related('user__username').order_by('last_imprint')[:amt]
    for fa in featured_artists:
        fa.last_imprint = datetime.now()
        fa.total_imprints += 1
        fa.save()

    return featured_artists