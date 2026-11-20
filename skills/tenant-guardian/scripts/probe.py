"""Opt-in synthetic GET probes for two explicitly scoped tenant identities.

No redirects, retries, environment proxies, raw-response persistence or writes.
Denial is meaningful only after both own-tenant positive controls succeed.
"""
import argparse
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from guardian import load,today,write

MAX_BODY=1048576

def origin(value):
    if not isinstance(value,str):raise ValueError('Origin must be a string')
    u=urllib.parse.urlsplit(value)
    if u.scheme not in ('http','https') or not u.hostname or u.username or u.password or u.query or u.fragment or u.path not in ('','/'):
        raise ValueError('Use an origin without path, credentials, query or fragment')
    try:port=u.port
    except ValueError:raise ValueError('Invalid port')
    if u.scheme=='http' and u.hostname not in ('localhost','127.0.0.1','::1'):
        raise ValueError('HTTP is allowed only for explicit loopback fixtures; use HTTPS for staging')
    return (u.scheme,u.hostname,port or (443 if u.scheme=='https' else 80))

def validate_plan(p):
    if not isinstance(p,dict) or p.get('schema_version')!='1.0':raise ValueError('Unsupported probe plan')
    origin(p.get('origin'))
    if p.get('environment') not in ('local','test','staging') or p.get('synthetic_only') is not True:
        raise ValueError('Only explicitly synthetic local/test/staging fixtures are supported')
    actors=p.get('actors');resources=p.get('resources')
    if not isinstance(actors,dict) or len(actors)!=2:raise ValueError('Provide exactly two synthetic actors')
    tenant_ids=[];envs=[]
    for key,a in actors.items():
        if not re.fullmatch('[A-Za-z0-9_-]{1,40}',key) or not isinstance(a,dict):raise ValueError('Invalid actor')
        for field in ('tenant','token_env'):
            if not isinstance(a.get(field),str):raise ValueError('Actor needs tenant and token_env')
        if not re.fullmatch('[A-Z][A-Z0-9_]{2,79}',a['token_env']):raise ValueError('Use environment-variable names, never token values')
        tenant_ids.append(a['tenant']);envs.append(a['token_env'])
    if len(set(tenant_ids))!=2 or any(not x for x in tenant_ids) or len(set(envs))!=2:
        raise ValueError('Use distinct tenant labels and credential variables')
    if not isinstance(resources,list) or not 2<=len(resources)<=20:raise ValueError('Provide 2 to 20 synthetic resources')
    labels=set();markers=set();owners=set()
    for r in resources:
        if not isinstance(r,dict):raise ValueError('Invalid resource')
        label=r.get('label');owner=r.get('owner');path=r.get('path');marker=r.get('marker')
        if not isinstance(label,str) or not re.fullmatch('[A-Za-z0-9_-]{1,80}',label) or label in labels:raise ValueError('Resource labels must be unique')
        if not isinstance(owner,str) or owner not in actors:raise ValueError('Unknown resource owner')
        if not isinstance(path,str) or not path.startswith('/') or path.startswith('//') or '\\' in path or any(ord(c)<32 for c in path):raise ValueError('Use a relative application path')
        u=urllib.parse.urlsplit(path)
        decoded=urllib.parse.unquote(urllib.parse.unquote(u.path))
        if u.scheme or u.netloc or u.fragment or '..' in decoded.split('/') or decoded.startswith('//'):
            raise ValueError('Unsafe application path')
        if not isinstance(marker,str) or not re.fullmatch('[A-Za-z0-9_-]{16,128}',marker) or marker in markers:
            raise ValueError('Use distinct opaque synthetic markers of 16 to 128 characters')
        labels.add(label);markers.add(marker);owners.add(owner)
    if owners!=set(actors):raise ValueError('Include own-tenant positive controls for both actors')
    if any(a!=b and (a in b or b in a) for a in markers for b in markers):raise ValueError('Synthetic markers must not overlap')
    if any(marker in urllib.parse.unquote(urllib.parse.unquote(r['path'])) for marker in markers for r in resources):
        raise ValueError('Seed markers in stored response data, not request paths')
    return p

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args):return None

def fetch(url,token,timeout):
    request=urllib.request.Request(url,headers={'Authorization':'Bearer '+token,'Accept':'application/json','User-Agent':'CTOside-Tenant-Guardian/1.0'},method='GET')
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    try:
        response=opener.open(request,timeout=timeout)
    except urllib.error.HTTPError as e:response=e
    except (urllib.error.URLError,TimeoutError,OSError,http.client.HTTPException):return {'status':None,'body':b'','truncated':False,'transport_error':True}
    try:
        with response:
            body=response.read(MAX_BODY+1)
            return {'status':response.status,'body':body[:MAX_BODY], 'truncated':len(body)>MAX_BODY,'transport_error':False}
    except (OSError,http.client.HTTPException):
        return {'status':getattr(response,'status',None),'body':b'','truncated':False,'transport_error':True}

