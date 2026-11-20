"""Build a reproducible demonstration using owned synthetic loopback fixtures only."""
from pathlib import Path
import copy
import importlib.util
import os
import sys
from threading import Thread
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/tenant-guardian'
sys.path.insert(0,str(SKILL/'scripts'))
from guardian import initialize,write,load,report,tasks,plan,today
from probe import run

spec=importlib.util.spec_from_file_location('tenant_demo',SKILL/'assets/demo_server.py')
demo=importlib.util.module_from_spec(spec);spec.loader.exec_module(demo)
out=ROOT/'docs/example';out.mkdir(parents=True,exist_ok=True)
base=load(SKILL/'assets/probe-plan.json')
observations={}
for vulnerable in (False,True):
    server=demo.make_server(vulnerable);worker=Thread(target=server.serve_forever,daemon=True);worker.start()
    try:
        fixture=copy.deepcopy(base);fixture['origin']='http://127.0.0.1:'+str(server.server_port)
        env={base['actors'][a]['token_env']:token for a,token in demo.TOKENS.items()}
        with patch.dict(os.environ,env):result=run(fixture,fixture['origin'],True,True)
        name='vulnerable' if vulnerable else 'safe';observations[name]=result
        write(out/('probes-'+name+'.json'),result,True)
    finally:server.shutdown();server.server_close();worker.join(timeout=2)

assessment=initialize('Synthetic two-tenant invoice API','local')
assessment.update(assessor='Automated synthetic demonstration; not a human or customer assessment',
    systems=['Owned loopback invoice fixture'],exclusions=['No customer or production services'],
    scope_unknowns=['Writes, lists, database roles, storage, caches, jobs, websockets and AI paths are not tested by this GET demonstration.'],
    isolation_architecture='Synthetic shared service with explicit object ownership checks',
    synthetic_fixture_ref='skills/tenant-guardian/assets/demo_server.py')
leaks=[c for c in observations['vulnerable']['cases'] if c['result']=='leak_observed']
if len(leaks)!=2 or not observations['vulnerable']['positive_controls_valid']:raise RuntimeError('Synthetic vulnerable fixture did not reproduce expected evidence')
if any(c['result']!='denied' for c in observations['safe']['cases']):raise RuntimeError('Synthetic isolated fixture did not deny configured cross-tenant reads')
assessment['evidence']=[{'id':'SYNTHETIC-GET-LEAK','kind':'test','ref':'docs/example/probes-vulnerable.json',
    'method':'Reproducible loopback demonstration against owned synthetic fixture with vulnerable mode enabled',
    'reviewer':'Automated synthetic demonstration','environment':'local','scope':'Two fixture invoice objects and two distinct synthetic tenant identities; GET only',
    'observed_on':today(),'positive_control':'Both fixture identities returned their own independently seeded response markers',
    'negative_case':'Each actor requested the other fixture tenant invoice',
    'expected':'The foreign synthetic marker is not returned','observed':'Two foreign-marker disclosures were observed in vulnerable fixture mode',
    'actor_scope':'Two distinct synthetic fixture members','resource_scope':'The two configured synthetic invoice GET paths','result':'leak_observed'}]
check=next(c for c in assessment['checks'] if c['id']=='API-001')
check.update(status='confirmed_gap',reviewer='Automated synthetic demonstration',
    rationale='Only the deliberately vulnerable synthetic fixture disclosed both foreign invoice markers. The isolated mode denied the same configured reads.',
    evidence_refs=['SYNTHETIC-GET-LEAK'],severity='high',owner='Synthetic fixture owner',
    recommendation='Enforce the fixture ownership check independently of the requested object identifier.',
    verification_test='Both own-tenant controls succeed and both foreign fixture reads return marker-free denials. This covers GET only.')
write(out/'assessment.json',assessment,True)
report(assessment,out,True);tasks(assessment,out)
test_plan=out/'TEST-PLAN.md'
if test_plan.exists():test_plan.unlink()
plan(assessment,test_plan)
print('Rebuilt synthetic loopback observations, scoped evidence and reports')
