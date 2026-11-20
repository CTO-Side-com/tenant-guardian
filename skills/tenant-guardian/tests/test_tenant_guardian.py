"""Offline tests plus synthetic loopback integration tests. No external traffic."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from threading import Thread
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from guardian import initialize,validate,report,tasks,recheck,scan,write,plan,cell,catalog
from probe import validate_plan,run,origin,MAX_BODY,fetch

def test_evidence(result='denied'):
    return {'id':'EV-TEST','kind':'test','ref':'synthetic/probe-results.json','method':'Synthetic scoped test review',
        'reviewer':'Synthetic Reviewer','environment':'staging','scope':'Synthetic invoice GET / two fixture identities',
        'observed_on':'2026-11-19','positive_control':'Both synthetic identities read their own known objects',
        'negative_case':'Actor A requests synthetic object B','expected':'No foreign data returned','observed':'Synthetic denial' if result=='denied' else result,
        'actor_scope':'Synthetic tenant A member','resource_scope':'Synthetic invoice B','result':result}

class AssessmentTests(unittest.TestCase):
    def setUp(self):self.a=initialize('Synthetic SaaS','staging')
    def bad(self):self.assertTrue(validate(self.a))
    def verified(self):
        self.a['evidence']=[test_evidence()];c=self.a['checks'][0]
        c.update(status='verified_in_scope',reviewer='Synthetic Reviewer',rationale='Synthetic scoped test supports denial',evidence_refs=['EV-TEST'],verified_scope='Synthetic invoice GET only, two identities, staging, observed 2026-11-19')
        return c
    def test_initialization(self):self.assertEqual([],validate(self.a));self.assertEqual(36,len(self.a['checks']));self.assertTrue(all(c['status']=='insufficient_evidence' for c in self.a['checks']))
    def test_unique_catalog(self):self.assertEqual(36,len({c['id'] for c in catalog()['checks']}))
    def test_blank_product(self):
        with self.assertRaises(ValueError):initialize('','staging')
    def test_scoped_runtime_denial(self):self.verified();self.assertEqual([],validate(self.a))
    def test_verification_requires_runtime(self):self.verified();self.a['evidence'][0]['kind']='code';self.bad()
    def test_verification_requires_scope(self):self.verified()['verified_scope']='';self.bad()
    def test_verification_rejects_leak(self):self.verified();self.a['evidence'][0]['result']='leak_observed';self.bad()
    def test_verification_rejects_inconclusive(self):self.verified();self.a['evidence'][0]['result']='inconclusive';self.bad()
    def test_test_requires_positive_control(self):self.verified();self.a['evidence'][0]['positive_control']='';self.bad()
    def test_test_requires_actor_scope(self):self.verified();self.a['evidence'][0]['actor_scope']='';self.bad()
    def test_missing_reviewer(self):self.verified()['reviewer']='';self.bad()
    def test_unknown_reference(self):self.verified()['evidence_refs']=['missing'];self.bad()
    def test_duplicate_evidence(self):self.verified();self.a['evidence'].append(copy.deepcopy(self.a['evidence'][0]));self.bad()
    def test_duplicate_check(self):self.a['checks'].append(copy.deepcopy(self.a['checks'][0]));self.bad()
    def test_missing_check(self):self.a['checks'].pop();self.bad()
    def test_environment_mismatch(self):self.verified();self.a['evidence'][0]['environment']='production';self.bad()
    def test_future_observation(self):self.verified();self.a['evidence'][0]['observed_on']='2099-01-01';self.bad()
    def test_invalid_hash(self):self.verified();self.a['evidence'][0]['sha256']='invalid';self.bad()
    def test_unknown_catalog(self):self.a['catalog_version']='unknown';self.bad()
    def test_malformed_status(self):self.a['checks'][0]['status']=[];self.bad()
    def test_malformed_kind(self):self.verified();self.a['evidence'][0]['kind']=[];self.bad()
    def test_malformed_refs(self):self.a['checks'][0]['evidence_refs']=None;self.bad()
    def test_malformed_watch(self):self.a['checks'][0]['watched_paths']=[None];self.bad()
    def test_missing_severity(self):self.a['checks'][0].pop('severity');self.bad()
    def test_malformed_systems(self):self.a['systems']='staging';self.bad()
    def test_inapplicable_needs_approval(self):self.verified().update(status='not_applicable',approved_by='');self.bad()
    def test_inapplicable_with_approval(self):self.verified().update(status='not_applicable',approved_by='Synthetic Owner');self.assertEqual([],validate(self.a))
    def test_confirmed_needs_support_and_action(self):
        c=self.verified();c.update(status='confirmed_gap',owner='Synthetic Owner',severity='high',recommendation='Fix synthetic boundary',verification_test='Retest boundary');self.bad()
        self.a['evidence'][0]['result']='leak_observed';self.assertEqual([],validate(self.a))
    def test_confirmed_code_finding(self):
        c=self.verified();self.a['evidence'][0]['kind']='code';c.update(status='confirmed_gap',owner='Owner',severity='high',recommendation='Fix',verification_test='Retest');self.assertEqual([],validate(self.a))
    def test_all_reports(self):
        with tempfile.TemporaryDirectory() as d:
            report(self.a,d,True);self.assertEqual(36,tasks(self.a,d));plan(self.a,Path(d)/'plan.md')
            self.assertTrue(Path(d,'TENANT-ISOLATION.pdf').read_bytes().startswith(b'%PDF'))
            manifest=json.loads(Path(d,'handoff-manifest.json').read_text())
            for f in manifest['files']:self.assertEqual(f['sha256'],hashlib.sha256(Path(d,f['path']).read_bytes()).hexdigest())
    def test_invalid_assessment_produces_no_reports(self):
        self.a['checks'].pop()
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):report(self.a,d)
            with self.assertRaises(ValueError):tasks(self.a,d)
            self.assertEqual([],list(Path(d).iterdir()))
    def test_report_scope_and_redaction(self):
        self.a['product']='person@example.com';self.a['scope_unknowns']=['Synthetic unknown']
        with tempfile.TemporaryDirectory() as d:
            report(self.a,d);text=Path(d,'TENANT-ISOLATION.md').read_text();self.assertNotIn('person@example.com',text);self.assertIn('Synthetic unknown',text)
    def test_safe_tracker_exports(self):
        self.a['checks'][0]['recommendation']='@channel <https://bad.test> person@example.com'
        with tempfile.TemporaryDirectory() as d:
            tasks(self.a,d);text=Path(d,'tasks-slack.txt').read_text();self.assertNotIn('@channel',text);self.assertNotIn('<https',text);self.assertNotIn('person@example.com',text)
        self.assertTrue(cell('  =SUM(1,2)').startswith("'"))
    def test_symlink_output_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'sentinel');p.write_text('keep');Path(d,'TENANT-ISOLATION.md').symlink_to(p)
            with self.assertRaises(ValueError):report(self.a,d)
            self.assertEqual('keep',p.read_text())
    def test_init_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'x.json');write(p,self.a)
            with self.assertRaises(FileExistsError):write(p,self.a)
    def test_plan_preserves_existing_assessment(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'assessment.json');write(p,self.a);before=p.read_bytes()
            with self.assertRaises(FileExistsError):plan(self.a,p)
            self.assertEqual(before,p.read_bytes())
    def test_plan_includes_architecture_and_exclusions(self):
        with tempfile.TemporaryDirectory() as d:
            self.a['isolation_architecture']='Separate databases';self.a['exclusions']=['No AI or queues in scope'];plan(self.a,Path(d,'separate.md'))
            s=Path(d,'separate.md').read_text();self.assertIn('bounded database credentials',s);self.assertIn('No AI or queues in scope',s)
            self.a['isolation_architecture']='Shared-table RLS';plan(self.a,Path(d,'rls.md'));self.assertIn('owner/bypass behavior',Path(d,'rls.md').read_text())
    def test_cli_report_preserves_source_assessment(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d,'assessment-redacted.json');write(p,self.a);before=p.read_bytes()
            r=subprocess.run([sys.executable,str(ROOT/'scripts/guardian.py'),'report','--assessment',str(p),'--out',d],capture_output=True,text=True)
            self.assertNotEqual(0,r.returncode);self.assertEqual(before,p.read_bytes());self.assertNotIn('Traceback',r.stderr)
    def test_recheck_preserves_baseline(self):
        self.verified();new=recheck(self.a,['app/api.py']);self.assertEqual('verified_in_scope',self.a['checks'][0]['status']);self.assertEqual('insufficient_evidence',new['checks'][0]['status']);self.assertEqual(['EV-TEST'],new['checks'][0]['stale_evidence']);self.assertEqual('',new['checks'][0]['verified_scope'])
    def test_recheck_watch(self):
        c=self.verified();c['watched_paths']=['backend/*'];self.assertEqual('verified_in_scope',recheck(self.a,['frontend/a.ts'])['checks'][0]['status'])
    def test_recheck_no_changes(self):self.assertEqual([],recheck(self.a,[])['recheck']['invalidated'])
    def test_recheck_traversal(self):
        with self.assertRaises(ValueError):recheck(self.a,['../secret'])
    def test_scanner_metadata_only(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'api.py').write_text('invoice = session.get(Invoice, invoice_id)\n')
            s=scan(d);self.assertEqual(1,len(s['findings']));self.assertEqual('unconfirmed_lead',s['findings'][0]['status']);self.assertNotIn('invoice_id',json.dumps(s))
    def test_scanner_secret_and_fixture_exclusions(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'.env').write_text('CURRENT_TENANT = A');Path(d,'fixtures').mkdir();Path(d,'fixtures','a.py').write_text('CURRENT_TENANT = A');Path(d,'link.py').symlink_to(Path(d,'.env'))
            self.assertEqual([],scan(d)['findings'])
    def test_scanner_skips_known_credential_files(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'credentials.json').write_text('CURRENT_TENANT = A');self.assertEqual(0,scan(d)['files_considered'])
    def test_scanner_rls_and_local_context(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'db.sql').write_text('ALTER ROLE api BYPASSRLS;\nSET LOCAL app.tenant_id = A;\n')
            s=scan(d);self.assertEqual(['rls-bypass-role'],[x['rule'] for x in s['findings']])
    def test_scanner_limits(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'api.py').write_text('session.get(A, x)\nsession.get(B,y)');self.assertTrue(scan(d,max_findings=1)['limit_reached'])
    def test_scanner_missing_directory_clean_cli_error(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/guardian.py'),'scan','--repo','/not/a/real/tenant/repo','--out','unused.json'],capture_output=True,text=True)
        self.assertNotEqual(0,p.returncode);self.assertNotIn('Traceback',p.stderr)

class OutputGuardTests(unittest.TestCase):
    def in_tmp(self,sub=False):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);old=os.getcwd();os.chdir(tmp.name);self.addCleanup(os.chdir,old)
        os.makedirs('out/real/sub' if sub else 'out/real');os.symlink('real','out/link');return tmp.name
    def outside(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);old=os.getcwd();self.addCleanup(os.chdir,old)
        for d in ('work','real/sub'):os.makedirs(os.path.join(tmp.name,d))
        os.symlink('real',os.path.join(tmp.name,'link'));os.chdir(os.path.join(tmp.name,'work'));return tmp.name
    def test_planted_symlink_folder_inside_cwd_is_refused(self):
        self.in_tmp()
        with self.assertRaises(ValueError):write('out/link/report.json',{})
        self.assertEqual([],os.listdir('out/real'))
    def test_planted_symlink_deeper_in_path_is_refused(self):
        self.in_tmp(True)
        with self.assertRaises(ValueError):write('out/link/sub/report.json',{})
        self.assertEqual([],os.listdir('out/real/sub'))
    def test_alias_path_to_planted_symlink_is_refused(self):
        name=self.in_tmp(True)
        with self.assertRaises(ValueError):write(os.path.join(name,'out','link','sub','report.json'),{})
        self.assertEqual([],os.listdir('out/real/sub'))
    def test_dotdot_cannot_sidestep_guard(self):
        self.in_tmp(True)
        with self.assertRaises(ValueError):write('out/real/../link/sub/report.json',{})
        self.assertEqual([],os.listdir('out/real/sub'))
    def test_case_variant_path_to_planted_symlink_is_refused(self):
        self.in_tmp(True);cwd=os.getcwd();up=cwd.upper()
        if up==cwd or not os.path.isdir(up):self.skipTest('case-sensitive filesystem: no case-variant alias of the working directory')
        with self.assertRaises(ValueError):write(up+'/out/link/sub/report.json',{})
        self.assertEqual([],os.listdir('out/real/sub'))
    def test_symlinked_parent_outside_cwd_is_refused(self):
        name=self.outside()
        with self.assertRaises(ValueError):write('../link/report.json',{})
        self.assertEqual(['sub'],os.listdir(os.path.join(name,'real')))
    def test_symlink_above_output_folder_outside_cwd_is_allowed(self):
        # The macOS case: /var and /tmp are symlinks above every temporary folder.
        name=self.outside();write(os.path.join(name,'link','sub','report.json'),{})
        self.assertTrue(os.path.isfile(os.path.join(name,'real','sub','report.json')))
    def test_dotdot_is_normalised_before_checking(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);old=os.getcwd();os.chdir(tmp.name);self.addCleanup(os.chdir,old)
        os.makedirs('out');os.makedirs('elsewhere');os.symlink('../elsewhere','out/link')
        try:write('out/link/../x.json',{})
        except ValueError:self.fail("'..' was not collapsed before the symlink check")
        self.assertTrue(os.path.isfile('out/x.json'));self.assertFalse(os.path.exists('x.json'));self.assertFalse(os.path.exists('elsewhere/x.json'))

class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.p=json.loads((ROOT/'assets/probe-plan.json').read_text())
        self.env={'TG_TOKEN_A':'synthetic-token-A','TG_TOKEN_B':'synthetic-token-B'}
    def transport(self,mode='safe',foreign_status=403,truncated=False):
        def send(url,token,timeout):
            r=next(x for x in self.p['resources'] if url.endswith(x['path']))
            owner_token=self.env[self.p['actors'][r['owner']]['token_env']]
            own=token==owner_token
            if own:status=200;body=r['marker'].encode();tr=False
            elif mode=='leak':status=foreign_status;body=r['marker'].encode();tr=truncated
            else:status=foreign_status;body=b'{"synthetic":"no-data"}';tr=truncated
            if mode=='bad-auth' and own:status=401;body=b'not authenticated'
            if mode=='bad-baseline' and own:status=200;body=b'empty'
            return {'status':status,'body':body,'truncated':tr,'transport_error':False}
        return send
    def execute(self,**kwargs):
        with patch.dict(os.environ,self.env):return run(self.p,self.p['origin'],True,True,transport=kwargs.pop('transport',self.transport()),**kwargs)
    def test_plan_valid(self):self.assertEqual(self.p,validate_plan(self.p))
    def test_safe_reads(self):
        r=self.execute();self.assertEqual(4,r['request_count']);self.assertTrue(r['positive_controls_valid']);self.assertTrue(all(c['result']=='denied' for c in r['cases']))
    def test_detects_leak_even_on_denial_status(self):
        r=self.execute(transport=self.transport('leak',403));self.assertTrue(all(c['result']=='leak_observed' for c in r['cases']))
    def test_detects_leak_on_200(self):self.assertTrue(all(c['result']=='leak_observed' for c in self.execute(transport=self.transport('leak',200))['cases']))
    def test_inconclusive_auth_errors(self):self.assertTrue(all(c['result']=='inconclusive' for c in self.execute(transport=self.transport(foreign_status=401))['cases']))
    def test_inconclusive_empty_success(self):self.assertTrue(all(c['result']=='inconclusive' for c in self.execute(transport=self.transport(foreign_status=200))['cases']))
    def test_inconclusive_redirect(self):self.assertTrue(all(c['result']=='inconclusive' for c in self.execute(transport=self.transport(foreign_status=302))['cases']))
    def test_inconclusive_server_error(self):self.assertTrue(all(c['result']=='inconclusive' for c in self.execute(transport=self.transport(foreign_status=500))['cases']))
    def test_404_denial_supported(self):self.assertTrue(all(c['result']=='denied' for c in self.execute(transport=self.transport(foreign_status=404))['cases']))
    def test_truncated_clean_denial_inconclusive(self):self.assertTrue(all(c['result']=='inconclusive' for c in self.execute(transport=self.transport(truncated=True))['cases']))
    def test_truncated_known_leak_still_detected(self):self.assertTrue(all(c['result']=='leak_observed' for c in self.execute(transport=self.transport('leak',200,True))['cases']))
    def test_bad_auth_skips_foreign_requests(self):
        r=self.execute(transport=self.transport('bad-auth'));self.assertEqual(2,r['request_count']);self.assertFalse(r['positive_controls_valid']);self.assertTrue(all(c['result']=='inconclusive' for c in r['cases']))
    def test_missing_marker_skips_foreign_requests(self):self.assertEqual(2,self.execute(transport=self.transport('bad-baseline'))['request_count'])
    def test_baseline_foreign_leak_visible(self):
        def t(url,token,timeout):return {'status':200,'body':' '.join(r['marker'] for r in self.p['resources']).encode(),'truncated':False,'transport_error':False}
        r=self.execute(transport=t);self.assertEqual(2,r['request_count']);self.assertEqual(2,sum(c['result']=='leak_observed' for c in r['cases']))
    def test_metadata_has_no_tokens_paths_or_markers(self):
        s=json.dumps(self.execute(transport=self.transport('leak',200)))
        for value in [*self.env.values(),*[r[k] for r in self.p['resources'] for k in ('marker','path')]]:self.assertNotIn(value,s)
    def test_result_binds_to_exact_plan(self):
        r=self.execute();expected=hashlib.sha256(json.dumps(self.p,sort_keys=True,separators=(',',':')).encode()).hexdigest();self.assertEqual(expected,r['plan_sha256'])
    def test_response_read_failure_is_transport_error(self):
        class BrokenResponse:
            status=200
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self,size):raise TimeoutError('synthetic timeout')
        with patch('urllib.request.build_opener') as factory:
            factory.return_value.open.return_value=BrokenResponse()
            result=fetch('http://127.0.0.1:8765/synthetic','synthetic-credential',1)
            self.assertTrue(result['transport_error']);self.assertEqual(b'',result['body'])
    def test_no_network_without_optin(self):
        with patch.dict(os.environ,self.env):
            with self.assertRaises(ValueError):run(self.p,self.p['origin'],False,True,transport=lambda *a:self.fail('unexpected request'))
    def test_no_network_without_synthetic_flag(self):
        with self.assertRaises(ValueError):run(self.p,self.p['origin'],True,False,transport=lambda *a:self.fail('unexpected request'))
    def test_origin_mismatch(self):
        with self.assertRaises(ValueError):run(self.p,'http://127.0.0.1:9999',True,True,transport=lambda *a:self.fail('unexpected request'))
    def test_missing_credential(self):
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(ValueError):run(self.p,self.p['origin'],True,True)
    def test_identical_credentials(self):
        self.env['TG_TOKEN_B']=self.env['TG_TOKEN_A']
        with self.assertRaises(ValueError):self.execute()
    def test_header_injection_credential(self):
        self.env['TG_TOKEN_A']='unsafe\r\nheader:value'
        with self.assertRaises(ValueError):self.execute()
    def test_http_nonloopback_rejected(self):
        with self.assertRaises(ValueError):origin('http://staging.example.com')
    def test_origin_credentials_rejected(self):
        with self.assertRaises(ValueError):origin('https://user:pass@staging.example.com')
    def test_origin_path_rejected(self):
        with self.assertRaises(ValueError):origin('https://staging.example.com/api')
    def test_production_plan_rejected(self):
        self.p['environment']='production'
        with self.assertRaises(ValueError):validate_plan(self.p)
    def test_wrong_fixture_owner_rejected(self):
        self.p['resources'][0]['owner']='missing'
        with self.assertRaises(ValueError):validate_plan(self.p)
    def test_missing_own_control_rejected(self):
        self.p['resources'][1]['owner']='actor_a'
        with self.assertRaises(ValueError):validate_plan(self.p)
    def test_path_redirect_or_traversal_rejected(self):
        for path in ('//bad.test/x','/x/../../admin','/%252e%252e/admin','/x\\evil'):
            self.p['resources'][0]['path']=path
            with self.subTest(path=path):
                with self.assertRaises(ValueError):validate_plan(self.p)
    def test_reflected_marker_rejected(self):
        self.p['resources'][0]['path']+='?marker='+self.p['resources'][0]['marker']
        with self.assertRaises(ValueError):validate_plan(self.p)
    def test_overlapping_markers_rejected(self):
        self.p['resources'][1]['marker']=self.p['resources'][0]['marker']+'EXTRA'
        with self.assertRaises(ValueError):validate_plan(self.p)
    def test_dry_run_no_credentials_or_traffic(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/probe.py'),'--plan',str(ROOT/'assets/probe-plan.json'),'--dry-run'],capture_output=True,text=True,env={})
        self.assertEqual(0,p.returncode);self.assertEqual('dry_run_no_requests',json.loads(p.stdout)['status'])
    def test_real_loopback_secure_and_vulnerable(self):
        spec=importlib.util.spec_from_file_location('tg_demo',ROOT/'assets/demo_server.py');demo=importlib.util.module_from_spec(spec);spec.loader.exec_module(demo)
        for vulnerable in (False,True):
            server=demo.make_server(vulnerable);worker=Thread(target=server.serve_forever,daemon=True);worker.start()
            try:
                p=copy.deepcopy(self.p);p['origin']='http://127.0.0.1:'+str(server.server_port)
                with patch.dict(os.environ,{'TG_TOKEN_A':demo.TOKENS['actor_a'],'TG_TOKEN_B':demo.TOKENS['actor_b']}):r=run(p,p['origin'],True,True)
                self.assertTrue(r['positive_controls_valid']);self.assertTrue(all(c['result']==('leak_observed' if vulnerable else 'denied') for c in r['cases']))
            finally:server.shutdown();server.server_close();worker.join(timeout=2)

if __name__=='__main__':unittest.main()