def run(p,allow_origin,allow_network=False,synthetic_only=False,timeout=10,transport=fetch):
    validate_plan(p)
    if not allow_network or not synthetic_only:raise ValueError('Active probes require --allow-network and --synthetic-only')
    if origin(allow_origin)!=origin(p['origin']):raise ValueError('Explicit allowed origin must match plan origin')
    if not 1<=timeout<=30:raise ValueError('Timeout must be between 1 and 30 seconds')
    actors=p['actors'];tokens={}
    for name,a in actors.items():
        token=os.environ.get(a['token_env'],'')
        if not token or len(token)>8192 or any(ord(c)<32 or ord(c)>126 for c in token):raise ValueError('Missing or invalid synthetic actor credential')
        tokens[name]=token
    if len(set(tokens.values()))!=2:raise ValueError('Two distinct credentials are required')
    if any(r['marker'] in token for r in p['resources'] for token in tokens.values()):
        raise ValueError('Synthetic response markers must not be embedded in credentials')
    observations=[];baselines={};overall=True
    def request(resource,actor,phase):
        raw=transport(p['origin'].rstrip('/')+resource['path'],tokens[actor],timeout)
        body=raw['body'];target=resource['marker'].encode() in body
        foreign=any(r['marker'].encode() in body for r in p['resources'] if actors[r['owner']]['tenant']!=actors[actor]['tenant'])
        obs={'resource':resource['label'],'actor':actor,'phase':phase,'http_status':raw['status'],
            'target_marker_present':target,'foreign_marker_present':foreign,'truncated':raw['truncated'],
            'transport_error':raw['transport_error'],'response_sha256':hashlib.sha256(body).hexdigest()}
        observations.append(obs);return obs
    for r in p['resources']:
        b=request(r,r['owner'],'own_tenant_positive_control')
        good=b['http_status']==200 and b['target_marker_present'] and not b['foreign_marker_present'] and not b['truncated'] and not b['transport_error']
        baselines[r['label']]=good;overall=overall and good
    cases=[]
    for r in p['resources']:
        actor=next(a for a in actors if a!=r['owner'])
        if not overall:
            cases.append({'resource':r['label'],'actor':actor,'result':'inconclusive','reason':'Positive controls are incomplete or contaminated; cross-tenant requests skipped.'});continue
        o=request(r,actor,'cross_tenant_negative_case')
        if o['foreign_marker_present']:result='leak_observed';reason='Known foreign synthetic marker appeared in this response.'
        elif o['http_status'] in (403,404) and not o['truncated'] and not o['transport_error']:result='denied';reason='Scoped object read was denied after valid positive controls.'
        else:result='inconclusive';reason='Response does not establish denial; authentication errors, redirects, empty successful responses and transport failures need review.'
        cases.append({'resource':r['label'],'actor':actor,'result':result,'reason':reason})
    baseline_leaks=[{'resource':o['resource'],'actor':o['actor'],'result':'leak_observed','reason':'Foreign synthetic marker appeared during an own-tenant baseline.'} for o in observations if o['phase']=='own_tenant_positive_control' and o['foreign_marker_present']]
    return {'schema_version':'1.0','observed_on':today(),'environment':p['environment'],'status':'review_required',
        'plan_sha256':hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'request_count':len(observations),'positive_controls_valid':overall,'cases':baseline_leaks+cases,'observations':observations,
        'notice':'Results cover only the explicitly configured GET paths and synthetic identities. Tokens, raw bodies, markers and paths are not included. No assessment status has been changed.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',required=True);p.add_argument('--out')
    p.add_argument('--allow-origin');p.add_argument('--allow-network',action='store_true');p.add_argument('--synthetic-only',action='store_true')
    p.add_argument('--dry-run',action='store_true');p.add_argument('--timeout',type=int,default=10);a=p.parse_args()
    try:
        plan=validate_plan(load(a.plan))
        if a.dry_run:
            print(json.dumps({'status':'dry_run_no_requests','resources':len(plan['resources']),'maximum_requests':2*len(plan['resources']),'environment':plan['environment']}));return
        if not a.out or not a.allow_origin:raise ValueError('Supply --out and --allow-origin for active probes')
        # Refuse output collisions before any request is sent.
        from guardian import output
        if output(a.out).exists():raise ValueError('Choose a new output path')
        write(a.out,run(plan,a.allow_origin,a.allow_network,a.synthetic_only,a.timeout))
    except (ValueError,OSError,TypeError,KeyError) as e:p.exit(1,'Tenant Guardian probe: '+str(e)+'\n')
if __name__=='__main__':main()
