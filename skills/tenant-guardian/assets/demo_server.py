"""Synthetic local HTTP fixture. Not an example production authentication design."""
import argparse
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path

PLAN=json.loads((Path(__file__).with_name('probe-plan.json')).read_text())
TOKENS={'actor_a':'TG_DEMO_CREDENTIAL_ACTOR_A','actor_b':'TG_DEMO_CREDENTIAL_ACTOR_B'}

def make_server(vulnerable=False,port=0):
    resources={r['path']:r for r in PLAN['resources']}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            actor=next((a for a,t in TOKENS.items() if self.headers.get('Authorization')=='Bearer '+t),None)
            r=resources.get(self.path)
            if actor is None:status=401;payload={'error':'synthetic authentication required'}
            elif r is None:status=404;payload={'error':'synthetic object absent'}
            elif actor!=r['owner'] and not vulnerable:status=403;payload={'error':'synthetic denial'}
            else:status=200;payload={'synthetic':True,'marker':r['marker']}
            body=json.dumps(payload).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--vulnerable',action='store_true');p.add_argument('--port',type=int,default=8765);a=p.parse_args()
    if not 1024<=a.port<=65535:p.error('Use a local port from 1024 to 65535')
    server=make_server(a.vulnerable,a.port)
    print('Synthetic loopback fixture only; press Ctrl-C to stop. Mode:', 'vulnerable' if a.vulnerable else 'isolated',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
