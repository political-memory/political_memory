from dateutil.parser import parse as date_parse
from .models import Dossier, Proposal, Vote
import datetime
# Export

def export_all_dossiers():
    return [export_a_dossier(dossier) for dossier in Dossier.objects.all()]

def export_a_dossier(dossier):
    ret = {'dossier': {
        'title': dossier.title,
        'reference': dossier.reference,
        'text': dossier.text
    }}

    ret['proposals'] = [export_a_proposal(proposal) for proposal in dossier.proposal_set.all()]
    return ret

def export_a_proposal(proposal):
    ret = {
        'title': proposal.title,
        'reference': proposal.reference,
        'description': proposal.description,
        'datetime': proposal.datetime.isoformat(),
        'kind': proposal.kind,
        'total_abstain': proposal.total_abstain,
        'total_against': proposal.total_against,
        'total_for': proposal.total_for
    }

    ret['votes'] = [export_a_vote(vote) for vote in proposal.vote_set.all()]
    return ret

def export_a_vote(vote):
    return {
        'representative_name': vote.representative_name,
        'representative_remote_id': vote.representative_remote_id,
        'postion': vote.position
    }

# Import

def import_a_dossier(dossier_data):
    dossier, created = Dossier.objects.get_or_create(reference=dossier_data['reference'])

    if created:
        dossier_attr = ['title', 'text', 'link']
        for attr in dossier_attr:
            setattr(dossier, attr, dossier_data[attr])
        dossier.save()

    dossier.proposal_set.all().delete()
    for proposal_data in dossier_data['proposals']:
        import_a_proposal(proposal_data, dossier)
        
def import_a_proposal(proposal_data, dossier):
    proposal = Proposal.objects.create(
        dossier=dossier,
        title=proposal_data['title'],
        description=proposal_data['description'],
        reference=proposal_data['reference'],
        datetime=date_parse(proposal_data['datetime']),
        kind=proposal_data['kind'],
        total_abstain=proposal_data['total_abstain'],
        total_against=proposal_data['total_against'],
        total_for=proposal_data['total_for']        
    )
    
    for vote_data in proposal_data['votes']:
        import_a_vote(vote_data, proposal)

def import_a_vote(vote_data, proposal):
    vote_data['proposal'] = proposal
    Vote.objects.create(**vote_data)
